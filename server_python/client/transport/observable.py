
import httpx
import logging

from server_python.client.setting import Observable


class ObservableTransport(httpx.BaseTransport):
    def __init__(self, transport: httpx.BaseTransport, observable: Observable, logger: logging.Logger = None):
        self.transport = transport
        self.logger = logger
        # TODO: Initialize logger, tracer and stats
        self.tracer = None
        self.stats = None

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        # TODO: Implement logging, tracing and stats

        return self.transport.handle_request(request)