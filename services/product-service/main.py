from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers.products import router as products_router

app = FastAPI(
    title="Catálogo de Productos - Microservicio",
    description="Solo operaciones GET (lectura)"
)

# ==================== CORS ====================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", "http://127.0.0.1:5500", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear tablas automáticamente
Base.metadata.create_all(bind=engine)

# Incluir rutas
app.include_router(products_router, prefix="/products", tags=["products"])

@app.get("/")
def root():
    return {"message": "✅ Product Service está corriendo en el puerto 8002"}