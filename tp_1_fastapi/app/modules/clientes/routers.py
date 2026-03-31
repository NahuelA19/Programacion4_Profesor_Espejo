from fastapi import APIRouter, HTTPException, Path, Query, status
from typing import List, Optional
from . import schemas, services

router = APIRouter(prefix="/clientes", tags=["Clientes"])


# ---------------------------------------------------------
# ALTA DE CLIENTE
# Método: POST | Endpoint: /clientes/ | Estado: 201 Created
# ---------------------------------------------------------
@router.post(
    "/", response_model=schemas.ClienteRead, status_code=status.HTTP_201_CREATED
)
def alta_cliente(cliente: schemas.ClienteCreate):
    return services.crear(cliente)


# ---------------------------------------------------------
# LISTAR CLIENTES CON FILTROS
# Método: GET | Endpoint: /clientes/ | Estado: 200 OK
# ---------------------------------------------------------
@router.get(
    "/", response_model=List[schemas.ClienteRead], status_code=status.HTTP_200_OK
)
def listar_clientes(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=50),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    tipo: Optional[str] = Query(None, description="Filtrar por tipo (Regular, Premium, VIP)")
):
    return services.obtener_todos(skip, limit, activo, tipo)


# ---------------------------------------------------------
# DETALLE DE CLIENTE
# Método: GET | Endpoint: /clientes/{id} | Estado: 200 OK
# ---------------------------------------------------------
@router.get(
    "/{id}", response_model=schemas.ClienteRead, status_code=status.HTTP_200_OK
)
def detalle_cliente(id: int = Path(..., gt=0)):
    cliente = services.obtener_por_id(id)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado"
        )
    return cliente


# ---------------------------------------------------------
# ACTUALIZACIÓN TOTAL DE CLIENTE
# Método: PUT | Endpoint: /clientes/{id} | Estado: 200 OK
# ---------------------------------------------------------
@router.put(
    "/{id}", response_model=schemas.ClienteRead, status_code=status.HTTP_200_OK
)
def actualizar_cliente(cliente: schemas.ClienteCreate, id: int = Path(..., gt=0)):
    actualizado = services.actualizar_total(id, cliente)
    if not actualizado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado"
        )
    return actualizado


# ---------------------------------------------------------
# BORRADO LÓGICO
# Método: PUT | Endpoint: /clientes/{id}/desactivar | Estado: 200 OK
# ---------------------------------------------------------
@router.put(
    "/{id}/desactivar",
    response_model=schemas.ClienteRead,
    status_code=status.HTTP_200_OK,
)
def borrado_logico(id: int = Path(..., gt=0)):
    desactivado = services.desactivar(id)
    if not desactivado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado"
        )
    return desactivado


# ---------------------------------------------------------
# CLASIFICACIÓN DE CLIENTE (Regla de negocio)
# Método: GET | Endpoint: /clientes/{id}/clasificacion | Estado: 200 OK
# ---------------------------------------------------------
@router.get(
    "/{id}/clasificacion",
    response_model=schemas.ClienteRecomendacion,
    status_code=status.HTTP_200_OK,
)
def clasificacion_cliente(id: int = Path(..., gt=0)):
    resultado = services.clasificar_cliente(id)
    if not resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado"
        )
    return resultado
