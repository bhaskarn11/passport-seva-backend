from pydantic import BaseModel as Base, ConfigDict
from datetime import date


class BaseModel(Base):
    model_config = ConfigDict(from_attributes=True)


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
    father_name: str
    mother_name: str
    legal_guardian_name: str
    spouse_name: str


class PrevPspDetails(BaseModel):
    is_identity_cert_held: bool
    is_diplomatic_psp_held: bool
    applied_psp_before: bool


class ApplicationBase(BaseModel):
    name: str
    status: str
    application_type: str
    scheme_type: str
    booklet_type: str
    personal_details: PersonalDetails
    address_details: AddressDetails
    prev_psp_details: PrevPspDetails
    family_details: FamilyDetails


class CreateApplication(ApplicationBase):
    pass


class ApplicationResponse(ApplicationBase):
    user_id: int


class CreatePayment(BaseModel):
    arn: str
    fee: float
