import mysql.connector
import urllib.parse
from datetime import datetime

class Database:
    """
    Clase para la gestión de la base de datos.
    """

    def __init__(self, uri):
        """
        Inicialización de la clase Database

        Args:
            uri (str): URI de conexión con la base de datos.
        """
        self.conn = self.connect_db(uri)

    def connect_db(self, uri:str):
        """
        Conecta a la base de datos por la URI.

        Args:
            uri (str): URI de conexión con la base de datos.

        Returns:
            mysql.connector: Objeto de conexión a la base de datos.
        """

        # Parsear la URI para extraer los componentes
        parsed_uri = urllib.parse.urlparse(uri)
        
        # Extraer la información necesaria para la conexión
        user = parsed_uri.username
        password = parsed_uri.password
        host = parsed_uri.hostname
        port = parsed_uri.port
        # Eliminar el primer "/" de la ruta
        database = parsed_uri.path[1:]
        
        connection = mysql.connector.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            database=database
        )
        
        return connection

    def store_data(self, data):
        """
        Almacena datos en la base de datos.

        Args:
            data (list): Datos capturados del sensor.
        """
        cursor = self.conn.cursor()

        insert_command = 'INSERT INTO sensor_data (timestamp, data) VALUES (%s, %s)'             
        insert_data = (datetime.now().isoformat(), str(data))
        
        cursor.execute(insert_command, insert_data)
        self.conn.commit()

