import math
from service.report_parser.labs.thyrocare.entities import Header


def parse_headers(page) -> Header:
    headers = ["TEST NAME", "TECHNOLOGY", "VALUE", "UNITS", "NORMAL RANGE", "REFERENCE RANGE", "REF. RANGE"]

    header_names = []
    header_boxes = []

    last_boxes = page.search_for(headers[0])
    for header in headers[1:]:
        boxes = page.search_for(header)

        found = False
        for lb in last_boxes:
            for cb in boxes:
                if lb.y0 <= cb.y1 and lb.y1 >= cb.y0:
                    if not header_boxes:
                        header_names.append(headers[0])
                        header_boxes.append(lb)
                    header_names.append(header)
                    header_boxes.append(cb)
                    found = True
                    break
            if found:
                break
        last_boxes = boxes if boxes else last_boxes

    name_box_list = [(header_names[i], header_boxes[i]) for i in range(len(header_names))]
    name_box_list.sort(key=lambda t: t[1].x0)

    #  ["TEST NAME", "TECHNOLOGY", "VALUE", "UNITS", "NORMAL RANGE", "REFERENCE RANGE"]
    hd = Header()
    for name, box in name_box_list:
        if name == "TEST NAME":
            hd.test_name = box
        if name == "TECHNOLOGY":
            hd.technology = box
        if name == "VALUE":
            hd.value = box
        if name == "UNITS":
            hd.units = box
        if name == "NORMAL RANGE":
            hd.normal_range = box
        if name in ["REFERENCE RANGE", "REF. RANGE"]:
            hd.reference_range = box

    return hd


def is_float(num: str):
    try:
        return float(num)
    except ValueError:
        return None


def parse_range(value: str):
    start, end = None, None

    if not value:
        return start, end

    if "<" in value:
        s, e = value.split("<")[0], value.split("<")[1]
        start = float(s) if is_float(s) else None
        end = float(e) if is_float(e) else None
    if ">" in value:
        s, e = value.split(">")[0], value.split(">")[1]
        end = float(s) if is_float(s) else None
        start = float(e) if is_float(e) else None
    if "-" in value:
        s, e = value.split("-")[0], value.split("-")[1]
        start = float(s) if is_float(s) else None
        end = float(e) if is_float(e) else None
    return start, end


def merge_ranges(ranges: list):
    name_range = {}
    for range_ in ranges:
        name = range_[0]
        name_range.setdefault(name, [])
        name_range[name].append(range_)

    for name, ranges in name_range.items():
        if not ranges:
            continue

        ranges.sort(key=lambda r: (-1 if r[1][0] is None else r[1][0], math.inf if r[1][1] is None else r[1][1]))

        merged = []
        for i in range(len(ranges)-1):
            nxt = list(ranges[i+1][1])
            curr = list(ranges[i][1])

            cs, ce = -1 if curr[0] is None else curr[0], math.inf if curr[1] is None else curr[1]
            ns, ne = -1 if nxt[1] is None else nxt[0], math.inf if nxt[1] is None else nxt[1]

            if curr[1] > nxt[0]:
                rs = min(ns, cs)
                re = max(ne, ce)
                ranges[i+1][1] = [None if rs == -1 else rs, None if re == math.inf else re]
            else:
                merged.append(ranges[i])

        if ranges[-1][1] != [None, None]:
            merged.append(ranges[-1])
        name_range[name] = merged

    result = []
    keys = list(name_range.keys())
    for name in keys:
        if not name_range[name]:
            continue
        result.extend(name_range[name])

    return result
