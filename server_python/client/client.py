import logging
import httpx
import server_python.client.auth as auth

from typing import Dict, Union
from server_python.client.setting import Auth, Timeout, Retry, Observable, ClientSetting
from server_python.client.transport.retry import RetryTransport
from server_python.client.transport.observable import ObservableTransport


auth_map = {
     'bearer-token': auth.BearerTokenAuth,
     'iam': auth.IAMAuth,
     'idaas': auth.IDaaSAuth,
}


class BaseClient:
    def __init__(self, setting: Union[ClientSetting, Dict] = None, base_url: str = ''):
        if setting is None:
            setting = ClientSetting()
            setting.base_url = base_url
        if isinstance(setting, dict):
            setting = ClientSetting(**setting)

        self.setting = setting
        self.base_url = setting.base_url
        self.headers = setting.headers
        auth_cls = auth_map.get(setting.auth.auth_type, None) if setting.auth else None
        if auth_cls:
            self.auth = auth_cls(**setting.auth.credentials)
        else:
            self.auth = None

        # Initialize logger            
        logger_name = __name__ + '.log'
        log_level = logging.INFO
        if setting.observable and setting.observable.log_name:
            logger_name = setting.observable.log_name
            log_level = setting.observable.log_level
        logger = logging.getLogger(logger_name)
        logger.setLevel(log_level)
        self.logger = logger

        self.timeout = httpx.Timeout(**setting.timeout.to_dict()) if setting.timeout else None
        retry = setting.retry if setting.retry else Retry(attempts=3) 

        # Setup inner transport
        if setting.transport:
            # Use the injected transport, useful for testing
            transport = setting.transport
        elif setting.host:
            # If host is set and the corresponding App exists,
            # try send request directly into ASGI bypassing HTTP
            app_name = setting.app_name or self.__class__.__name__.replace('Client', 'App')
            app = setting.host.get_app(app_name)
            if app is not None:
                transport = httpx.WSGITransport(setting.host.get_runtime())
            else:
                transport = httpx.HTTPTransport(retries=retry.attempts) 
        else:
            transport = httpx.HTTPTransport(retries=retry.attempts)   

        # Wrap transport with observability and retry
        if setting.observable:
            transport = ObservableTransport(transport, logger)

        if setting.retry:
            transport = RetryTransport(transport, retry)
        
        self.transport = transport
        self._client = httpx.Client(
            auth=self.auth, 
            timeout=self.timeout, 
            base_url=self.base_url, 
            transport=self.transport)

    def open(self):
        if self._client is None:
            self._client = httpx.Client(
                auth=self.auth, 
                timeout=self.timeout, 
                base_url=self.base_url, 
                transport=self.transport)

    def close(self):
        if self._client:
            self._client.close()

    def __enter__(self):
        self.open()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
    def request(self, method: str, endpoint: str, **kwargs):
        request = self._client.build_request(method, endpoint, headers=self.headers, **kwargs)
        try:
            response = self._client.send(request)
            response.raise_for_status()
            return response
        except httpx.HTTPError as ex:
            self.logger.error("Error requesting %s %s: %s", method, endpoint, ex)
            raise       
