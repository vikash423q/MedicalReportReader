from uuid import uuid4
from typing import Union

from bson.objectid import ObjectId
from fastapi.exceptions import HTTPException

from mongodb import user_collection
from mongodb.dbo.user import User


def add_new_user(username: str, password: str, name: str, yob: int, sex: str):
    user = user_collection.retrieve_user_by_username(username)
    if user:
        raise HTTPException(status_code=400, detail="User already exist with this username!")
    user = User(name=name,
                username=username,
                password=password,
                salt=str(uuid4()),
                yob=yob,
                sex=sex)

    user_collection.insert_user(user)


def retrieve_user(username: str, password: str) -> User:
    user = user_collection.retrieve_user_by_username(username)
    if not user:
        raise HTTPException(status_code=400, detail="User doesn't exist with this username!")

    if user.password != password:
        raise HTTPException(status_code=400, detail="username or password is wrong!")

    return user


def retrieve_user_by_id(user_id: Union[str, ObjectId]) -> User:
    return user_collection.retrieve_user_by_id(user_id)
