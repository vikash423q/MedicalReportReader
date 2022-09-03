from typing import Optional, Union, List

from bson.objectid import ObjectId
from mongodb.mongo_template import MongoTemplate, report_db
from mongodb.mongo_queries import find_document
from mongodb.dbo.report import ProfileTestDTO
from utils import mongo_encoder

tests_collection = MongoTemplate.get_collection(report_db, "tests")


def insert_profile_test(test: ProfileTestDTO):
    test_dict = mongo_encoder(test, exclude={"id"})

    test_dict["_id"] = test.id
    return tests_collection.insert_one(test_dict)


def insert_many_profile_test(tests: List[ProfileTestDTO]):
    test_list = []
    for test in tests:
        test_dict = mongo_encoder(test, exclude={"id"})
        test_dict["_id"] = test.id
        test_list.append(test_dict)
    return tests_collection.insert_many(test_list)


def retrieve_test_by_id(_id: Union[str, ObjectId]) -> Optional[ProfileTestDTO]:
    if isinstance(_id, str):
        doc = find_document(tests_collection, dict(_id=ObjectId(_id)))
    else:
        doc = find_document(tests_collection, dict(_id=_id))
    if not doc:
        return
    doc["id"] = doc["_id"]
    return ProfileTestDTO(**doc)


def retrieve_tests_by_ids(_ids: List[ObjectId]) -> List[ProfileTestDTO]:
    docs = find_document(tests_collection, {"_id": {"$in": _ids}}, multiple=True)

    res = []
    for doc in docs:
        doc["id"] = doc["_id"]
        res.append(ProfileTestDTO(**doc))
    return res


def retrieve_tests_by_report_id(report_id: Union[str, ObjectId]) -> List[ProfileTestDTO]:
    if isinstance(report_id, str):
        docs = find_document(tests_collection, dict(user_id=ObjectId(report_id)), multiple=True)
    else:
        docs = find_document(tests_collection, dict(user_id=report_id), multiple=True)

    tests = []
    for doc in docs:
        doc["id"] = doc["_id"]
        tests.append(ProfileTestDTO(**doc))
    return tests
