from typing import List, Optional
from fastapi import HTTPException, status
from .schemas import ClienteCreate, ClienteRead, ClienteUpdate

db_clientes: List[ClienteRead] = []
id_counter = 1

def _email_existe(email: str, exclude_id: Optional[int] = None) -> bool:
    for c in db_clientes:
        if c.email == email:
            if exclude_id and c.id == exclude_id:
                continue
            return True
    return False

def crear(data: ClienteCreate) -> ClienteRead:
    global id_counter
    if _email_existe(data.email):
         raise HTTPException(
             status_code=status.HTTP_400_BAD_REQUEST, 
             detail="El email ya está registrado"
         )
    
    nuevo = ClienteRead(id=id_counter, **data.model_dump())
    db_clientes.append(nuevo)
    id_counter += 1
    return nuevo

def obtener_todos(skip: int, limit: int, activo: Optional[bool] = None, tipo: Optional[str] = None) -> List[ClienteRead]:
    resultado = db_clientes
    if activo is not None:
        resultado = [c for c in resultado if c.activo == activo]
    if tipo is not None:
        resultado = [c for c in resultado if c.tipo == tipo]
    
    return resultado[skip : skip + limit]

def obtener_por_id(id: int) -> Optional[ClienteRead]:
    for c in db_clientes:
        if c.id == id:
            return c
    return None

def actualizar_total(id: int, data: ClienteCreate) -> Optional[ClienteRead]:
    if _email_existe(data.email, exclude_id=id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="El email ya está registrado por otro cliente"
        )
    
    for index, c in enumerate(db_clientes):
        if c.id == id:
            cliente_actualizado = ClienteRead(id=id, **data.model_dump())
            db_clientes[index] = cliente_actualizado
            return cliente_actualizado
    return None

def desactivar(id: int) -> Optional[ClienteRead]:
    for index, c in enumerate(db_clientes):
        if c.id == id:
            c_dict = c.model_dump()
            c_dict["activo"] = False
            cliente_actualizado = ClienteRead(**c_dict)
            db_clientes[index] = cliente_actualizado
            return cliente_actualizado
    return None

def clasificar_cliente(id: int) -> Optional[dict]:
    cliente = obtener_por_id(id)
    if not cliente:
        return None
        
    recomendaciones = {
        "Regular": "Ofrecer upgrade a plan Premium con descuento del 10%.",
        "Premium": "Ofrecer atención prioritaria y promociones exclusivas.",
        "VIP": "Asignar ejecutivo de cuenta personal y acceso a pre-ventas."
    }
    
    beneficios = {
        "Regular": "Acceso estándar.",
        "Premium": "Envío gratis.",
        "VIP": "Envío gratis express y soporte 24/7."
    }
    
    return {
        "id": cliente.id,
        "tipo": cliente.tipo,
        "beneficio": beneficios.get(cliente.tipo, "Sin definir"),
        "recomendacion": recomendaciones.get(cliente.tipo, "Sin definir")
    }
