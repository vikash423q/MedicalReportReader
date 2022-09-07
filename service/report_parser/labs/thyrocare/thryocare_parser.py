import re

from typing import List, Optional, Tuple
from dataclasses import fields
from datetime import datetime

import fitz
from fitz import Rect, CheckRect

from model.objects import TestField, ReportMeta, Report
from service.report_parser.labs.thyrocare.entities import Header
from service.report_parser.report_parser_base import ReportParser
from service.report_parser.labs.thyrocare.helper import parse_headers, is_float, parse_range, merge_ranges
from service.report_parser.labs.thyrocare.test_profiles import test_profiles
from model.enums import Laboratories
from config.base import config


class ThyroCareReportParser(ReportParser):
    def __init__(self, file):
        super().__init__(Laboratories.THYROCARE.value, file)
        self.doc = fitz.open(stream=self.file.read(), filetype="pdf")

    def parse_meta(self) -> ReportMeta:
        return self._extract_report_details(self.doc[0])

    def parse(self, test_names: List[str] = None) -> Report:
        test_fields = []
        for page in self.doc:
            header = parse_headers(page)
            if not header.valid:
                continue
            page_fields = self._extract_test_fields(page, header)
            test_fields.extend(page_fields)

        report_meta = self.parse_meta()

        if config.DEBUG:
            self.doc.save("output.pdf", garbage=4, deflate=True, clean=True)
        return Report(meta=report_meta, test_results=test_fields)

    def _extract_report_details(self, first_page, padding: int = 5) -> Optional[ReportMeta]:
        name_pattern = r"(.*)\((\d+)Y/([MF])\)"
        name_boxes = first_page.search_for(r"NAME")
        test_package = first_page.search_for(r"TEST ASKED")
        sct = first_page.search_for(r"Sample Collected on (SCT)")
        sct_page = first_page
        if not sct and len(self.doc) >= 1:
            sct = self.doc[1].search_for(r"Sample Collected on (SCT)")
            sct_page = self.doc[1]

        # extracting test asked (package)
        test_asked_rect = Rect(test_package[0].x1, test_package[0].y0 - padding,
                               first_page.rect.x1 // 2, test_package[0].y1 + padding)
        test_asked = first_page.get_textbox(test_asked_rect).strip(" \n:")

        # extracting sample collection time
        sct_rect = Rect(sct[0].x1, sct[0].y0 - padding, first_page.rect.x1 // 2 + padding, sct[0].y1 + padding)
        sct_value = sct_page.get_textbox(sct_rect).strip(" \n:")
        try:
            sct_datetime = datetime.strptime(sct_value, "%d %b %Y %H:%M")
        except ValueError:
            sct_datetime = sct_value

        # extracting patient details
        name_boxes.sort(key=lambda rect: rect.y0)
        name_rect = Rect(name_boxes[0].x1, name_boxes[0].y0-padding, first_page.rect.x1//2, name_boxes[0].y1+padding)
        name_rect_val = first_page.get_textbox(name_rect).strip()
        match = re.search(name_pattern, name_rect_val, re.I)
        if match:
            name, age, sex = match.group(1), int(match.group(2)), match.group(3)
        else:
            name, age, sex = "", 0, ""

        self._annotate_page(first_page, [test_asked_rect, name_rect, sct_rect])

        return ReportMeta(patient_name=name, patient_age=age, patient_sex=sex,
                          test_asked=test_asked, sample_collected_on=sct_datetime, lab=self.lab)

    def _extract_test_fields(self, page, header: Header, padding: int = 5):
        hd_boxes = [getattr(header, fd.name) for fd in fields(header)]
        hd_boxes = [box for box in hd_boxes if box]
        hd_end_y = max([rect.y1 for rect in hd_boxes])

        test_fields = []
        for test_profile in test_profiles:
            for test in test_profile.tests:
                rects: List[Rect] = page.search_for(test)
                rects = [rect for rect in rects if rect.y0 >= hd_end_y and
                         header.test_name.x0-padding <= rect.x0 <= header.test_name.x0+padding]
                if not rects:
                    continue

                if not header.technology:
                    header.technology = header.value

                normal_range, reference_range = None, None

                rect = rects[0]
                y0, y1 = rect.y0 - padding//2, rect.y1 + padding//2
                name_rect = Rect(rect.x0-padding, y0, header.technology.x0-padding, y1)
                tech_rect = Rect(header.technology.x0-padding, y0, header.value.x0-padding, y1)
                value_rect = Rect(header.value.x0-padding, y0, header.units.x0-padding, y1)
                units_rect = Rect(header.units.x0-padding, y0, page.rect.x1-padding, y1)

                name_val = page.get_textbox(name_rect)
                tech_val = page.get_textbox(tech_rect)
                value_val = page.get_textbox(value_rect)
                units_val = page.get_textbox(units_rect)

                all_rects = [name_rect, tech_rect, value_rect, units_rect]

                if header.normal_range:
                    units_rect = Rect(header.units.x0-padding, y0, header.normal_range.x0-padding, y1)
                    units_val = page.get_textbox(units_rect)
                    all_rects[3] = units_rect

                    normal_range_rect = Rect(header.normal_range.x0-padding, y0, page.rect.x1-padding, y1)
                    normal_range = page.get_textbox(normal_range_rect)
                    all_rects.append(normal_range_rect)

                if header.reference_range:
                    units_rect = Rect(header.units.x0-padding, y0, header.reference_range.x0-padding, y1)
                    units_val = page.get_textbox(units_rect)
                    all_rects[3] = units_rect

                    reference_range_rect = Rect(header.reference_range.x0-padding, y0, page.rect.x1-padding, y1)
                    reference_range = page.get_textbox(reference_range_rect)
                    all_rects.append(reference_range_rect)

                self._annotate_page(page, all_rects)

                if not header.normal_range and header.reference_range:
                    normal_range = reference_range

                test_field = TestField(test_name=name_val,
                                       technology=tech_val,
                                       test_profile=test_profile.profile_name,
                                       value=float(value_val) if is_float(value_val) else 0,
                                       units=units_val,
                                       normal_range=parse_range(normal_range))

                if not header.normal_range and not header.reference_range:
                    test_field.reference_range = self._find_reference_range(name_rect, units_val, page)

                if test_field.value:
                    test_fields.append(test_field)

        return test_fields

    def _find_reference_range(self, name_rect: Rect, units: str, page):
        def goto_next_line(rect, max_try: int = 5):
            val = ''
            next_rect = name_rect
            i = 0
            while not val and i < max_try:
                next_rect = Rect(rect.x0, rect.y1-3, page.rect.x1 // 2, 2 * rect.y1 - rect.y0+3)
                val = page.get_textbox(next_rect)
                rect = next_rect
                i += 1
            return next_rect

        def calc_range(val: str) -> List:
            val = val.replace(units, '').replace('=', '').replace('\n', ' ')
            range_pattern = r"([0-9\.]+)?\s*([<>-])\s*([0-9\.]+)"
            ranges = []

            for match in re.finditer(range_pattern, val):
                start, end = parse_range(match.group(0))
                left = f'([^:]+)[:-]\s*{match.group(0)}'
                m = re.search(left, val)
                if m:
                    name = re.sub(r'[^\w\s]|\d', '', m.group(1).strip()).strip()
                    ranges.append([name, [start, end]])
                    continue
                right = f'{match.group(0)}\s*[:-]([^:]+)'
                m = re.search(right, val)
                if m:
                    name = re.sub(r'[^\w\s]|\d', '', m.group(1).strip()).strip()
                    ranges.append([name, [start, end]])
                    continue

                if start or end:
                    ranges.append(['NORMAL', [start, end]])
            return ranges

        def re_calibrate(rect: Rect):
            text = page.get_textbox(rect)
            rects = page.search_for(text)
            rects.sort(key=lambda x: (x.x0 - rect.x0) ** 2 + (x.y0 - rect.y0) ** 2)
            return Rect(rect.x0, rects[0].y0, rect.x1, rects[0].y1)

        reference_ranges = []
        next_line = goto_next_line(name_rect)
        next_line = re_calibrate(next_line)
        next_line_val = page.get_textbox(next_line)
        if re.search("reference range", next_line_val, re.I):
            range_line = goto_next_line(next_line)
            range_line = re_calibrate(range_line)
            range_val = page.get_textbox(range_line)
            ref_range = calc_range(range_val)
            while ref_range:
                ref_range = merge_ranges(ref_range)
                if ref_range:
                    reference_ranges.extend(ref_range)
                range_line = goto_next_line(range_line)
                range_line = re_calibrate(range_line)
                range_val = page.get_textbox(range_line)
                ref_range = calc_range(range_val)
        return reference_ranges if reference_ranges else None

    def _annotate_page(self, page, rects):
        if not config.DEBUG:
            return

        red = (1, 0, 0)
        blue = (0, 0, 1)
        gold = (1, 1, 0)
        green = (0, 1, 0)
        cyan = (0, 1, 1)
        teal = (1, 1, 0)

        colors = [red, blue, gold, green, cyan, teal]

        for rect, col in zip(rects, colors):
            if not CheckRect(rect):
                continue
            annot = page.add_highlight_annot(rect)
            annot.set_colors(stroke=col)
