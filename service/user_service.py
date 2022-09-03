from uuid import uuid4

from fastapi.exceptions import HTTPException

from mongodb.user_collection import insert_user, retrieve_user_by_username
from mongodb.dbo.user import User


def add_new_user(username: str, password: str, name: str, yob: int, sex: str):
    user = retrieve_user_by_username(username)
    if user:
        raise HTTPException(status_code=400, detail="User already exist with this username!")
    user = User(name=name,
                username=username,
                password=password,
                salt=str(uuid4()),
                yob=yob,
                sex=sex)

    insert_user(user)


def retrieve_user(username: str, password: str) -> User:
    user = retrieve_user_by_username(username)
    if not user:
        raise HTTPException(status_code=400, detail="User doesn't exist with this username!")

    if user.password != password:
        raise HTTPException(status_code=400, detail="username or password is wrong!")

    return user
