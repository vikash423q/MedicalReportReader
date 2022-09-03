from typing import List

from model.objects import Report, ReportMeta


class ReportParser:
    def __init__(self, lab: str, file):
        self.lab: str = lab
        self.file = file

    def parse(self, test_names: List[str] = None) -> Report:
        raise NotImplementedError()

    def parse_meta(self) -> ReportMeta:
        raise NotImplementedError()