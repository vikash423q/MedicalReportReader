from service.report_parser.labs.thyrocare.entities import Header


def parse_headers(page) -> Header:
    headers = ["TEST NAME", "TECHNOLOGY", "VALUE", "UNITS", "NORMAL RANGE", "REFERENCE RANGE"]

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
        if name == "REFERENCE RANGE":
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
        start = float(s) if is_float(s) else None
        end = float(e) if is_float(e) else None
    if "-" in value:
        s, e = value.split("-")[0], value.split("-")[1]
        start = float(s) if is_float(s) else None
        end = float(e) if is_float(e) else None
    return start, end
