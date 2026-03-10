from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.product import Product
from pydantic import BaseModel

router = APIRouter(prefix="/api/inventory", tags=["Inventory"])

class StockUpdate(BaseModel):
    quantity: int

@router.get("/")
def get_inventory(db: Session = Depends(get_db)):
    """Get all products with stock levels (Admin)"""
    products = db.query(Product).all()
    return products

@router.get("/{product_id}")
def get_product_stock(product_id: int, db: Session = Depends(get_db)):
    """Get stock level for specific product"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    return {
        "product_id": product.id,
        "name": product.name,
        "stock_quantity": product.stock_quantity,
        "size_liters": product.size_liters,
        "price": product.price,
    }

@router.put("/{product_id}/add-stock")
def add_stock(product_id: int, stock_update: StockUpdate, db: Session = Depends(get_db)):
    """Add stock to product (Admin)"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    if stock_update.quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quantity must be greater than 0"
        )
    
    product.stock_quantity += stock_update.quantity
    db.commit()
    db.refresh(product)
    
    return {
        "message": "Stock added successfully",
        "product": {
            "id": product.id,
            "name": product.name,
            "stock_quantity": product.stock_quantity,
        }
    }

@router.put("/{product_id}/reduce-stock")
def reduce_stock(product_id: int, stock_update: StockUpdate, db: Session = Depends(get_db)):
    """Reduce stock from product (Admin)"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    if stock_update.quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quantity must be greater than 0"
        )
    
    if product.stock_quantity < stock_update.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient stock. Available: {product.stock_quantity}"
        )
    
    product.stock_quantity -= stock_update.quantity
    db.commit()
    db.refresh(product)
    
    return {
        "message": "Stock reduced successfully",
        "product": {
            "id": product.id,
            "name": product.name,
            "stock_quantity": product.stock_quantity,
        }
    }
