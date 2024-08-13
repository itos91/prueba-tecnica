import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.sensor_app.sensor_reader import SensorReader  

def test_read_mockup():
    """
    Test para verificar que SensorReader genera una lista de 64 enteros aleatorios en el rango correcto.
    """
    reader = SensorReader(type_sensor='mockup', min_value=0, max_value=10)
    data = reader.read_sensor()

    # Verifica que se generaron 64 valores
    assert len(data) == 64

    # Verifica que los valores estén dentro del rango especificado
    assert all(0 <= value <= 10 for value in data)

def test_read_real_sensor():
    """
    Test para verificar que SensorReader lanza una excepción para sensores reales.
    """
    reader = SensorReader(type_sensor='real')
    with pytest.raises(NotImplementedError):
        reader.read_sensor()
