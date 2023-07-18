from datetime import date
from pydantic import BaseModel as Base, ConfigDict


class BaseModel(Base):
    model_config = ConfigDict(from_attributes=True)


class PassportOfficeSchema(BaseModel):
    po_code: str
    address: str
    rpo: str
    state: str
    district: str
    appointment_capacity: int


class AppointmentBase(Base):
    date: date
    po_code: str
    arn: str


class CreateAppointment(AppointmentBase):
    pass


class UpdateAppointment(AppointmentBase):
    pass


class AppointmentResponse(AppointmentBase):
    passport_office: PassportOfficeSchema | None


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


