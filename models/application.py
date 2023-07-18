from database import Base
from sqlalchemy import Column, ForeignKey, String, Integer, Boolean, Date, Float, func
from sqlalchemy.orm import relationship


class ApplicantAddress(Base):
    __tablename__ = "applicant_addresses"

    arn = Column(String(30), ForeignKey("applications.arn", ondelete="CASCADE"), primary_key=True)
    house_street = Column(String(50))
    city_name = Column(String(50))
    pin_code = Column(String(20))
    state = Column(String(30))
    district = Column(String(30))
    police_station = Column(String(30))


class ApplicantFamily(Base):
    __tablename__ = "applicant_family"

    arn = Column(String(30), ForeignKey("applications.arn", ondelete="CASCADE"), primary_key=True, autoincrement=False)
    father_name = Column(String(50), nullable=True)
    mother_name = Column(String(50), nullable=True)
    legal_guardian_name = Column(String(50), nullable=True)
    spouse_name = Column(String(50), nullable=True)


class PrevPsp(Base):
    __tablename__ = "prev_psp_details"

    arn = Column(String(30), ForeignKey("applications.arn", ondelete="CASCADE"), primary_key=True, autoincrement=False)
    is_identity_cert_held = Column(Boolean)
    is_diplomatic_psp_held = Column(Boolean)
    applied_psp_before = Column(Boolean)


class PaymentDetail(Base):
    __tablename__ = "payment_details"
    order_id = Column(String(30), unique=True)
    payment_id = Column(String(30), unique=True)
    arn = Column(String(30), ForeignKey("applications.arn", ondelete="CASCADE"), primary_key=True, autoincrement=False)
    date = Column(Date)
    payment_gateway = Column(String(30))


# class ApplicationUpdate(Base):
#     id = Column(Integer, primary_key=True, index=True)
#     description = Column(String(300))
#     created_at = Column(Date, default=func.now())
#

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    arn = Column(String(30), unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship("User", uselist=False, cascade="expunge")
    first_name = Column(String(50))
    last_name = Column(String(50))
    gender = Column(String(20))
    marital_status = Column(String(20))
    email = Column(String(50))
    mobile_number = Column(String(20))
    dob = Column(Date)
    submitted_at = Column(Date, default=func.now())
    app_name = Column(String(40))
    status = Column(String(30))
    application_type = Column(String(20))  #
    scheme_type = Column(String(20))
    booklet_type = Column(String(20))
    address_details = relationship("ApplicantAddress", uselist=False, cascade="all, delete-orphan")
    family_details = relationship("ApplicantFamily", uselist=False, cascade="all, delete-orphan")
    prev_psp_details = relationship("PrevPsp", uselist=False, cascade="all, delete-orphan")
    fee = Column(Float(2))

    appointment = relationship("Appointment", uselist=False, cascade="all, delete-orphan")
    payment_details = relationship("PaymentDetail", uselist=False, cascade="all, delete-orphan")
