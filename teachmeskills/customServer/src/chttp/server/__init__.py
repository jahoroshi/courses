import asyncio
from datetime import datetime

from chttp.routers import Router
from chttp.services import catch_exception
from chttp.handlers import RequestHandler
import time




class Controller(asyncio.Protocol):
    def __init__(self, router):
        self._transport = None
        self.router = router

    def connection_made(self, transport):
        self._transport = transport

    def _handle_resp(self, task: asyncio.Task):
        try:
            body = task.result()
        except Exception as e:
            print('--Exception: ', e)
        else:
            if body:
                RESP = """HTTP/1.1 200 OK\r
                                Date: {0}\r
                                Server: Custom http\r
                                Last-Modified: {0}\r
                                Content-Length: {1}\r
                                Content-Type: text/html\r
                                Connection: Closed\r\n\r
                                {2}""".format(datetime.now().strftime("%c"), len(body), body)

            else:
                RESP = (
                    "HTTP/1.1 302 Found\r\n"
                    "Location: http://127.0.0.1:8000/home/\r\n"
                    "Content-Length: 0\r\n"
                    "Connection: close\r\n"
                    "\r\n"
                )

            self._transport.write(RESP.encode("utf-8"))
        self._transport.close()

    @catch_exception
    async def _home_handler(self,  message: str):
        return await self.router.handle_request(message)

    def data_received(self, data):
        message = data.decode("utf-8")
        asyncio.create_task(self._home_handler(message)).add_done_callback(self._handle_resp)


@catch_exception
async def serve():
    loop = asyncio.get_running_loop()
    request_handler = RequestHandler()
    router = Router(request_handler)
    server = await loop.create_server(lambda: Controller(router), "127.0.0.1", 8000)
    async with server:
        print('[ Server start ]')
        await server.serve_forever()
