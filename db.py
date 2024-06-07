import sqlite3

def get_db():
    "Conecta a la base de datos SQLite y devuelve el objeto de conexión."
    try:
        conn = sqlite3.connect("database/db-libros.db")
        print("Conexión a la base de datos establecida exitosamente.")
        return conn
    except Exception as e:
        print(f"No se pudo conectar a la base de datos: {e}")
    raise e

def close_db(db):
    "Cierra la conexión a la base de datos."
    db.close()
