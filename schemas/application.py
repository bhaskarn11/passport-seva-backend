from pydantic import BaseModel


class PersonalDetails(BaseModel):
    firstName: str
    lastName: str
    gender: str
    maritalStatus: str
    mobileNumber: str
    dob: str

    class Config:
        orm_mode = True


class AddressDetails(BaseModel):
    houseStreet: str
    cityName: str
    pinCode: str
    state: str
    district: str
    policeStation: str

    class Config:
        orm_mode = True


class FamilyDetails(BaseModel):
    fatherName: str
    motherName: str
    legalGuardianName: str
    spouseName: str

    class Config:
        orm_mode = True


class PrevPspDetails(BaseModel):
    isIdentityCertHeld: bool
    isDiplomaticPassHeld: bool
    appliedPspBefore: bool

    class Config:
        orm_mode = True


class ApplicationBase(BaseModel):
    userId: int
    name: str
    status: str
    applicationType: str
    schemeType: str
    bookletType: str
    personalDetails: PersonalDetails
    addressDetails: AddressDetails
    prevPspDetails: PrevPspDetails

    class Config:
        orm_mode = True


class CreateApplication(ApplicationBase):
    pass


class ApplicationResponse(CreateApplication):
    pass
