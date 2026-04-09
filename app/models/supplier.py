from sqlalchemy import Column, String, Integer, DateTime, Boolean
from datetime import datetime
from app.models.base import Base


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(255), nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(20), nullable=False)

    company_name = Column(String(255), nullable=True)
    address = Column(String(500), nullable=True)
    city = Column(String(100), nullable=True)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Supplier id={self.id} name='{self.name}'>"