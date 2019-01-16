from wsstat.clients import WebsocketTestingClient

import asyncio
import datetime
import random
import websockets
import sys

if sys.version_info < (3, 4, 4):
    asyncio.ensure_future = getattr(asyncio, 'async')

@asyncio.coroutine
def echo_time(websocket, path):
    while True:
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        try:
            yield from websocket.send(now)
            yield from asyncio.sleep(random.random() * 3)
        except:
            pass

class DemoClient(WebsocketTestingClient):
    def __init__(self, websocket_url, **kwargs):
        super().__init__('ws://127.0.0.1:65432', **kwargs)

    def setup_tasks(self):
        super().setup_tasks()
        start_server = websockets.serve(echo_time, '127.0.0.1', 65432)
        asyncio.ensure_future(start_server, loop=self.loop)
