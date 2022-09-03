from typing import List, Union
from datetime import datetime

from fastapi import APIRouter, UploadFile, Form
from pydantic import BaseModel, Field

from service import report_service

report_router = APIRouter(prefix="/report")


class ReportRequest(BaseModel):
    user_id: str
    start_date: datetime
    end_date: datetime
    with_result: bool = Field(default=False)
    profiles: Union[List[str], None]


@report_router.post("/upload")
def upload_report(file: UploadFile, user_id: str = Form(), validate: bool = Form(default=True)):
    return report_service.parse_report(user_id, file.file, validate)


@report_router.post("/index")
def index_report(file: UploadFile, user_id: str = Form(),
                 validate_user: bool = Form(default=True),
                 validate_report: bool = Form(default=True)):
    return report_service.index_new_report(user_id, file.file, validate_user, validate_report)


@report_router.get("/")
def retrieve_reports(req: ReportRequest):
    return report_service.retrieve_reports(req.user_id, req.start_date, req.end_date, req.with_result, req.profiles)
