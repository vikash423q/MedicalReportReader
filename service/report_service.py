from datetime import datetime, timedelta
from typing import List

import fitz
from fastapi.encoders import jsonable_encoder
from bson.objectid import ObjectId
from starlette.exceptions import HTTPException

from model.enums import Laboratories
from model.objects import ReportMeta, Report, TestField, TestProfileReport, TestReport
from service.lab_parser_map import lab_parser_map
from mongodb.dbo.user import User
from mongodb.dbo.report import ReportDTO, ProfileTestDTO, TestDTO
from mongodb import user_collection
from mongodb import report_collection
from mongodb import test_collection
from fuzzywuzzy import fuzz


def parse_report(user: str, file, validate: bool) -> Report:
    user_detail = user_collection.retrieve_user_by_id(user)
    if not user_detail:
        raise HTTPException(status_code=404, detail="User not found!")

    lab_name = find_lab(file)
    if not lab_name:
        raise HTTPException(status_code=400, detail="Bad Request. Unsupported Lab Found!")

    lab_parser = lab_parser_map[lab_name](file)

    if validate:
        report_meta = lab_parser.parse_meta()
        validate_user_details(report_meta, user_detail)

    report = lab_parser.parse()
    return report


def index_new_report(user: str, file, validate_user: bool, validate_report: bool):
    report = parse_report(user, file, validate_user)

    if validate_report:
        validate_existing_report(user, report.meta)

    profile_tests_map = {}
    for test in report.test_results:
        profile_tests_map.setdefault(test.test_profile, [])
        profile_tests_map[test.test_profile].append(TestDTO(test_name=test.test_name,
                                                            technology=test.technology,
                                                            value=test.value,
                                                            units=test.units,
                                                            normal_range=test.normal_range))

    report_id = ObjectId()
    profile_tests = [ProfileTestDTO(id=ObjectId(), report_id=report_id, profile_name=profile,
                                    tests={test.test_name: test for test in tests})
                     for profile, tests in profile_tests_map.items()]
    report_dto = ReportDTO(id=report_id, user_id=ObjectId(user), date=report.meta.sample_collected_on,
                           lab=report.meta.lab, package=report.meta.test_asked,
                           test_profiles={test.profile_name: test.id for test in profile_tests})

    report_collection.insert_report(report_dto)
    test_collection.insert_many_profile_test(profile_tests)


def retrieve_reports(user_id: str, start_date: datetime, end_date: datetime,
                     with_results: bool, profiles: List[str] = None) -> List[TestReport]:
    report_dtos = report_collection.retrieve_reports_with_date_range(ObjectId(user_id), start_date, end_date, profiles)
    reports = [TestReport(report_id=str(rep.id), lab=rep.lab,
                          date=rep.date, package=rep.package) for rep in report_dtos]

    if with_results:
        profile_ids = [profile_id for rep in report_dtos for profile, profile_id in rep.test_profiles.items()]
        test_profiles = test_collection.retrieve_tests_by_ids(profile_ids)
        report_tests_map = {}
        for profile in test_profiles:
            report_tests_map.setdefault(str(profile.report_id), {})
            report_tests_map[str(profile.report_id)].setdefault(profile.profile_name, {})

            for test_name, test in profile.tests.items():
                test_dict = jsonable_encoder(test)
                test_field = TestField(test_profile=profile.profile_name, **test_dict)
                report_tests_map[str(profile.report_id)][profile.profile_name][test_name] = test_field

        for report in reports:
            report.profiles = report_tests_map[report.report_id]

    return reports


def find_lab(file) -> str:
    doc = fitz.open(stream=file.read(), filetype="pdf")
    first_page = doc[0]

    supported_labs = [Laboratories.THYROCARE.value]
    for lab in supported_labs:
        if first_page.search_for(lab.lower()):
            file.seek(0)
            return lab
    file.seek(0)


def validate_user_details(report_meta: ReportMeta, user: User):
    user_age = datetime.now().year - user.yob
    age_from_report = report_meta.patient_age + (datetime.now().year - report_meta.sample_collected_on.year)

    errors = []
    if user.sex != report_meta.patient_sex:
        errors.append("Gender difference found.")
    if abs(user_age - age_from_report) > 2:
        errors.append("Age difference found.")
    if fuzz.ratio(report_meta.patient_name.lower(), user.name.lower()) < 80:
        errors.append("Name difference found.")

    if errors:
        raise HTTPException(status_code=400, detail=" ".join(errors))


def validate_existing_report(user_id: str, report_meta: ReportMeta):
    report_date = report_meta.sample_collected_on
    start_date = report_date - timedelta(days=1)
    end_date = report_date + timedelta(days=1)
    existing = report_collection.retrieve_reports_with_date_range(ObjectId(user_id), start_date, end_date)
    if existing:
        raise HTTPException(status_code=400,
                            detail=f"Existing report {existing[0].id} found for date: {existing[0].date}")
