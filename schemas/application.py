from pydantic import BaseModel as Base, ConfigDict
from datetime import date
from enum import Enum
from schemas.appointment import AppointmentResponse

class BaseModel(Base):
    model_config = ConfigDict(from_attributes=True)


class AppStatus(Enum):
    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    PROCESSING = "PROCESSING"
    PENDING_POLICE_CLEARANCE = "PENDING_POLICE_CLEARANCE"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class PersonalDetails(BaseModel):
    first_name: str
    last_name: str
    gender: str
    marital_status: str
    mobile_number: str
    dob: date


class AddressDetails(BaseModel):
    house_street: str
    city_name: str
    pin_code: str
    state: str
    district: str
    police_station: str


class FamilyDetails(BaseModel):
    father_name: str | None
    mother_name: str | None
    legal_guardian_name: str | None
    spouse_name: str | None


class PrevPspDetails(BaseModel):
    is_identity_cert_held: bool
    is_diplomatic_psp_held: bool
    applied_psp_before: bool


class PaymentDetail(BaseModel):
    order_id: str
    payment_id: str
    arn: str
    date: date
    payment_gateway: str


class ApplicationBase(BaseModel):
    app_name: str
    status: str
    application_type: str
    scheme_type: str
    booklet_type: str
    first_name: str
    last_name: str
    gender: str
    marital_status: str
    email: str
    mobile_number: str
    dob: date
    address_details: AddressDetails
    prev_psp_details: PrevPspDetails
    family_details: FamilyDetails
    fee: float


class CreateApplication(ApplicationBase):
    pass


class ApplicationResponse(ApplicationBase):
    user_id: int
    arn: str
    id: int
    payment_details: PaymentDetail = None
    submitted_at: date
    appointment: AppointmentResponse = None
    address_details: AddressDetails = None
    prev_psp_details: PrevPspDetails = None
    family_details: FamilyDetails = None


class CreatePayment(BaseModel):
    arn: str
    fee: float
