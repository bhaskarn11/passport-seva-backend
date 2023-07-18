from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.appointment import CreateAppSlots, PassportOfficeSchema
from schemas.user import CreateUser
from models.appointment import PassportOffice, AppointmentSchedule
from dependencies import get_db
from sqlalchemy.dialects.mysql import insert

router = APIRouter()


@router.post("/psp-offices")
def add_passport_offices(req: list[PassportOfficeSchema], db: Session = Depends(get_db)):
    offices = []

    for item in req:
        offices.append(PassportOffice(**item.model_dump()))

    db.bulk_save_objects(offices)
    db.commit()

    return offices


@router.post("/appointments/slots")
def create_appointment_slots(req: list[CreateAppSlots], db: Session = Depends(get_db)):
    try:

        for item in req:
            stmt = insert(AppointmentSchedule).values(**item.model_dump())
            on_duplicate_key_stmt = stmt.on_duplicate_key_update(**item.model_dump())
            db.execute(on_duplicate_key_stmt)

        db.commit()

        return {"status": "success"}

    except Exception as e:
        print(e)
        return {"status": "failed"}


@router.post("/users")
def create_admin_user(req: CreateUser, db: Session = Depends(get_db)):
    pass