from datetime import datetime

from pydantic import BaseModel


class CreateAppointment(BaseModel):
    date: datetime
    poCode: str
    rpoName: str
    arn: str


class GetAppointment(BaseModel):
    date: datetime
    poCode: str
    rpoName: str
    arn: str


class SearchAppointments(BaseModel):
    rpoName: str


class AppDateResponse(BaseModel):
    date: datetime
    available: int


class SearchResponse(BaseModel):
    rpoName: str
    poCode: str
    dates: list[AppDateResponse]
    capacity: int

