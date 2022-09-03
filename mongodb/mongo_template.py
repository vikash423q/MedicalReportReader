from dataclasses import dataclass

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from config.base import config


NAMED_CONCERN_DICT = {
    "w1": 1,
    "w2": 2,
    "w3": 3,
    "majority": "majority"
}


@dataclass
class MongoTemplate:
    @staticmethod
    def create_mongo_client() -> MongoClient:
        try:
            return MongoClient(host=config.MONGO_HOST, username=config.MONGO_USER, password=config.MONGO_PASS)
        except ConnectionFailure:
            print(f"ERROR! Connecting to Mongo DB Failed !!")

    @staticmethod
    def get_database(client: MongoClient):
        if MongoTemplate.check_db_existence(config.DB_NAME, client):
            return client.get_database(config.DB_NAME)
        raise Exception(f"No database found by name {config.DB_NAME}")

    @staticmethod
    def get_collection(database, collection_name):
        return database[collection_name]

    @staticmethod
    def check_db_existence(db_name, client):
        list_of_dbs = client.list_database_names()
        if db_name in list_of_dbs:
            return True
        return False

    @staticmethod
    def check_collection_existence(collection, database):
        collection_list = database.list_collection_names()
        if collection in collection_list:
            return True
        return False


mongo_client = MongoTemplate.create_mongo_client()
report_db = MongoTemplate.get_database(mongo_client)
