import random

class SensorReader:
    """
    Lee datos del sensor en un rango de 64 valores de enteros de 16 bits
    """
    def __init__(self, min_value:int = 0, max_value:int = 65536, type_sensor:str = "mockup") -> None:
        """
        Inicializador de clase

        Args:
            min_value (int, optional): Minimo valor del sensor mockup. Defaults to 0.
            max_value (int, optional): _description_. Defaults to 65536.
            type_sensor (str, optional): _description_. Defaults to "mockup".
        """
        self.min_value = min_value
        self.max_value = max_value
        self.type_sensor = type_sensor

    def read_sensor(self):
        # Comprueba si el sensor es de tipo mockup
        if self.type_sensor == "mockup":
            return [random.randint(self.min_value, self.max_value) for _ in range(64)]
        else:
            raise NotImplementedError("Sensor real no esta implementado aun")