from datetime import datetime, timedelta

from bson.objectid import ObjectId
from fastapi import APIRouter, Response, Request
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from service import user_service, report_service
from utils import mongo_encoder

user_router = APIRouter(prefix="/user")


class UserRegisterRequest(BaseModel):
    name: str
    username: str
    password: str
    yob: int
    sex: str


class UserLoginRequest(BaseModel):
    username: str
    password: str


@user_router.post("/register")
def register_user(user: UserRegisterRequest):
    return user_service.add_new_user(user.username, user.password, user.name, user.yob, user.sex)


@user_router.post("/login")
def login_user(user: UserLoginRequest, response: Response):
    user = user_service.retrieve_user(user.username, user.password)
    response.set_cookie('id', str(user.id))
    response.headers.setdefault("Access-Control-Expose-Headers", "Authorization")
    user_dict = jsonable_encoder(user, exclude={"id", "password", "salt"})
    user_dict['id'] = str(user.id)
    return user_dict


@user_router.get("/session")
def user_session(request: Request, response: Response):
    user = user_service.retrieve_user_by_id(request.cookies.get('id'))
    user_dict = jsonable_encoder(user, exclude={"id", "password", "salt"})
    if user:
        user_dict['id'] = str(user.id)
    else:
        response.status_code = 404
    return user_dict


@user_router.get("/summary")
def user_summary(request: Request):
    user = user_service.retrieve_user_by_id(request.cookies.get('id'))
    start_date = datetime.now() - timedelta(days=180)
    report_count = report_service.retrieve_report_count_for_user(user.id)
    recent_reports = report_service.retrieve_reports(str(user.id), start_date=start_date, end_date=datetime.now())
    recent_reports = jsonable_encoder(recent_reports, custom_encoder={ObjectId: lambda ob: str(ob)})
    return dict(count=report_count, recent_reports=recent_reports)
