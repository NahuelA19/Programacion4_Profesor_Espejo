from fastapi import FastAPI
from app.modules.producto.routers import router as producto_router
from app.modules.categoria.routers import router as categoria_router
from app.modules.clientes.routers import router as clientes_router

def create_app() -> FastAPI:
    app = FastAPI(
        title="Trabajo Practico Integrador - Unidad 1",
       
    )
    
    app.include_router(producto_router)
    app.include_router(categoria_router)
    app.include_router(clientes_router)
    
    return app

app = create_app()
