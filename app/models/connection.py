import os

import psycopg2
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

# Datos de conexión
HOST = os.getenv("DATABASE_HOST")
PORT = os.getenv("DATABASE_PORT")
DATABASE = os.getenv("DATABASE_NAME")
USER = os.getenv("DATABASE_USER")
PASSWORD = os.getenv("DATABASE_PASSWORD")


class Connection:
    conn = None

    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                user=USER,
                password=PASSWORD,
                host=HOST,
                port=PORT,
                dbname=DATABASE,
                sslmode="require",
            )
            print("Conection successful!")
        except psycopg2.OperationalError as err:
            print("ERROR BD::", err)
            self.conn.close()

    def read_product(self):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT * FROM "tbl_productos" 
            """
            )
            data = cur.fetchall()
            return data

    def read_product_one(self, id):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT * FROM tbl_productos WHERE id = %s
            """,
                (id,),
            )
            data = cur.fetchone()
            return data

    def update_product(self, id: int, data):
        try:
            with self.conn.cursor() as cur:
                # ✅ Construir la consulta dinámicamente con los campos enviados
                campos = ", ".join([f"{key} = %({key})s" for key in data.keys()])
                sql = f"UPDATE tbl_productos SET {campos} WHERE id = %(id)s"
                data["id"] = id  # Agregar el id a los datos

                cur.execute(sql, data)
                self.conn.commit()
                if cur.rowcount == 0:
                    return {"message": "No se encontró el producto con ese ID"}
                return {"message": "Producto actualizado correctamente"}

        except Exception as e:
            self.conn.rollback()
            raise HTTPException(
                status_code=500, detail=f"❌ Error en la actualización: {str(e)}"
            )

    def create_product(self, data):
        try:
            with self.conn.cursor() as cur:
                # Verificar si ya existe el barcode en la BD
                cur.execute(
                    "SELECT COUNT(*) FROM tbl_productos WHERE barcode = %(barcode)s",
                    {"barcode": data["barcode"]},
                )
                existe = cur.fetchone()[0]

                if existe > 0:
                    return {"error": "Codigo ya existe"}

                cur.execute(
                    """
                    INSERT INTO "tbl_productos"(barcode, descripcion, informacion, imagen, moneda, valor_venta, impuesto, precio_venta, incremento, estado, id_unidad, id_unidad_contenido, id_categoria, id_subcategoria) VALUES(%(barcode)s,%(descripcion)s,%(informacion)s,%(imagen)s,%(moneda)s,%(valor_venta)s,%(impuesto)s,%(precio_venta)s,%(incremento)s,%(estado)s,%(id_unidad)s,%(id_unidad_contenido)s,%(id_categoria)s,%(id_subcategoria)s)
                """,
                    data,
                )
                self.conn.commit()
                return {"message": "Producto agregado exitosamente"}

        except Exception as e:
            self.conn.rollback()
            return {"error": str(e)}

    def read_categoria(self):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT * FROM "tbl_categorias" 
            """
            )
            data = cur.fetchall()
            return data

    def update_categoria(self, id: int, data):
        try:
            with self.conn.cursor() as cur:
                # ✅ Construir la consulta dinámicamente con los campos enviados
                campos = ", ".join([f"{key} = %({key})s" for key in data.keys()])
                sql = f"UPDATE tbl_categorias SET {campos} WHERE id = %(id)s"
                data["id"] = id  # Agregar el id a los datos

                cur.execute(sql, data)
                self.conn.commit()
                if cur.rowcount == 0:
                    return {"message": "No se encontró la categoria con ese ID"}
                return {"message": "Categoria actualizado correctamente"}

        except Exception as e:
            self.conn.rollback()
            raise HTTPException(
                status_code=500, detail=f"❌ Error en la actualización: {str(e)}"
            )

    def create_categoria(self, data):
        try:
            with self.conn.cursor() as cur:
                if data["indetity"] == "C":
                    cur.execute(
                        """
                        INSERT INTO "tbl_categorias"(indetity, descripcion, imagen, estado) VALUES(%(indetity)s,%(descripcion)s,%(imagen)s,%(estado)s) RETURNING id
                    """,
                        data,
                    )
                    nuevo_id = cur.fetchone()[0]  # ✅ Captura el ID generado
                    cur.execute(
                        """
                        UPDATE tbl_categorias SET id_categoria = %s WHERE id = %s
                    """,
                        (nuevo_id, nuevo_id),
                    )
                    self.conn.commit()

                elif data["indetity"] == "S":
                    cur.execute(
                        """
                        INSERT INTO tbl_categorias (indetity, descripcion, imagen, estado, id_categoria)
                        VALUES (%(indetity)s, %(descripcion)s, %(imagen)s, %(estado)s, %(id_categoria)s)
                    """,
                        data,
                    )
                    self.conn.commit()

                return {"message": "Categoria agregado exitosamente"}

        except Exception as e:
            self.conn.rollback()
            return {"error": str(e)}

    def read_und(self):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT * FROM "tbl_unidades" 
            """
            )
            data = cur.fetchall()
            return data

    def read_und_cont(self):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT * FROM "tbl_unidad_contenidos" 
            """
            )
            data = cur.fetchall()
            return data

    def __def__(self):
        self.conn.close()
