import argparse
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.sensor_app.db import Database  

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Prueba de insercion de datos en base de datos")

    parser.add_argument("--db_uri", type=str, required=True, help="URI de conexión con la base de datos SQL")

    args = parser.parse_args()

    db_conn = Database(args.db_uri)

    data = "[1,2,3,4,5,6]"

    db_conn.store_data(data)
    
    print("Data insertada")