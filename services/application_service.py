from models.application import Application, ApplicantFamily, ApplicantAddress, PrevPsp
from models.appointment import Appointment
from models.user import User
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.application import ApplicationResponse, CreateApplication, AppStatus
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
        app_name=req.app_name, status=req.status, application_type=req.application_type, fee=req.fee,
        scheme_type=req.scheme_type, booklet_type=req.booklet_type,
        first_name=req.first_name, last_name=req.last_name, gender=req.gender, dob=req.dob,
        marital_status=req.marital_status, email=req.email, mobile_number=req.mobile_number,
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
def get_application(arn: str, user_id: int, db: Session = Depends(get_db)):
    app = db.query(Application).where(Application.arn == arn, Application.user_id == user_id).first()

    if app:

        return app

    raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Application not found")


@router.delete("/{arn}")
def delete_application(arn: str, db: Session = Depends(get_db)):
    app = db.query(Application).where(Application.arn == arn, Application.status == AppStatus.DRAFT)
    if app.first():
        count = app.delete()
        db.commit()
        return {"deleted": True, "count": count}

    raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Bad request")


@router.post("/appointment")
def create_appointment(req: CreateAppointment, db: Session = Depends(get_db)):
    try:
        app = Appointment(arn=req.arn, date=req.date, po_code=req.po_code)
        db.add(app)
        db.commit()
        db.refresh(app)
        return app
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


@router.patch("/appointment")
def reschedule_appointment(req: UpdateAppointment, db: Session = Depends(get_db)):
    app = db.query(Appointment).where(Appointment.arn == req.arn)
    if not app.first():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Appointment Not Found")
    app.update({
        "date": req.date,
        "is_rescheduled": True
    })

    db.commit()
    db.refresh(app)
    return app
