from typing import Optional, Union, List
from datetime import datetime

from bson.objectid import ObjectId
from mongodb.mongo_template import MongoTemplate, report_db
from mongodb.mongo_queries import find_document
from mongodb.dbo.report import ReportDTO
from utils import mongo_encoder

report_collection = MongoTemplate.get_collection(report_db, "report")


def insert_report(report: ReportDTO):
    report_dict = mongo_encoder(report, exclude={"id"})

    report_dict["_id"] = report.id
    report_collection.insert_one(report_dict)


def retrieve_report_by_id(_id: Union[str, ObjectId]) -> Optional[ReportDTO]:
    if isinstance(_id, str):
        doc = find_document(report_collection, dict(_id=ObjectId(_id)))
    else:
        doc = find_document(report_collection, dict(_id=_id))
    if not doc:
        return
    doc["id"] = doc["_id"]
    return ReportDTO(**doc)


def retrieve_reports_by_user_id(user_id: Union[str, ObjectId]) -> List[ReportDTO]:
    if isinstance(user_id, str):
        docs = find_document(report_collection, dict(user_id=ObjectId(user_id)), multiple=True)
    else:
        docs = find_document(report_collection, dict(user_id=user_id), multiple=True)

    reports = []
    for doc in docs:
        doc["id"] = doc["_id"]
        reports.append(ReportDTO(**doc))
    return reports


def retrieve_reports_with_date_range(user_id: ObjectId,
                                     start_date: datetime,
                                     end_date: datetime,
                                     profiles: List[str] = None) -> List[ReportDTO]:
    docs = find_document(report_collection,  dict(user_id=user_id,
                                                  date={"$gte": start_date, "$lte": end_date}), multiple=True)

    reports = []
    for doc in docs:
        doc["id"] = doc["_id"]
        report_dto = ReportDTO(**doc)

        if profiles:
            match_profiles = []
            for profile in report_dto.test_profiles:
                for prof in profiles:
                    if prof == profile:
                        match_profiles.append(profile)
            if not match_profiles:
                continue
            report_dto.test_profiles = {k: v for k, v in report_dto.test_profiles.items() if k in match_profiles}

        reports.append(report_dto)
    return reports
