# app/models.py

import uuid
from sqlalchemy import Column, String, Integer
from app.database import Base

def _generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"

    id = Column(String(length=36), primary_key=True, index=True, default=_generate_uuid, unique=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True, index=True)
    age = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, email={self.email}, age={self.age})>"
