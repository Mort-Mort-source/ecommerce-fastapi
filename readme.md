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

## Ejecución del proyecto

### Requisitos previos
- Tener instalado **Docker** y **Docker Compose (Versión oficial)**

**[!NOTE]**
**Se recomienda instalar Docker desde el repositorio oficial.
 Algunas instalaciones (como docker.io en Linux) pueden no incluir "buildx", lo que puede causar errores al construir las imagenes.**

### Primer uso (IMPORTANTE)
1. **Estar en el directorio del proyecto (ecommerce-fastapi/)**
2. **Construir las imagenes de los microservicios e instalar las dependencias de estos:**
```bash
docker compose build
```
**Esto puede tardar algunos minutos pero solo se realiza una vez**

3. **Ejecutar el sistema:**
```bash
docker compose up -d 
```
**Los servicios estarán disponible en pocos segundos**

4. **Verficar que todos los servicios estén corriendo:**
```bash
docker compose ps
```
**Deberías ver los 5 servicios en estado Up**


5. **Acceder al Frontend:**
Abre el archivo frontend/index.html con Live Server (recomendado) o directamente en:
http://127.0.0.1:5500/frontend/index.html


**Para detener el sistema:**

```bash
docker compose down
```
**Para volver a ejecutar el sistema:**
```bash
docker compose up -d
```
**Ya no se necesita volver a crear las imagenes e instalar las dependencias**

### ¡¡PROBLEMA COMÚN EN LINUX!!:
**Al ejecutar el sistema puede aparecer el siguiente error:**
```bash
error getting credentials - err: exec: "docker-credential-desktop": executable file not found in $PATH
```

**Esto se debe a que Docker usa el archivo:**

```bash
~/.docker/config.json
```
**Si contiene:**
```json
{
  "credsStore": "desktop"
}
```
**intentará usar docker-credential-desktop, que solo existe en Docker Desktop (Windows/Mac) y no en Linux.**

**Solución: Editar el archivo de configuración**
1. **Abre el archivo con tu editor de texto favorito:**
```bash
 ~/.docker/config.json
```

2. **Elimina la siguiente linea:**
```bash
 "credsStore": "desktop"
```
3. **Guarda los cambios y cierra el archivo**

**Después de aplicar la solución, ejecutar nuevamente:**

```bash
docker compose down
docker compose up -d
```

**[!NOTE]**
**Si el error ocurrió durante el primer intento de construcción, ejecutar también:**
```bash
docker compose build
```

**[!NOTE]**
**Este problema no está relacionado con el proyecto, sino con la configuración local de Docker en algunos sistemas Linux.**

## URLs de Documentación (Swagger)

- User Service: http://localhost:8001/docs
- Product Service: http://localhost:8002/docs
- Cart Service: http://localhost:8003/docs
- Order Service: http://localhost:8004/docs
- Shipment Service: http://localhost:8005/docs

## Flujo Recomendado de Prueba

- Registrar un usuario o iniciar sesión
**(Muy importante, el usuario debe crearse con el formato simulando un correo real , por ejemplo: "prueba@test.com", "correo@prueba.com", "juan@cualquiercosa.com". Es importante que tenga este tipo de formato o la pagina arroja error)**
- Explorar el catálogo de productos
- Agregar productos al carrito
- Ir al carrito y pulsar "Generar Orden de Compra"
- Revisar Mis Órdenes y Mis Envíos

## Estructura del proyecto
```
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
```