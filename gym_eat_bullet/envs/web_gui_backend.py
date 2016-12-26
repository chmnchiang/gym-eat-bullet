import asyncio
import threading
import aiohttp
from aiohttp import web
from aiohttp_index import IndexMiddleware
from typing import Tuple
from concurrent.futures import CancelledError
import json
import os

try:
    from .base_env import BaseEnv
except SystemError:
    from base_env import BaseEnv

class WebGUIBackend(BaseEnv):

    def __init__(self,
                 frame_size: Tuple[int, int],
                 action_n: int,
                 *,
                 max_step: int = 100,
                 fps: int = 20) -> None:
        '''
        Usage:
        self.super().__init__(actions, grid_size, block_size,
                              gui_amp, FPS)
        '''
        super().__init__(frame_size, action_n, max_step=max_step)
        self.fps = fps
        self.loop = asyncio.get_event_loop()
        self.app = None
        self.server_thread = None

        self.gui_start()

    # Tk GUI setup
    def gui_start(self) -> None:
        self.server_thread = threading.Thread(target=self._server_handler)
        self.server_thread.start()

    def _server_handler(self):
        loop = self.loop
        asyncio.set_event_loop(loop)
        app = self.app = web.Application(loop=self.loop,
                                         middlewares=[IndexMiddleware()])

        async def websocket_handler(request):
            ws = web.WebSocketResponse()
            await ws.prepare(request)
            while not ws.closed:
                ws.send_str(json.dumps(self.get_bitmap().tolist()))
                try:
                    await asyncio.sleep(1 / self.fps)
                except CancelledError:
                    break

            return ws
        
        app.router.add_get('/ws', websocket_handler)
        static_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static')
        app.router.add_static('/', static_path)
        handler = app.make_handler()
        print('Server start at 0.0.0.0:60000')
        coro = loop.create_server(handler, '0.0.0.0', 60000)
        server = loop.run_until_complete(coro)
        loop.run_forever()

    def end(self):
        self.loop.stop()

if __name__ == '__main__':
    gui = WebGUIBackend((50, 50), 4)
