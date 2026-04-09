from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.database import get_db
from app.models.product import Product
from app.models.user import User, UserRole
from app.dependencies import get_current_user

router = APIRouter(prefix="/api/inventory", tags=["Inventory"])


class StockUpdate(BaseModel):
    quantity: int


def admin_only(user: User):
    if user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin only")


def get_product(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.get("/")
def get_inventory(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    admin_only(current_user)
    return db.query(Product).all()


@router.get("/{product_id}")
def get_product_stock(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    admin_only(current_user)
    product = get_product(db, product_id)

    return {
        "product_id": product.id,
        "name": product.name,
        "stock_quantity": product.stock_quantity,
        "size_liters": product.size_liters,
        "price": product.price,
    }


@router.put("/{product_id}/add-stock")
def add_stock(
    product_id: int,
    stock_update: StockUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    admin_only(current_user)
    product = get_product(db, product_id)

    if stock_update.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than 0")

    product.stock_quantity += stock_update.quantity
    db.commit()
    db.refresh(product)

    return {
        "message": "Stock added successfully",
        "stock_quantity": product.stock_quantity
    }


@router.put("/{product_id}/reduce-stock")
def reduce_stock(
    product_id: int,
    stock_update: StockUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    admin_only(current_user)
    product = get_product(db, product_id)

    if stock_update.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than 0")

    if product.stock_quantity < stock_update.quantity:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient stock. Available: {product.stock_quantity}"
        )

    product.stock_quantity -= stock_update.quantity
    db.commit()
    db.refresh(product)

    return {
        "message": "Stock reduced successfully",
        "stock_quantity": product.stock_quantity
    }