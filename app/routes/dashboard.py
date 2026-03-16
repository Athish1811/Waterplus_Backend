from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.order import Order, OrderStatus
from app.models.product import Product
from app.models.user import User, UserRole
from app.dependencies import get_current_user

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

@router.get("/admin-stats")
def get_admin_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get admin dashboard statistics (Admin only)"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin only")

    total_orders = db.query(Order).count()
    pending_orders = db.query(Order).filter(Order.status == OrderStatus.PENDING).count()
    confirmed_orders = db.query(Order).filter(Order.status == OrderStatus.CONFIRMED).count()
    delivered_orders = db.query(Order).filter(Order.status == OrderStatus.DELIVERED).count()

    total_users = db.query(User).count()
    total_products = db.query(Product).count()

    # Calculate total revenue
    total_revenue = 0
    delivered_order_records = db.query(Order).filter(Order.status == OrderStatus.DELIVERED).all()
    for order in delivered_order_records:
        total_revenue += order.total_price

    # Calculate total stock
    total_stock = 0
    products = db.query(Product).all()
    for product in products:
        total_stock += product.stock_quantity

    return {
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "confirmed_orders": confirmed_orders,
        "delivered_orders": delivered_orders,
        "total_users": total_users,
        "total_products": total_products,
        "total_revenue": total_revenue,
        "available_stock": total_stock,
    }

@router.get("/user-stats/{user_id}")
def get_user_statistics(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user dashboard statistics"""
    # Users can only see their own stats; admins can see any
    if current_user.role != UserRole.ADMIN and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    total_orders = db.query(Order).filter(Order.user_id == user_id).count()
    pending_orders = db.query(Order).filter(
        Order.user_id == user_id,
        Order.status == OrderStatus.PENDING
    ).count()
    delivered_orders = db.query(Order).filter(
        Order.user_id == user_id,
        Order.status == OrderStatus.DELIVERED
    ).count()

    # Calculate total spent
    total_spent = 0
    orders = db.query(Order).filter(Order.user_id == user_id).all()
    for order in orders:
        total_spent += order.total_price

    return {
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
        "address": user.address,
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "delivered_orders": delivered_orders,
        "total_spent": total_spent,
    }

@router.get("/recent-orders")
def get_recent_orders(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get recent orders (Admin only)"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin only")
    orders = db.query(Order).order_by(Order.created_at.desc()).limit(limit).all()
    return orders

@router.get("/low-stock-products")
def get_low_stock_products(
    threshold: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get products with low stock (Admin only)"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin only")
    products = db.query(Product).filter(Product.stock_quantity <= threshold).all()
    return products
