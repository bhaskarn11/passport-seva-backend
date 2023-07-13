from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.appointment import CreateAppSlots, PassportOfficeSchema
from models import PassportOffice, AppointmentSchedule
from dependencies import get_db


router = APIRouter()


@router.get("/appointments/availability")
def get_appointment_slots(po_code: str, limit: int = 20, db: Session = Depends(get_db)):
    slots = db.query(AppointmentSchedule).where(AppointmentSchedule.po_code == po_code).all()
    return slots


@router.get("/psp-offices")
def get_passport_offices(rpo_name: str, db: Session = Depends(get_db)):
    offices = db.query(PassportOffice).where(PassportOffice.rpo == rpo_name).all()
    return offices


@router.post("/psp-offices")
def add_passport_offices(req: list[PassportOfficeSchema], db: Session = Depends(get_db)):
    psks = []

    for item in req:
        psks.append(PassportOffice(**item.model_dump()))

    db.bulk_save_objects(psks)
    db.commit()

    return psks


@router.post("/appointments/slots")
def create_appointment_slots(req: list[CreateAppSlots], db: Session = Depends(get_db)):
    slots = []

    for item in req:
        slots.append(AppointmentSchedule(**item.model_dump()))

    db.bulk_save_objects(slots)
    db.commit()

    return slots
