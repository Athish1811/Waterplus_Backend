from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import init_db
from app.routes import (
    auth_router,
    users_router,
    products_router,
    orders_router,
    suppliers_router,
    dashboard_router,
    contact_router,
    inventory_router,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5501",
        "http://localhost:5501",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    init_db()

app.include_router(auth_router)
app.include_router(users_router, prefix="/api")
app.include_router(products_router)
app.include_router(orders_router)
app.include_router(suppliers_router)
app.include_router(dashboard_router)
app.include_router(contact_router)
app.include_router(inventory_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Watera Plus API"}