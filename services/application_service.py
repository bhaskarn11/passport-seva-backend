from models import Application, Appointment, AppointmentSchedule, PassportOffice
from fastapi import APIRouter


router = APIRouter()


@router.patch("/{arn}")
def update_application(arn: str):
    pass


@router.get("/{arn}")
def get_application(arn: str):
    pass


def delete_application():
    pass


