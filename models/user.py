from database import Base
from sqlalchemy import Column, ForeignKey, String, Integer, Boolean, Date
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    firstName = Column(String(50))
    lastName = Column(String(50))
    email = Column(String(50), unique=True, index=True)
    is_email_verified = Column(Boolean, default=False)
    hashed_password = Column(String(100))
    dob = Column(Date)
    role = Column(String(20), nullable=True)

    applications = relationship("Application", back_populates="user")

