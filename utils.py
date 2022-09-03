from datetime import datetime

from fastapi.encoders import jsonable_encoder
from bson.objectid import ObjectId


def mongo_encoder(obj, **kwargs):
    return jsonable_encoder(obj, custom_encoder={ObjectId: lambda ob: ob,
                                                 datetime: lambda ob: ob}, **kwargs)
