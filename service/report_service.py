from datetime import datetime, timedelta
from typing import Union

import fitz
from bson.objectid import ObjectId
from starlette.exceptions import HTTPException

from model.enums import Laboratories
from model.objects import ReportMeta, Report
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
                                                            normal_range=test.normal_range,
                                                            reference_range=test.reference_range))

    report_id = ObjectId()
    profile_tests = [ProfileTestDTO(id=ObjectId(), report_id=report_id, profile_name=profile,
                                    tests={test.test_name: test for test in tests})
                     for profile, tests in profile_tests_map.items()]
    report_dto = ReportDTO(id=report_id, user_id=ObjectId(user), date=report.meta.sample_collected_on,
                           lab=report.meta.lab, package=report.meta.test_asked,
                           test_profiles={test.profile_name: test.id for test in profile_tests})

    report_collection.insert_report(report_dto)
    test_collection.insert_many_profile_test(profile_tests)


def retrieve_reports(user_id: str,  start_date: datetime, end_date: datetime):
    report_dtos = report_collection.retrieve_reports_with_date_range(ObjectId(user_id), start_date, end_date)
    report_dtos.sort(key=lambda r: r.date)
    return report_dtos


def retrieve_reports_with_results(user_id: str, start_date: datetime, end_date: datetime, profile: str,
                                  normalize: bool = True) -> dict:
    user = user_collection.retrieve_user_by_id(user_id)
    report_dtos = report_collection.retrieve_reports_with_date_range(ObjectId(user_id), start_date, end_date, profile)
    result = dict(profile=profile, tests=[], units={}, range={}, reference={}, data=[])

    test_profile_ids = [profile_id for rep in report_dtos
                        for prof, profile_id in rep.test_profiles.items() if prof == profile]
    test_profiles = test_collection.retrieve_tests_by_ids(test_profile_ids)
    test_profile_id_map = {tp.id: tp for tp in test_profiles}

    tests = []
    for report in report_dtos:
        if profile not in report.test_profiles:
            continue
        report_data = dict(report_id=str(report.id), date=report.date, key=report.date.strftime("%b %Y"))
        test_profile_id = report.test_profiles[profile]
        test_profile = test_profile_id_map[test_profile_id]

        for test_id, test in test_profile.tests.items():
            if test.test_name not in tests:
                tests.append(test.test_name)
            result['range'][test.test_name] = test.normal_range

            if not test.reference_range:
                result['reference'][test.test_name] = []
            if test.reference_range and user.sex == 'M':
                result['reference'][test.test_name] = [rr for rr in test.reference_range if rr[0].lower() != 'female']
            if test.reference_range and user.sex == 'F':
                result['reference'][test.test_name] = [rr for rr in test.reference_range if rr[0].lower() != 'male']

            result['units'][test.test_name] = test.units
            report_data[test.test_name] = test.value
        result['data'].append(report_data)

    result['tests'] = tests

    if normalize and result['data']:
        idx = 0
        normalized_data = []
        start_date, end_date = result['data'][0]['date'], result['data'][-1]['date']
        while start_date < end_date:
            next_date = start_date + timedelta(days=30)
            if idx < len(result['data']):
                curr: datetime = result['data'][idx]['date']
                if start_date <= curr < next_date:
                    normalized_data.append(result['data'][idx])
                    idx += 1
                else:
                    normalized_data.append(dict(key=start_date.strftime("%b %Y")))
            start_date = next_date

        result['data'] = normalized_data

    return result


def retrieve_report_count_for_user(user_id: Union[ObjectId, str]):
    return report_collection.retrieve_report_count(user_id)


def delete_report_for_user(user_id: Union[ObjectId, str], report_id: Union[ObjectId, str]):
    user = user_collection.retrieve_user_by_id(user_id)
    report = report_collection.retrieve_report_by_id(report_id)
    if not report:
        raise HTTPException(404, "Report not found!")
    if report.user_id != user.id:
        raise HTTPException(400, "Invalid Report!")
    test_collection.delete_tests_with_report_id(report_id)
    report_collection.delete_report(report_id)


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
        raise HTTPException(status_code=420, detail=" ".join(errors))


def validate_existing_report(user_id: str, report_meta: ReportMeta):
    report_date = report_meta.sample_collected_on
    start_date = report_date - timedelta(days=1)
    end_date = report_date + timedelta(days=1)
    existing = report_collection.retrieve_reports_with_date_range(ObjectId(user_id), start_date, end_date)
    if existing:
        raise HTTPException(status_code=421,
                            detail=f"Existing report {existing[0].id} found for date: {existing[0].date}")
