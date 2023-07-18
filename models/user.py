from database import Base
from sqlalchemy import Column, ForeignKey, String, Integer, Boolean, Date, Float, func
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(50), unique=True, index=True)
    is_email_verified = Column(Boolean, default=False)
    hashed_password = Column(String(100))
    dob = Column(Date)
    scopes = Column(String(50), default="read, write")
    disabled = Column(Boolean, default=False)
