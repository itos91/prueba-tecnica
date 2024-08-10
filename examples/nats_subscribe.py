import asyncio
import nats


async def main():
    """
        Main function
    """
    async def subscribe_handler(msg):
        """
        Maneja el mensabe subscrito al subject sensor.data

        Args:
            msg (nats.aio.client.Msg): Mensaje subscrito
        """
        subject = msg.subject
        data = msg.data.decode()
        print(
            "Mensaje recibido en el subject '{subject}': {data}".format(
                subject=subject, data=data
            )
        )

    # Nos conectamos al servidor local de NATS
    nc = await nats.connect("nats://localhost:4222")

    # Publicamos el mensaje con el subject dados
    await nc.subscribe("sensor.data", cb=subscribe_handler)

    

if __name__ == '__main__':
    # Obtenemos el bucle de eventos de asyncio
    loop = asyncio.get_event_loop()
    # Ejecutamos la funcion main hasta que se completen
    loop.run_until_complete(main())
    # Ejecutamos el bucle de eventos hasta el infinito
    try:
        loop.run_forever()
    finally:
        loop.close()