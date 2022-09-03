from pydantic import BaseModel, Field

from mongodb.dbo.common import PydanticObjectId


class User(BaseModel):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId)
    name: str
    username: str
    password: str
    salt: str
    yob: int
    sex: str
