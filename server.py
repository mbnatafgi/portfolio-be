import asyncio
from websockets import serve


async def connect(websocket, path):

    async for message in websocket:

        await websocket.send(message)


start_server = serve(connect, 'localhost', 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
