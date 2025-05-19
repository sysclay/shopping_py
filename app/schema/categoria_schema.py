from typing import Optional

from pydantic import BaseModel


class CategoriaSchemaUdate(BaseModel):
    indetity: Optional[str] = None
    descripcion: Optional[str] = None
    imagen: Optional[bytes] = None
    estado: Optional[str] = None
    id_categoria: Optional[int] = None


class CategoriaSchema(BaseModel):
    id: Optional[int] = None
    indetity: str
    descripcion: str
    imagen: Optional[bytes] = None
    estado: str
    id_categoria: Optional[int] = None
