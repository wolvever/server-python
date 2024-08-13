
import httpx
import logging
import tenacity

from server_python.client.setting import Retry


class RetryTransport(httpx.BaseTransport):
    def __init__(self, transport: httpx.BaseTransport, retry: Retry, logger: logging.Logger = None):
        if retry is None:
            raise ValueError('Retry must be specified')
        
        self.transport = transport
        self.logger = logger
        self.retry = retry

        if not retry.is_random and not retry.is_exponential:
            wait = tenacity.wait_fixed(retry.wait_fix)
        elif retry.is_random:
            wait = tenacity.wait_random(min=retry.wait_random_min, max=retry.wait_random_max)
        else:
            wait = tenacity.wait_exponential(min=retry.wait_exponential_min, max=retry.wait_exponential_max)

        retry_decorator = tenacity.retry(wait=wait, stop=tenacity.stop_after_attempt(retry.attempts))
        self.retry_fn = retry_decorator(self.transport.handle_request)
    
    def handle_request(self, request: httpx.Request) -> httpx.Response:
        return self.retry_fn(request)