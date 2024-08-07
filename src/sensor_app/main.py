import asyncio
import nats
from nats.errors import TimeoutError

async def main():
    nc = await nats.connect("nats://localhost:4222")

    async def message_handler(msg):
        subject = msg.subject

        # Vemos si el subject es para iniciar la recogida de datos del sensor
        if subject == "sensor.start":
            print("Inicio de recogida de datos del sensor")
        elif subject == "sensor.stop":
            print("Parada de recogida de datos del sensor")

    await nc.subscribe("sensor.start", cb=message_handler)
    await nc.subscribe("sensor.stop", cb=message_handler)



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    #asyncio.run(main())

    try:
        loop.run_forever()
    finally:
        loop.close()