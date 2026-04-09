from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings


# =========================
# DATABASE ENGINE
# =========================

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True
)


# =========================
# SESSION FACTORY
# =========================

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)


# =========================
# DATABASE DEPENDENCY
# =========================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# INITIALIZE DATABASE
# =========================

def init_db():
    from app.models.base import Base
    Base.metadata.create_all(bind=engine)