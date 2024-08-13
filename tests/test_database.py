import pytest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.sensor_app.db import Database
from datetime import datetime
import mysql.connector

@pytest.fixture
def db():
    """
    Fixture para configurar y limpiar la base de datos antes y después de cada test.
    """
    # URI de la base de datos MySQL para pruebas
    test_db_uri = 'mysql://root:sqlserver@localhost:3307/test_db'

    # Crear la instancia de Database
    db = Database(test_db_uri)

    # Limpiar la tabla antes de cada prueba
    cursor = db.conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS sensor_data")
    db.conn.commit()

    # Volver a crear la tabla para las pruebas
    cursor.execute('''CREATE TABLE IF NOT EXISTS sensor_data
                      (timestamp TEXT, data TEXT)''')
    db.conn.commit()

    yield db

    # Cerrar la conexión al final de las pruebas
    db.conn.close()

def test_connect_db(db):
    """
    Test para verificar que la conexión a la base de datos se realiza correctamente.
    """
    # Verificar que la conexión no es None
    assert db.conn is not None

    # Verificar que la tabla sensor_data fue creada
    cursor = db.conn.cursor()
    cursor.execute("SHOW TABLES LIKE 'sensor_data'")
    result = cursor.fetchone()
    assert result is not None, "La tabla 'sensor_data' no se creó correctamente."

def test_store_data(db):
    """
    Test para verificar que los datos se almacenan correctamente en la base de datos.
    """
    test_data = [10, 20, 30]  # Datos de prueba

    # Almacenar datos usando el método store_data
    db.store_data(test_data)

    # Verificar que los datos se almacenaron en la base de datos
    cursor = db.conn.cursor()
    cursor.execute("SELECT * FROM sensor_data")
    rows = cursor.fetchall()

    # Debería haber un solo registro
    assert len(rows) == 1
    
    # Verificar que los datos almacenados son correctos
    timestamp, data = rows[0]
    assert data == str(test_data), "Los datos almacenados no coinciden con los datos de entrada."

    # Verificar que el timestamp es un valor ISO 8601 válido
    try:
        datetime.fromisoformat(timestamp)
    except ValueError:
        pytest.fail("El timestamp no está en un formato válido ISO 8601.")

