from database import Base
from sqlalchemy import Column, ForeignKey, String, Integer, Boolean, Date
from sqlalchemy.orm import relationship


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    arn = Column(String(30), ForeignKey("applications.arn"))
    date = Column(Date)
    po_code = Column(String(20), ForeignKey("passport_offices.po_code"))
    passport_office = relationship("PassportOffice", foreign_keys="po_code")
    is_rescheduled = Column(Boolean, default=False)


class PassportOffice(Base):
    __tablename__ = "passport_offices"

    po_code = Column(String(20), primary_key=True, autoincrement=False, unique=True, index=True)
    address = Column(String(500))
    rpo = Column(String(20))
    state = Column(String(20))
    district = Column(String(20))
    appointment_capacity = Column(Integer)
    appointment_schedules = relationship("AppointmentSchedule", back_populates="passport_office")


class AppointmentSchedule(Base):
    __tablename__ = "appointment_schedules"

    po_code = Column(String(20), ForeignKey("passport_offices.po_code"), primary_key=True, index=True)
    passport_office = relationship("PassportOffice", back_populates="appointment_schedules",
                                   foreign_keys="po_code", uselist=False)
    date = Column(Date)
    available_slots = Column(Integer)
    scheme_type = Column(String(30), primary_key=True, index=True)   # NORMAL/TATKAL
    application_type = Column(String(30), primary_key=True, index=True)  # PASSPORT/PCC

