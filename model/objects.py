from datetime import datetime
from typing import Any, List, Dict, Union

from pydantic import BaseModel


class ReportMeta(BaseModel):
    lab: str
    patient_name: str
    patient_age: int
    patient_sex: str
    test_asked: str
    sample_collected_on: datetime


class TestField(BaseModel):
    test_name: str
    test_profile: str
    technology: str
    value: float
    units: str
    normal_range: Any
    reference_range: Any


class Report(BaseModel):
    meta: ReportMeta
    test_results: List[TestField]


class TestProfileReport(BaseModel):
    profile_id: str
    tests: Dict[str, TestField]


class TestReport(BaseModel):
    report_id: str
    date: datetime
    lab: str
    package: str
    profiles: Union[Dict[str, TestProfileReport], None]
