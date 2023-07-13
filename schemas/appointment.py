from datetime import datetime
from pydantic import BaseModel


class CreateAppointment(BaseModel):
    date: datetime
    po_code: str
    arn: str


class UpdateAppointment(CreateAppointment):
    pass


class GetAppointment(BaseModel):
    date: datetime
    po_code: str
    rpo_name: str
    arn: str


class AppDate(BaseModel):
    date: datetime
    available: int


class SearchResponse(BaseModel):
    rpo_name: str
    po_code: str
    dates: list[AppDate]
    capacity: int


class CreateAppSlots(BaseModel):
    available_slots: int
    po_code: str
    scheme_type: str
    application_type: str
    date: datetime

    class Config:
        orm_mode = True


class PassportOfficeSchema(BaseModel):
    po_code: str
    address: str
    rpo: str
    state: str
    district: str
    appointment_capacity: int
