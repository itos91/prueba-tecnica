import pytest
import asyncio
import nats
from unittest.mock import AsyncMock, patch, MagicMock
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.sensor_app.main import NatsHandler
from src.sensor_app.sensor_reader import SensorReader
from src.sensor_app.db import Database

@pytest.mark.asyncio
async def test_start_sensor():
    """
    Test para verificar que el sensor comienza a capturar datos correctamente.
    """
    args = MagicMock(freq=1, min_value=0, max_value=100, sensor='mockup', db_uri='mysql://root:sqlserver@localhost:3307/test_db')
    with patch('src.sensor_app.main.SensorReader') as MockSensorReader, \
         patch('src.sensor_app.main.Database') as MockDatabase, \
         patch('src.sensor_app.main.NATS.connect', new_callable=AsyncMock) as mock_nats_connect, \
         patch('src.sensor_app.main.NATS.subscribe', new_callable=AsyncMock) as mock_nats_subscribe:
                
        # Instancia del NatsHandler
        handler = NatsHandler(args)

        # Simular la conexión llamando a la función start()
        await handler.start()

        # Verificar que la conexión se realizó correctamente
        mock_nats_connect.assert_called_once()

        # Simular la suscripción y llamada al callback de "sensor.start"
        msg = MagicMock()
        await handler.start_sensor(msg)  # Llamar directamente al callback

        # Verificar que el sensor comenzó a capturar datos
        assert handler.sensor_state is True
        

@pytest.mark.asyncio
async def test_stop_sensor():
    """
    Test para verificar que el sensor detiene la captura de datos correctamente.
    """
    args = MagicMock(freq=1, min_value=0, max_value=100, sensor='mockup', db_uri='mysql://root:sqlserver@localhost:3307/test_db')
    with patch.object(NatsHandler, 'stop_sensor', new_callable=AsyncMock) as mock_stop_sensor:
                
        handler = NatsHandler(args)
        await handler.start()
        await handler.stop_sensor(None)

        assert handler.sensor_state is False
        mock_stop_sensor.assert_called_once()

@pytest.mark.asyncio
async def test_run():
    """
    Test para verificar que los datos del sensor son leídos, publicados, y almacenados en la base de datos.
    """
    args = MagicMock(freq=1, min_value=0, max_value=100, sensor='mockup', db_uri='mysql://root:sqlserver@localhost:3307/test_db')
    
    with patch('src.sensor_app.main.SensorReader') as MockSensorReader, \
         patch('src.sensor_app.main.Database') as MockDatabase, \
         patch('src.sensor_app.main.NATS.connect', new_callable=AsyncMock) as mock_nats_connect, \
         patch('src.sensor_app.main.NATS.subscribe', new_callable=AsyncMock) as mock_nats_subscribe, \
         patch('src.sensor_app.main.NATS.publish', new_callable=AsyncMock) as mock_nats_publish, \
         patch('asyncio.sleep', new_callable=AsyncMock) as mock_sleep:

        # Instancia del NatsHandler
        handler = NatsHandler(args)

        # Simular la conexión llamando a la función start()
        await handler.start()

        # Verificar que la conexión se realizó correctamente
        mock_nats_connect.assert_called_once()

        # Simular que el sensor está en estado activo
        handler.sensor_state = True

        # Configurar `mock_sleep` para hacer que el bucle solo se ejecute una vez
        mock_sleep.side_effect = [None, asyncio.CancelledError()]

        # Ejecutar la función run
        try:
            await handler.run()
        except asyncio.CancelledError:
            pass

        # Verificar que se publicaron datos en NATS
        mock_nats_publish.assert_called_with(
            subject="sensor.data", 
            payload=bytes(str(MockSensorReader.return_value.read_sensor.return_value), 'utf-8')
        )

        # Verificar que los datos también se almacenaron en la base de datos
        handler.db_conn.store_data.assert_called()