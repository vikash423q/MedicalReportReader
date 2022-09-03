from typing import Optional, Union

from bson.objectid import ObjectId
from mongodb.mongo_template import MongoTemplate, report_db
from mongodb.mongo_queries import find_document
from mongodb.dbo.user import User
from utils import mongo_encoder

user_collection = MongoTemplate.get_collection(report_db, "user")


def insert_user(user: User):
    user_dict = mongo_encoder(user, exclude={"id"})

    user_dict["_id"] = user.id
    user_collection.insert_one(user_dict)


def retrieve_user_by_id(user_id: Union[str, ObjectId]) -> Optional[User]:
    if isinstance(user_id, str):
        doc = find_document(user_collection, dict(_id=ObjectId(user_id)))
    else:
        doc = find_document(user_collection, dict(_id=user_id))
    if not doc:
        return
    doc["id"] = doc["_id"]
    return User(**doc)


def retrieve_user_by_username(username: str) -> Optional[User]:
    doc = find_document(user_collection, dict(username=username))
    if not doc:
        return
    doc["id"] = doc["_id"]
    return User(**doc)
