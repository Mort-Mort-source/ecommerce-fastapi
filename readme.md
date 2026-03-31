# EcoShop - Microservicios con FastAPI

Sistema de e-commerce desarrollado con arquitectura de microservicios usando FastAPI, SQLAlchemy y Docker Compose.

## Tecnologías Utilizadas

### Backend
- **FastAPI** - Framework principal
- **JWT (python-jose)** - Autenticación con tokens
- **SQLite** - Base de datos embebida
- **httpx** - Cliente HTTP para comunicación entre servicios

### Frontend
- HTML5 + JavaScript
- Tailwind CSS

### Infraestructura
- **Docker** y **Docker Compose**
- Redes internas Docker

## Servicios y Puertos

| Servicio           | Puerto | Descripción                          | Documentación Swagger          |
|--------------------|--------|--------------------------------------|--------------------------------|
| **User Service**   | 8001   | Autenticación y usuarios             | http://localhost:8001/docs     |
| **Product Service**| 8002   | Catálogo de productos                | http://localhost:8002/docs     |
| **Cart Service**   | 8003   | Gestión del carrito                  | http://localhost:8003/docs     |
| **Order Service**  | 8004   | Creación y gestión de órdenes        | http://localhost:8004/docs     |
| **Shipment Service**| 8005  | Gestión de envíos                    | http://localhost:8005/docs     |

**Frontend**: http://127.0.0.1:5500/frontend/index.html (Live Server recomendado)

## Cómo Levantar el Proyecto

### Requisitos previos
- Tener instalado **Docker** y **Docker Compose**

### Pasos para ejecutar

1. **Clonar el repositorio** (o ubicarte en la carpeta del proyecto)

2. **Levantar todos los servicios**:

```bash
docker compose down
docker compose up -d --build
```

2. **Verificar que todos los servicios estén corriendo:**
```bash
Bashdocker compose ps
```
Deberías ver los 5 servicios en estado Up.

4. **Acceder al Frontend:**
Abre el archivo frontend/index.html con Live Server (recomendado) o directamente en:
http://127.0.0.1:5500/frontend/index.html



URLs de Documentación (Swagger)

User Service: http://localhost:8001/docs
Product Service: http://localhost:8002/docs
Cart Service: http://localhost:8003/docs
Order Service: http://localhost:8004/docs
Shipment Service: http://localhost:8005/docs

5. **Flujo Recomendado de Prueba**

Registrar un usuario o iniciar sesión
**(Muy importante el usuario debe crearse con el formato simulando un correo real "prueba@test.com" "correo@prueba.com" "juan@cualquiercosa.com" es importante que tenga este tipo de formato o la pagina arroja error)**
Explorar el catálogo de productos
Agregar productos al carrito
Ir al carrito y pulsar "Generar Orden de Compra"
Revisar Mis Órdenes y Mis Envíos

## Estructura del proyecto
ecommerce-fastapi/
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── styles.css
├── services/
│   ├── user-service/
│   ├── product-service/
│   ├── cart-service/
│   ├── order-service/
│   └── shipment-service/
├── docker-compose.yml
└── README.md