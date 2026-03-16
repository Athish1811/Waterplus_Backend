
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.order import Order, OrderStatus
from app.models.product import Product
from app.models.user import User, UserRole
from app.schemas.order import OrderCreate, OrderUpdate, OrderResponse, OrderDetailResponse
from app.dependencies import get_current_user
import logging

logger = logging.getLogger("wateraplus.orders")

router = APIRouter(prefix="/api/orders", tags=["Orders"])


# =========================
# USER → CREATE ORDER
# =========================

@router.post("/", response_model=OrderDetailResponse)
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    product = db.query(Product).filter(Product.id == order.product_id).first()
    if not product:
        logger.warning(f"Order creation failed: Product not found (id={order.product_id}) by user {current_user.id}")
        raise HTTPException(status_code=404, detail="Product not found")
    if product.stock_quantity < order.quantity:
        logger.warning(f"Order creation failed: Not enough stock for product {product.id} by user {current_user.id}")
        raise HTTPException(
            status_code=400,
            detail=f"Only {product.stock_quantity} items left"
        )
    total_price = product.price * order.quantity
    new_order = Order(
        user_id=current_user.id,
        product_id=order.product_id,
        quantity=order.quantity,
        total_price=total_price,
        delivery_address=order.delivery_address
    )
    product.stock_quantity -= order.quantity
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    logger.info(f"Order created: order_id={new_order.id}, user_id={current_user.id}, product_id={order.product_id}, quantity={order.quantity}")

    # Convert to OrderDetailResponse
    return OrderDetailResponse(
        **new_order.__dict__,
        product_name=product.name,
        customer_name=current_user.name
    )


# =========================
# USER → MY ORDERS
# =========================

@router.get("/my-orders", response_model=List[OrderDetailResponse])
def get_my_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 20
):
    orders = db.query(Order).filter(Order.user_id == current_user.id).offset(skip).limit(limit).all()

    # Enrich with product names
    result = []
    for o in orders:
        detail = OrderDetailResponse.from_orm(o)
        detail.product_name = o.product.name if o.product else "Unknown Product"
        result.append(detail)

    return result


# =========================
# ADMIN → GET ALL ORDERS
# =========================

@router.get("/admin", response_model=List[OrderDetailResponse])
def get_all_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 20
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin only")
    orders = db.query(Order).offset(skip).limit(limit).all()

    result = []
    for o in orders:
        detail = OrderDetailResponse.from_orm(o)
        detail.product_name = o.product.name if o.product else "Unknown Product"
        detail.customer_name = o.user.name if o.user else "Unknown User"
        result.append(detail)

    return result


# =========================
# ADMIN → UPDATE STATUS
# =========================

@router.put("/admin/{order_id}/status", response_model=OrderDetailResponse)
def update_order_status(
    order_id: int,
    order_update: OrderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin only")

    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order_update.status:
        # Restore stock if cancelling a non-cancelled order
        if order_update.status == OrderStatus.CANCELLED and order.status != OrderStatus.CANCELLED:
            product = db.query(Product).filter(Product.id == order.product_id).first()
            if product:
                product.stock_quantity += order.quantity
                logger.info(f"Stock restored for product {product.id}: +{order.quantity}")
        order.status = order_update.status

    db.commit()
    db.refresh(order)

    detail = OrderDetailResponse.from_orm(order)
    detail.product_name = order.product.name if order.product else "Unknown Product"
    detail.customer_name = order.user.name if order.user else "Unknown User"

    return detail