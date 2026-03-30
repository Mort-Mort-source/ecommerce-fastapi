from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers.orders import router as orders_router

app = FastAPI(
    title="Órdenes de Compra - Microservicio",
    description="Generación de órdenes de compra"
)

# ==================== CORS ====================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", "http://127.0.0.1:5500", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
app.include_router(orders_router, prefix="/orders", tags=["orders"])

@app.get("/")
def root():
    return {"message": "✅ Order Service está corriendo en el puerto 8004"}