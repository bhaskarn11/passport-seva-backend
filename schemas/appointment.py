from datetime import date
from pydantic import BaseModel as Base, ConfigDict


class BaseModel(Base):
    model_config = ConfigDict(from_attributes=True)


class CreateAppointment(BaseModel):
    date: date
    po_code: str
    arn: str


class UpdateAppointment(CreateAppointment):
    pass


class GetAppointment(BaseModel):
    date: date
    po_code: str
    rpo_name: str
    arn: str


class AppDate(BaseModel):
    date: date
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
    date: date


class PassportOfficeSchema(BaseModel):
    po_code: str
    address: str
    rpo: str
    state: str
    district: str
    appointment_capacity: int
