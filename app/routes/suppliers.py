from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.supplier import Supplier
from app.models.user import User, UserRole
from app.schemas.supplier import SupplierCreate, SupplierUpdate, SupplierResponse
from app.dependencies import get_current_user

router = APIRouter(prefix="/api/suppliers", tags=["Suppliers"])


# =========================
# HELPER FUNCTIONS
# =========================

def check_admin(user: User):
    if user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin only")


def get_supplier_or_404(db: Session, supplier_id: int):
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier


# =========================
# LIST SUPPLIERS (ADMIN)
# =========================

@router.get("/", response_model=List[SupplierResponse])
def list_suppliers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    check_admin(current_user)

    return db.query(Supplier).filter(Supplier.is_active == True).all()


# =========================
# GET SINGLE SUPPLIER
# =========================

@router.get("/{supplier_id}", response_model=SupplierResponse)
def get_supplier(
    supplier_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    check_admin(current_user)

    return get_supplier_or_404(db, supplier_id)


# =========================
# CREATE SUPPLIER
# =========================

@router.post("/", response_model=SupplierResponse, status_code=status.HTTP_201_CREATED)
def create_supplier(
    supplier: SupplierCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    check_admin(current_user)

    existing = db.query(Supplier).filter(Supplier.email == supplier.email).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Supplier with this email already exists"
        )

    new_supplier = Supplier(**supplier.model_dump())

    db.add(new_supplier)
    db.commit()
    db.refresh(new_supplier)

    return new_supplier


# =========================
# UPDATE SUPPLIER
# =========================

@router.put("/{supplier_id}", response_model=SupplierResponse)
def update_supplier(
    supplier_id: int,
    supplier_update: SupplierUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    check_admin(current_user)

    supplier = get_supplier_or_404(db, supplier_id)

    for field, value in supplier_update.model_dump(exclude_unset=True).items():
        setattr(supplier, field, value)

    db.commit()
    db.refresh(supplier)

    return supplier


# =========================
# DELETE SUPPLIER
# =========================

@router.delete("/{supplier_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_supplier(
    supplier_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    check_admin(current_user)

    supplier = get_supplier_or_404(db, supplier_id)

    db.delete(supplier)
    db.commit()