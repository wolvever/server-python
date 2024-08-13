import os
import httpx

web_runtime = os.environ.get("WEB_RUNTIME", "flask")
if web_runtime == "flask":
     from flask import request as runtime_context
elif web_runtime == "fastapi":
     from fastapi import Request as runtime_context



class BceRequestIdTransport(httpx.BaseTransport):
    from flask import request

    def __init__(self, transport: httpx.BaseTransport):
            self.transport = transport
           
    def handle_request(self, httpx_req: httpx.Request) -> httpx.Response:
        bce_request_id = request.headers.get("X-Bce-Request-Id")
        httpx_req.headers["X-Bce-Request-Id"] = bce_request_id
        return self.transport.handle_request(httpx_req)