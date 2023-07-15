from database import Base
from sqlalchemy import Column, ForeignKey, String, Integer, Boolean, Date, Float, func
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(50), unique=True, index=True)
    is_email_verified = Column(Boolean, default=False)
    hashed_password = Column(String(100))
    dob = Column(Date)
    scopes = Column(String(50), default="user:public")
    disabled = Column(Boolean, default=False)


class ApplicantAddress(Base):
    __tablename__ = "applicant_addresses"

    arn = Column(String(30), ForeignKey("applications.arn"), primary_key=True)
    house_street = Column(String(50))
    city_name = Column(String(50))
    pin_code = Column(String(20))
    state = Column(String(30))
    district = Column(String(30))
    police_station = Column(String(30))


class ApplicantFamily(Base):
    __tablename__ = "applicant_family"

    arn = Column(String(30), ForeignKey("applications.arn"), primary_key=True, autoincrement=False)
    father_name = Column(String(50), nullable=True)
    mother_name = Column(String(50), nullable=True)
    legal_guardian_name = Column(String(50), nullable=True)
    spouse_name = Column(String(50), nullable=True)


class PrevPsp(Base):
    __tablename__ = "prev_psp_details"

    arn = Column(String(30), ForeignKey("applications.arn"), primary_key=True, autoincrement=False)
    is_identity_cert_held = Column(Boolean)
    is_diplomatic_psp_held = Column(Boolean)
    applied_psp_before = Column(Boolean)


class PaymentDetail(Base):
    __tablename__ = "payment_details"
    order_id = Column(String(30), unique=True)
    payment_id = Column(String(30), unique=True)
    arn = Column(String(30), ForeignKey("applications.arn"), primary_key=True, autoincrement=False)
    date = Column(Date)
    payment_gateway = Column(String(30))


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    arn = Column(String(30), unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")
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
    address_details = relationship("ApplicantAddress", uselist=False)
    family_details = relationship("ApplicantFamily", uselist=False)
    prev_psp_details = relationship("PrevPsp", uselist=False)
    fee = Column(Float(2))

    appointment = relationship("Appointment")
    payment_details = relationship("PaymentDetail")


class AppointmentSchedule(Base):
    __tablename__ = "appointment_schedules"

    po_code = Column(String(20), ForeignKey("passport_offices.po_code"), primary_key=True, index=True)
    passport_office = relationship("PassportOffice", back_populates="appointment_schedules", uselist=False)
    date = Column(Date, index=True)
    available_slots = Column(Integer)
    scheme_type = Column(String(30), primary_key=True, index=True)   # NORMAL/TATKAL
    application_type = Column(String(30), primary_key=True, index=True)  # PASSPORT/PCC


class PassportOffice(Base):
    __tablename__ = "passport_offices"

    po_code = Column(String(20), primary_key=True, autoincrement=False, index=True)
    address = Column(String(500))
    rpo = Column(String(20), index=True)
    state = Column(String(20))
    district = Column(String(20))
    appointment_capacity = Column(Integer)
    appointment_schedules = relationship("AppointmentSchedule")


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    arn = Column(String(30), ForeignKey("applications.arn"))
    date = Column(Date)
    po_code = Column(String(20), ForeignKey("passport_offices.po_code"))
    passport_office = relationship("PassportOffice")
    is_rescheduled = Column(Boolean, default=False)
    application = relationship("Application", back_populates="appointment")

#
# class TicketCategory(Base):
#     __tablename__ = "ticket_categories"
#
#     id = Column(Integer, primary_key=True)
#     category = Column(String(20))
#     sub_category = Column(String(20))
#
#
# class TicketReply(Base):
#     __tablename__ = "ticket_replies"
#     id = Column(Integer, primary_key=True)
#     ticket_id = Column(String(40), ForeignKey("support_tickets.id"))
#     description = Column(String(300))
#
#
#
#
# class Ticket(Base):
#     __tablename__ = "support_tickets"
#
#     id = Column(String(40), primary_key=True, autoincrement=False)
#     created_at = Column(Date, default=func.now())
#     last_updated = Column(Date)
#     po_code = Column(String(20), ForeignKey("passport_offices.po_code"))
#     description = Column(String(300))
#     phone_number = Column(String(20))
#     email = Column(String(20))
#     arn = Column(String(30))
#     file_number = Column(String(40))
#     category_id = Column(Integer, ForeignKey("ticket_categories.id"))
#     category = relationship("TicketCategory", uselist=False)
#
