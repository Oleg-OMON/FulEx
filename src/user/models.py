import datetime
from pydantic import BaseModel, Field
from typing import List, Dict


class UserResponseV1(BaseModel):
    id: int = Field(..., ge=1)
    login: str
    name: str


class UserAddRequestV1(BaseModel):
    id: int = Field(..., ge=1)
    login: str
    name: str


class StatsRepo(BaseModel):
    repo_id: int
    date: datetime.datetime
    stargazers: int
    forks: int
    watchers: int


class ResultUserRepo(BaseModel):
    users: UserResponseV1
    stats: List[StatsRepo]
