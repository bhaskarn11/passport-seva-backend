from models import User, Application
from schemas.user import CreateUser, PasswordResetReq, UserResponse, Token, CurrentUserResponse
from fastapi import APIRouter, Depends, HTTPException, status
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

    try:
        hashed_pass = pbkdf2_sha256.hash(req.password)
        user = User(first_name=req.first_name, last_name=req.last_name,
                    dob=req.dob, email=req.email, hashed_password=hashed_pass)

        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError as e:
        raise CustomHTTPException("Internal Error", status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("/login", response_model=Token)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"username": user.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me")
def get_current_user(current_user: User = Depends(read_current_user)):
    return current_user


@router.delete("/{user_id}", response_model=UserResponse)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        q = db.query(User).where(User.id == user_id).delete()
        db.commit()

        return {"deleted_rows": q}
    except Exception as e:
        raise CustomHTTPException("Error occurred", status_code=status.HTTP_404_NOT_FOUND)


@router.post("/password/reset")
def reset_password(req: PasswordResetReq, db: Session = Depends(get_db)):
    pass


@router.get("/{user_id}/applications")
def get_applications_by_user(user_id: int, limit: int = 10, db: Session = Depends(get_db)):
    apps = db.query(Application).where(Application.user_id == user_id).limit(limit).all()
    return apps


@router.get("/{user_id}", response_model=UserResponse)
def get_user_details(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).where(User.id == user_id).first()

    if not user:
        raise CustomHTTPException("No user Found", status.HTTP_404_NOT_FOUND)

    return user
