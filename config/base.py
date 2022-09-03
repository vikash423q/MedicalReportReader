import os

config_dict = {
    # Routes
    "BASE_URL": "/report-reader/v1",
    "ADD_REPORT": "/report/add",

    # MONGODB
    "MONGO_HOST": "mongodb://127.0.0.1:27017",
    "MONGO_USER": "",
    "MONGO_PASS": "",
    "DB_NAME": "reportDB",

    "DEBUG": False
}


class Config:
    def __getattr__(self, item):
        return os.environ.get(item) if item in os.environ else config_dict.get(item)


config = Config()
