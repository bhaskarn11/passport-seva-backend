from database import Base
from sqlalchemy import Column, ForeignKey, String, Integer, Boolean, Date
from sqlalchemy.orm import relationship


class AppointmentSchedule(Base):
    __tablename__ = "appointment_schedules"

    po_code = Column(String(20), ForeignKey("passport_offices.po_code", ondelete="CASCADE"),
                     primary_key=True, index=True)

    passport_office = relationship("PassportOffice", back_populates="appointment_schedules", uselist=False,
                                   cascade="expunge")

    date = Column(Date, index=True)
    available_slots = Column(Integer)
    scheme_type = Column(String(30), primary_key=True, index=True)  # NORMAL/TATKAL
    application_type = Column(String(30), primary_key=True, index=True)  # PASSPORT/PCC


class PassportOffice(Base):
    __tablename__ = "passport_offices"

    po_code = Column(String(20), primary_key=True, autoincrement=False, index=True)
    address = Column(String(500))
    rpo = Column(String(20), index=True)
    state = Column(String(20))
    district = Column(String(20))
    appointment_capacity = Column(Integer)
    appointment_schedules = relationship("AppointmentSchedule", cascade="all")


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    arn = Column(String(30), ForeignKey("applications.arn", ondelete="CASCADE"))
    date = Column(Date)
    po_code = Column(String(20), ForeignKey("passport_offices.po_code", ondelete="CASCADE"))
    passport_office = relationship("PassportOffice", cascade="expunge")
    is_rescheduled = Column(Boolean, default=False)
    application = relationship("Application", back_populates="appointment", cascade="expunge")


class PoliceStation(Base):
    __tablename__ = "police_stations"
    id = Column(Integer, primary_key=True, index=True)
    state = Column(String(20))
    district = Column(String(20))
    state_code = Column(String(10))
    name = Column(String(20))
