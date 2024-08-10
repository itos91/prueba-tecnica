import asyncio
import argparse
from nats.aio.client import Client as NATS
from sensor_reader import SensorReader

class NatsHandler:
    """
    Clase que maneja los mensajes NATS
    """
    def __init__(self, args) -> None:
        self.sensor_state = False
        self.nc = NATS()
        self.freq = args.freq
        self.sensor_reader = SensorReader(args.min_value, args.max_value, args.sensor)

    async def start(self):
        """
        Conecta con el servidor NATS y se suscribe a los subjects de inicio y parada del sensor
        """
        # Conectamos con servidor local NATS
        await self.nc.connect("nats://localhost:4222")
        # Nos subscribimos a los subjets "sensor.start" y "sensor.stop"
        await self.nc.subscribe("sensor.start", cb=self.start_sensor)
        await self.nc.subscribe("sensor.stop", cb=self.stop_sensor)

    async def start_sensor(self, msg):
        """ 
        Callback para iniciar la captura de datos del sensor.

        Args:
            msg (nats.aio.client.Msg): Mensaje subscrito
        """
        self.sensor_state = True
        print("Inicio de recogida de datos del sensor")

    async def stop_sensor(self, msg):
        """ 
        Callback para parar la captura de datos del sensor.

        Args:
            msg (nats.aio.client.Msg): Mensaje subscrito
        """
        self.sensor_state = False
        print("Parada de recogida de datos del sensor")

    async def run(self):
        """
        Bucle infinito para realizar la lectura del sensor
        """
        while True:
            if self.sensor_state:
                # Empezamos a capturar datos de sensores
                print("Captura de datos sensor")
                data = self.sensor_reader.read_sensor()
                # Publicamos datos
                await self.nc.publish(
                    subject="sensor.data", 
                    payload=str(data).encode()
                )
                # Dejamos n segundos entre captura y captura
                await asyncio.sleep(self.freq)
            else:
                # Dejamos 1 segunda para que no se quede parado en bucle infinito
                await asyncio.sleep(1)
        


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Aplicación de captura de datos del sensor")
    parser.add_argument("--sensor", type=str, required=True, choices=["mockup", "real"])
    parser.add_argument("--freq", type=int, required=True, help="Frecuencia de lectura del sensor en segundos")
    parser.add_argument("--min_value", type=int, required=True, help="Valor mínimo generado por el sensor mockup")
    parser.add_argument("--max_value", type=int, required=True, help="Valor máximo generado por el sensor mockup")

    args = parser.parse_args()

    #Creamos instancia de la clase NatsHandler
    app = NatsHandler(args)

    # Obtenemos el bucle de eventos de asyncio
    loop = asyncio.get_event_loop()

    # Ejecutamos las funciones start y run hasta que se completen
    asyncio.ensure_future(app.start())
    asyncio.ensure_future(app.run())

    # Ejecutamos el bucle de eventos hasta el infinito
    try:
        loop.run_forever()
    finally:
        loop.close()
