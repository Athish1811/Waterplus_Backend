from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.models.user import User, UserRole
from app.dependencies import get_current_user

router = APIRouter(prefix="/api/products", tags=["Products"])


# =========================
# HELPER FUNCTIONS
# =========================

def get_product_or_404(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


def check_admin(user: User):
    if user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized")


# =========================
# GET ALL PRODUCTS
# =========================

@router.get("/", response_model=List[ProductResponse])
def list_products(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 20
):
    return (
        db.query(Product)
        .filter(Product.is_active == True)
        .offset(skip)
        .limit(limit)
        .all()
    )


# =========================
# GET SINGLE PRODUCT
# =========================

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    return get_product_or_404(db, product_id)


# =========================
# CREATE PRODUCT (ADMIN)
# =========================

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    check_admin(current_user)

    # Check if product already exists
    existing = db.query(Product).filter(Product.name == product.name).first()

    # If exists → increase stock instead of error
    if existing:
        existing.stock_quantity += product.stock_quantity
        db.commit()
        db.refresh(existing)
        return existing

    # Create new product
    new_product = Product(**product.model_dump())

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


# =========================
# UPDATE PRODUCT (ADMIN)
# =========================

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_update: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    check_admin(current_user)

    product = get_product_or_404(db, product_id)

    for field, value in product_update.dict(exclude_unset=True).items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)

    return product


# =========================
# DELETE PRODUCT (ADMIN)
# =========================

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    check_admin(current_user)

    product = get_product_or_404(db, product_id)

    db.delete(product)
    db.commit()

    return {"message": "Product deleted successfully"}