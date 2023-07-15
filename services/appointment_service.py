from fastapi import APIRouter, Security, Depends
from sqlalchemy.orm import Session
from schemas.appointment import CreateAppointment, UpdateAppointment
from models import Appointment, PassportOffice, AppointmentSchedule
from utils.auth_utils import read_current_user
from dependencies import get_db

router = APIRouter()


@router.get("/availability")
def get_appointment_slots(rpo_name: str, limit: int = 20, db: Session = Depends(get_db)):
    slots = db.query(PassportOffice).join(AppointmentSchedule)\
        .where(PassportOffice.rpo == rpo_name).all()

    for i in range(len(slots)):
        slots[i].appointment_schedules = slots[i].appointment_schedules

    return slots
