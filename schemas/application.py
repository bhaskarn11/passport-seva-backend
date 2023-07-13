from pydantic import BaseModel
from datetime import date


class PersonalDetails(BaseModel):
    first_name: str
    last_name: str
    gender: str
    marital_status: str
    mobile_number: str
    dob: date

    class Config:
        orm_mode = True


class AddressDetails(BaseModel):
    house_street: str
    city_name: str
    pin_code: str
    state: str
    district: str
    police_station: str

    class Config:
        orm_mode = True


class FamilyDetails(BaseModel):
    father_name: str
    mother_name: str
    legal_guardian_name: str
    spouse_name: str

    class Config:
        orm_mode = True


class PrevPspDetails(BaseModel):
    is_identity_cert_held: bool
    is_diplomatic_psp_held: bool
    applied_psp_before: bool

    class Config:
        orm_mode = True


class ApplicationBase(BaseModel):
    user_id: int
    name: str
    status: str
    application_type: str
    scheme_type: str
    booklet_type: str
    personal_details: PersonalDetails
    address_details: AddressDetails
    prev_psp_details: PrevPspDetails

    class Config:
        orm_mode = True


class CreateApplication(ApplicationBase):
    pass


class ApplicationResponse(CreateApplication):
    pass
