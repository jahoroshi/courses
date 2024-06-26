import time
from datetime import datetime

from chttp.services import catch_exception
from .urls import urlpatterns


class Router():
    def __init__(self, request_handler):
        self.request = request_handler

    @catch_exception
    async def handle_request(self, message):
        if message:
            self.request.parse(message)
        else:
            return 'No data'

        view = urlpatterns.get(self.request.path)

        if view:
            return await view(self.request)
        else:
            return None
