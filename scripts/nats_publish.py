import asyncio
import nats
import argparse


async def main(subject:str, message:str="Hello"):
    # Nos conectamos al servidor local de NATS
    nc = await nats.connect("nats://localhost:4222")

    # Publicamos el mensaje con el subject dados
    await nc.publish(subject, message.encode('utf-8'))

    print(f"Published")
    await nc.flush()
    await nc.drain()

    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Enviar mensajes a un servidor NATS")
    parser.add_argument('--subject', type=str, required=True, help="Subject del mensaje")
    parser.add_argument('--message', type=str, required=False, help="Mensaje a enviar")

    args = parser.parse_args()

    # Ejecutamos la funcion main
    asyncio.run(main(subject=args.subject, message=args.message))