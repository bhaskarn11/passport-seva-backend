from database import Base
from sqlalchemy import Column, ForeignKey, String, Integer, Boolean, Date, Float
from sqlalchemy.orm import relationship


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    arn = Column(String(30), unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="applications")
    firstName = Column(String(50))
    lastName = Column(String(50))
    gender = Column(String(20))
    email = Column(String(50))
    mobileNumber = Column(String(20))
    submittedAt = Column(Date)
    name = Column(String(40))
    status = Column(String(30))
    applicationType = Column(String(20))  #
    schemeType = Column(String(20))
    bookletType = Column(String(20))
    addressDetails = relationship("ApplicantAddress", uselist=False)
    familyDetails = relationship("ApplicantFamily", uselist=False)
    prevPspDetails = relationship("PrevPsp", uselist=False)
    fee = Column(Float(2))


class ApplicantAddress(Base):
    __tablename__ = "applicant_addresses"

    arn = Column(String(30), ForeignKey("applications.arn"), primary_key=True)
    houseStreet = Column(String(50))
    cityName = Column(String(50))
    pinCode = Column(String(20))
    state = Column(String(30))
    district = Column(String(30))
    policeStation = Column(String(30))


class ApplicantFamily(Base):
    __tablename__ = "applicant_family"

    arn = Column(String(30), ForeignKey("applications.arn"), primary_key=True)
    fatherNme = Column(String(50), nullable=True)
    motherName = Column(String(50), nullable=True)
    legalGuardianName = Column(String(50), nullable=True)
    spouseName = Column(String(50), nullable=True)


class PrevPsp(Base):
    __tablename__ = "prev_psp_details"

    arn = Column(String(30), ForeignKey("applications.arn"), primary_key=True)
    isIdentityCertHeld = Column(Boolean)
    isDiplomaticPassHeld = Column(Boolean)
    appliedPspBefore = Column(Boolean)
