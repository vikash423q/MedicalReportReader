from typing import List
from dataclasses import dataclass, fields

from fitz import Rect


@dataclass
class Header:
    test_name: Rect = None
    technology: Rect = None
    value: Rect = None
    units: Rect = None
    normal_range: Rect = None
    reference_range: Rect = None

    @property
    def empty(self):
        return any([getattr(self, fd.name) for fd in fields(self)])

    @property
    def valid(self):
        return all([self.test_name, self.value, self.units])


@dataclass
class TestProfile:
    profile_name: str
    tests: List[str]
