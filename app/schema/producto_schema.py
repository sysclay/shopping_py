from typing import Optional

from pydantic import BaseModel


class ProductoSchemaUdate(BaseModel):
    barcode: Optional[str] = None
    descripcion: Optional[str] = None
    informacion: Optional[str] = None
    imagen: Optional[bytes] = None
    moneda: Optional[str] = None
    valor_venta: Optional[float] = None
    impuesto: Optional[float] = None
    precio_venta: Optional[float] = None
    incremento: Optional[float] = None
    estado: Optional[str] = None
    id_unidad: Optional[int] = None
    id_unidad_contenido: Optional[int] = None
    id_categoria: Optional[int] = None
    id_subcategoria: Optional[int] = None


class ProductoSchema(BaseModel):
    id: Optional[int] = None
    barcode: str
    descripcion: str
    informacion: str
    imagen: Optional[bytes] = None
    moneda: str
    valor_venta: float
    impuesto: float
    precio_venta: float
    incremento: float
    estado: str
    id_unidad: int
    id_unidad_contenido: int
    id_categoria: int
    id_subcategoria: int
