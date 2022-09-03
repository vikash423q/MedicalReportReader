from model.enums import Laboratories
from service.report_parser.labs.thyrocare.thryocare_parser import ThyroCareReportParser

lab_parser_map = {
    Laboratories.THYROCARE.value: ThyroCareReportParser
}