from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import logging

from app.core.database import get_db
from app.models.order import Order, OrderStatus
from app.models.product import Product
from app.models.user import User, UserRole
from app.schemas.order import OrderCreate, OrderUpdate, OrderDetailResponse
from app.dependencies import get_current_user

logger = logging.getLogger("wateraplus.orders")

router = APIRouter(prefix="/api/orders", tags=["Orders"])


# =========================
# HELPER FUNCTION
# =========================

def build_order_detail(order: Order):
    detail = OrderDetailResponse.from_orm(order)
    detail.product_name = order.product.name if order.product else "Unknown Product"
    detail.customer_name = order.user.name if order.user else "Unknown User"
    return detail


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
        logger.warning(f"Product not found: {order.product_id}")
        raise HTTPException(status_code=404, detail="Product not found")

    if product.stock_quantity < order.quantity:
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

    logger.info(
        f"Order created | order_id={new_order.id} user_id={current_user.id}"
    )

    detail = build_order_detail(new_order)
    detail.product_name = product.name
    detail.customer_name = current_user.name

    return detail


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

    orders = (
        db.query(Order)
        .filter(Order.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )

    return [build_order_detail(order) for order in orders]


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

    return [build_order_detail(order) for order in orders]


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

        # restore stock if cancelling
        if (
            order_update.status == OrderStatus.CANCELLED
            and order.status != OrderStatus.CANCELLED
        ):
            product = db.query(Product).filter(Product.id == order.product_id).first()

            if product:
                product.stock_quantity += order.quantity
                logger.info(f"Stock restored for product {product.id}")

        order.status = order_update.status

    db.commit()
    db.refresh(order)

    return build_order_detail(order)