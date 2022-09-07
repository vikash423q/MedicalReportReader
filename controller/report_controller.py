from typing import List, Union
from datetime import datetime

from fastapi import APIRouter, UploadFile, Form, Request
from pydantic import BaseModel, Field

from service import report_service, user_service

report_router = APIRouter(prefix="/report")


class ReportRequest(BaseModel):
    user_id: str
    start_date: datetime
    end_date: datetime
    profile: str
    scale: bool = Field(default=True)


@report_router.post("/upload")
def upload_report(file: UploadFile, user_id: str = Form(), validate: bool = Form(default=True)):
    return report_service.parse_report(user_id, file.file, validate)


@report_router.post("/index")
def index_report(file: UploadFile, user_id: str = Form(),
                 validate_user: bool = Form(default=True),
                 validate_report: bool = Form(default=True)):
    return report_service.index_new_report(user_id, file.file, validate_user, validate_report)


@report_router.post("/")
def retrieve_reports(req: ReportRequest):
    return report_service.retrieve_reports_with_results(req.user_id, req.start_date, req.end_date, req.profile, req.scale)


@report_router.delete("/{report_id}")
def delete_report(report_id: str, request: Request):
    return report_service.delete_report_for_user(request.cookies.get('id'), report_id)
