from pydantic import BaseModel, Field
from typing import Optional

class ClienteBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100, example="Nahuel Aciar")
    email: str = Field(..., pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$", example="agustinahuelaciar@gmail.com")
    telefono: Optional[str] = Field(None, example="+5491123456789")
    activo: bool = True
    tipo: str = Field(..., pattern="^(Regular|Premium|VIP)$", example="Regular")

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[str] = Field(None, pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    telefono: Optional[str] = None
    activo: Optional[bool] = None
    tipo: Optional[str] = Field(None, pattern="^(Regular|Premium|VIP)$")

class ClienteRead(ClienteBase):
    id: int

class ClienteRecomendacion(BaseModel):
    id: int
    tipo: str
    beneficio: str
    recomendacion: str
