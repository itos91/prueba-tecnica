import logging
import os
import asyncio
from mysql.connector import DatabaseError

# Configuración logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def handle_exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except asyncio.CancelledError as ce:
            logger.error(f"Exited! Error {ce}.")
            logger.error(f"Exiting...")
            os._exit(1)
        except DatabaseError as de:
            logger.error(f"Error: {de}")
            logger.error(f"Exiting...")
            os._exit(1)
            
        except Exception as ex:
            exception_report = {
                "event": {
                    "method": func.__name__,
                    "message": str(ex),
                    "args": args,
                    "kwargs": kwargs
                }
            }
            logger.error('exception_report ', exception_report)
            os._exit(1)
    return wrapper