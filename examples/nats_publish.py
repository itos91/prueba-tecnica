import asyncio
import nats
from nats.errors import TimeoutError


async def main():
    nc = await nats.connect("nats://localhost:4222")

    await nc.publish("sensor.stop", b'Hello')

    print(f"Published")
    await nc.flush()
    await nc.drain()

    

if __name__ == '__main__':
    asyncio.run(main())