from fastapi import APIRouter
from schemas.appointment import CreateAppointment, UpdateAppointment
router = APIRouter()


@router.post("/create")
def create_appointment(req: CreateAppointment):
    pass


@router.put("/update")
def reschedule_appointment(req: UpdateAppointment):
    pass

