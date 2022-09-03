from fastapi import APIRouter, Response
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from service import user_service

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
    response.headers['token'] = str(user.id)
    return jsonable_encoder(user, exclude={"id", "password", "salt"})
