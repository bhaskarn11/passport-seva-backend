from models import Application, User, ApplicantFamily, ApplicantAddress, PrevPsp, Appointment
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.application import ApplicationResponse, CreateApplication
from schemas.appointment import UpdateAppointment, CreateAppointment
from dependencies import get_db
from utils.application_utils import generate_arn
from utils.auth_utils import read_current_user

router = APIRouter()


@router.post("/create")
def create_application(req: CreateApplication, user: User = Depends(read_current_user), db: Session = Depends(get_db)):
    arn = generate_arn()
    add_det = ApplicantAddress(**req.address_details.model_dump(), arn=arn)
    prev_det = PrevPsp(**req.prev_psp_details.model_dump(), arn=arn)
    fam_det = ApplicantFamily(**req.family_details.model_dump(), arn=arn)

    app = Application(
        arn=arn, user_id=user.id,
        app_name=req.name, status=req.status, application_type=req.application_type, fee=1500,
        scheme_type=req.scheme_type, booklet_type=req.booklet_type,
        **req.personal_details.model_dump(),
        family_details=fam_det,
        address_details=add_det,
        prev_psp_details=prev_det
        )

    db.add(app)
    db.commit()
    db.refresh(app)
    return app


@router.patch("/{arn}")
def update_application(arn: str, db: Session = Depends(get_db)):
    pass


@router.get("/{arn}")
def get_application(arn: str, db: Session = Depends(get_db)):
    pass


@router.delete("/{arn}")
def delete_application():
    pass


@router.post("/appointment")
def create_appointment(req: CreateAppointment, db: Session = Depends(get_db)):
    app = Appointment(arn=req.arn, date=req.date, po_code=req.po_code)
    db.add(app)
    db.commit()
    db.refresh(app)
    return app


@router.patch("/appointment")
def reschedule_appointment(req: UpdateAppointment, db: Session = Depends(get_db)):
    app = db.query(Appointment).where(Appointment.arn == req.arn)
    app.update({
        "date": req.date,
        "is_rescheduled": True
    })

    db.commit()
    db.refresh(app)
    return app
