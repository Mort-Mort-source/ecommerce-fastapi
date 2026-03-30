from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers.auth import router as auth_router

app = FastAPI(
    title="Gestión de Usuarios - Microservicio",
    description="Servicio de registro, login y autenticación JWT"
)

# ==================== CORS ====================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],                    # En desarrollo: permite todo
    allow_credentials=True,
    allow_methods=["*"],                    # GET, POST, PUT, DELETE, OPTIONS...
    allow_headers=["*"],                    # Authorization, Content-Type, etc.
)

# Crear tablas automáticamente
Base.metadata.create_all(bind=engine)

# Incluir rutas
app.include_router(auth_router, prefix="/auth", tags=["auth"])

@app.get("/")
def root():
    return {"message": "✅ User Service está corriendo en el puerto 8001"}