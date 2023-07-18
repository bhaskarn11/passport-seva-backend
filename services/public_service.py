from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.appointment import PassportOffice, AppointmentSchedule, PoliceStation
from dependencies import get_db

router = APIRouter()


@router.get("/appointments/availability")
def get_appointment_slots(rpo_name: str, limit: int = 20, db: Session = Depends(get_db)):
    slots = db.query(PassportOffice).join(AppointmentSchedule)\
        .where(PassportOffice.rpo == rpo_name).all()

    for i in range(len(slots)):
        slots[i].appointment_schedules = slots[i].appointment_schedules

    return slots


@router.get("/psp-offices")
def get_passport_offices(rpo_name: str, db: Session = Depends(get_db)):
    offices = db.query(PassportOffice).where(PassportOffice.rpo == rpo_name).all()
    return offices


@router.get("/locate-police-stations")
def locate_police_stations(state: str, district: str = "", db: Session = Depends(get_db)):
    ps = db.query(PoliceStation).\
        where(PoliceStation.state.ilike(state)).\
        all()

    return ps


@router.get("/rpo")
def get_regional_psp_offices(db: Session = Depends(get_db)):
    r = [i[0] for i in db.query(PassportOffice.rpo).distinct(PassportOffice.rpo).all()]

    return r
