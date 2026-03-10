from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
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

# ===============================
# Create FastAPI App
# ===============================
app = FastAPI(
    title="Watera Plus API",
    description="Backend API for Watera Plus Water Delivery System",
    version="1.0.0",
)

# ===============================
# CORS Configuration (VERY IMPORTANT - Keep Here)
# ===============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Temporary for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ===============================
# Startup Event
# ===============================
@app.on_event("startup")
def startup_event():
    init_db()

# ===============================
# Include Routers
# ===============================
app.include_router(auth_router)

app.include_router(users_router, prefix="/api")

app.include_router(products_router)
app.include_router(orders_router)
app.include_router(suppliers_router)
app.include_router(dashboard_router)
app.include_router(contact_router)
app.include_router(inventory_router)
# ===============================
# Root Endpoint
# ===============================
@app.get("/")
def read_root():
    return {
        "message": "Welcome to Watera Plus API",
        "version": "1.0.0",
        "docs": "/docs",
    }

# ===============================
# Health Check
# ===============================
@app.get("/health")
def health_check():
    return {"status": "ok"}


# ===============================
# Run Server Directly
# ===============================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.DEBUG,
    )
