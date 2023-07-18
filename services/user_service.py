from models.user import User
from models.application import Application
from schemas.user import CreateUser, PasswordResetReq, UserResponse, Token, CurrentUserResponse
from fastapi import APIRouter, Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordRequestForm
from dependencies import get_db
from passlib.hash import pbkdf2_sha256
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from schemas import CustomHTTPException
from utils.auth_utils import authenticate_user, create_access_token, read_current_user

router = APIRouter()


@router.post("/create", status_code=status.HTTP_200_OK, response_model=UserResponse)
def create_user(req: CreateUser, db: Session = Depends(get_db)):
    if "delete" in req.scopes or "user:admin" in req.scopes:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Cannot have delete/admin permission")

    try:
        hashed_pass = pbkdf2_sha256.hash(req.password)
        scopes = ",".join(req.scopes)
        user = User(first_name=req.first_name, last_name=req.last_name, scopes=scopes,
                    dob=req.dob, email=req.email, hashed_password=hashed_pass)

        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        print(e)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Error occurred")


@router.post("/login", response_model=Token)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    print(form_data.username)
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    for scope in user.scopes.split(","):
        if scope not in form_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User scope mismatch",
                headers={"WWW-Authenticate": "Bearer"},
            )

    access_token = create_access_token(
        data={"username": user.email, "scopes": form_data.scopes}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=CurrentUserResponse)
def get_current_user(current_user: User = Depends(read_current_user)):
    return current_user


@router.delete("/{user_id}", response_model=UserResponse,
               dependencies=[Security(read_current_user, scopes=['user:admin'])]
               )
def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        q = db.query(User).where(User.id == user_id).delete()
        db.commit()

        return {"deleted_rows": q}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.post("/password/reset", dependencies=[Security(read_current_user, scopes=['read', 'write'])])
def reset_password(req: PasswordResetReq, db: Session = Depends(get_db)):
    user = db.query(User).where(User.email == req.email).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail={"message": "User not found"})
    if not user.email == req.email:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail={"message": "Email not matched"})

    # TODO: an email with password change request will be sent
    return {"status": "success"}


@router.get("/{user_id}/applications",
            dependencies=[Security(read_current_user, scopes=['read', 'write'])]
            )
def get_applications_by_user(user_id: int, limit: int = 10, db: Session = Depends(get_db)):
    apps = db.query(Application).where(Application.user_id == user_id).limit(limit).all()
    return apps


@router.get("/{user_id}", response_model=UserResponse,
            dependencies=[Security(read_current_user, scopes=['read', 'write'])]
            )
def get_user_details(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).where(User.id == user_id).first()

    if not user:
        raise CustomHTTPException("No user Found", status.HTTP_404_NOT_FOUND)

    return user


@router.get("/check-username")
def check_username(username: str, db: Session = Depends(get_db)):
    try:
        user = db.query(User).where(User.email == username).first()

        if not user:
            return {"username_available": True}

        return {"username_available": False}

    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


@router.get("/{user_id}/appointments")
def get_appointments_by_user(user_id: int):
    pass

