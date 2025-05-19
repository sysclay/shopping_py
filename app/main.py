import base64

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models.connection import Connection
from schema.categoria_schema import CategoriaSchema, CategoriaSchemaUdate
from schema.producto_schema import ProductoSchema, ProductoSchemaUdate

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 🔄 Permitir React/Next.js
    allow_credentials=True,
    allow_methods=["*"],  # 🔄 Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # 🔄 Permitir todos los headers
)

conn = Connection()


@app.get("/")
def index():
    # conn
    return {"message": "Hola, developers"}


@app.get("/api/product")
def listProduct():
    items = []
    for data in conn.read_product():
        dictionary = {}
        dictionary["id"] = data[0]
        dictionary["barcode"] = data[1]
        dictionary["descripcion"] = data[2]
        dictionary["informacion"] = data[3]
        dictionary["imagen"] = (
            base64.b64encode(data[4]).decode("utf-8") if data[4] else None,
        )
        dictionary["moneda"] = data[5]
        dictionary["valor_venta"] = data[6]
        dictionary["impuesto"] = data[7]
        dictionary["precio_venta"] = data[8]
        dictionary["incremento"] = data[9]
        dictionary["estado"] = data[10]
        dictionary["id_unidad"] = data[11]
        dictionary["id_unidad_contenido"] = data[12]
        dictionary["id_categoria"] = data[13]
        dictionary["id_subcategoria"] = data[14]
        items.append(dictionary)
    return items


@app.get("/api/product/{id}")
def listProductOne(id: str):
    dictionary = {}
    data = conn.read_product_one(id)
    dictionary["id"] = data[0]
    dictionary["barcode"] = data[1]
    dictionary["descripcion"] = data[2]
    dictionary["informacion"] = data[3]
    dictionary["imagen"] = data[4]
    dictionary["moneda"] = data[5]
    dictionary["valor_venta"] = data[6]
    dictionary["impuesto"] = data[7]
    dictionary["precio_venta"] = data[8]
    dictionary["incremento"] = data[9]
    dictionary["estado"] = data[10]
    dictionary["id_unidad"] = data[11]
    dictionary["id_unidad_contenido"] = data[12]
    dictionary["id_categoria"] = data[13]
    dictionary["id_subcategoria"] = data[14]
    return dictionary


@app.put("/api/product/update/{id}")
def updateProduct(id: int, product_data: ProductoSchemaUdate):
    data = product_data.model_dump(exclude_none=True)
    if not data:
        raise HTTPException(
            status_code=400, detail="❌ No se enviaron datos para actualizar"
        )

    if (
        "imagen" in data
        and isinstance(data["imagen"], str)
        and data["imagen"].startswith("data:image")
    ):
        base64_str = data["imagen"].split(",")[1]
        data["imagen"] = base64.b64decode(base64_str)

    return conn.update_product(id, data)


@app.post("/api/product")
def insertProduct(product_data: ProductoSchema):
    data = product_data.model_dump()
    # ✅ Decodificar imagen en Base64 si existe
    if (
        "imagen" in data
        and isinstance(data["imagen"], str)
        and data["imagen"].startswith("data:image")
    ):
        base64_str = data["imagen"].split(",")[
            1
        ]  # ✅ Quita el prefijo `data:image/...`
        data["imagen"] = base64.b64decode(base64_str)  # ✅ Convierte Base64 a `BYTEA`
    resultado = conn.create_product(data)
    resultado_dict = {}
    if resultado.get("message"):
        resultado_dict["message"] = resultado.get("message")
    if resultado.get("error"):
        resultado_dict["error"] = resultado.get("error")
    return resultado_dict


@app.get("/api/categoria")
def listCategoria():
    items = []
    for data in conn.read_categoria():
        dictionary = {}
        dictionary["id"] = data[0]
        dictionary["indetity"] = data[1]
        dictionary["descripcion"] = data[2]
        dictionary["imagen"] = (
            base64.b64encode(data[3]).decode("utf-8") if data[3] else None,
        )
        dictionary["estado"] = data[4]
        dictionary["id_categoria"] = data[5]
        items.append(dictionary)
    return items


@app.put("/api/categoria/update/{id}")
def updateCategoria(id: int, cat_data: CategoriaSchemaUdate):
    data = cat_data.model_dump(exclude_none=True)
    if not data:
        raise HTTPException(
            status_code=400, detail="❌ No se enviaron datos para actualizar"
        )

    if (
        "imagen" in data
        and isinstance(data["imagen"], str)
        and data["imagen"].startswith("data:image")
    ):
        base64_str = data["imagen"].split(",")[1]
        data["imagen"] = base64.b64decode(base64_str)

    return conn.update_categoria(id, data)


@app.post("/api/categoria")
def insertCate(cat_data: CategoriaSchema):
    data = cat_data.model_dump()
    # ✅ Decodificar imagen en Base64 si existe
    if (
        "imagen" in data
        and isinstance(data["imagen"], str)
        and data["imagen"].startswith("data:image")
    ):
        base64_str = data["imagen"].split(",")[1]
        data["imagen"] = base64.b64decode(base64_str)
    resultado = conn.create_categoria(data)
    resultado_dict = {}
    if resultado.get("message"):
        resultado_dict["message"] = resultado.get("message")
    if resultado.get("error"):
        resultado_dict["error"] = resultado.get("error")
    return resultado_dict


@app.get("/api/und")
def listUnd():
    items = []
    for data in conn.read_und():
        dictionary = {}
        dictionary["id"] = data[0]
        dictionary["unidad"] = data[1]
        dictionary["code"] = data[2]
        items.append(dictionary)
    return items


@app.get("/api/und_cont")
def listUndCont():
    items = []
    for data in conn.read_und_cont():
        dictionary = {}
        dictionary["id"] = data[0]
        dictionary["contenido"] = data[1]
        dictionary["id_unidad"] = data[2]
        items.append(dictionary)
    return items
