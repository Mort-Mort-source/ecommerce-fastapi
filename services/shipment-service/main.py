from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers.shipments import router as shipments_router

app = FastAPI(
    title="Órdenes de Envío - Microservicio",
    description="Gestión automática de órdenes de envío"
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
app.include_router(shipments_router, prefix="/shipments", tags=["shipments"])

@app.get("/")
def root():
    return {"message": "✅ Shipment Service está corriendo en el puerto 8005"}