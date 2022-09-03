from typing import Dict
from datetime import datetime

from pydantic import BaseModel, Field
from mongodb.dbo.common import PydanticObjectId


class ReportDTO(BaseModel):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId)
    user_id: PydanticObjectId
    test_profiles: Dict[str, PydanticObjectId]
    date: datetime
    lab: str
    package: str
    created_date: datetime = Field(default_factory=datetime.now)


class TestDTO(BaseModel):
    test_name: str
    technology: str
    value: float
    units: str
    normal_range: list


class ProfileTestDTO(BaseModel):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId)
    report_id: PydanticObjectId
    profile_name: str
    tests: Dict[str, TestDTO]
