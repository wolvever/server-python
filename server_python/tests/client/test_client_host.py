import httpx

from unittest.mock import patch, MagicMock
from server_python.client.client import BaseClient, ClientSetting, Auth, Retry, Timeout, Observable, RetryTransport
from server_python.client.auth import BearerTokenAuth



def test_client_setting():
    setting = ClientSetting(
        app_name="test",
        base_url="http://example.com/api",
        headers={"X-Test": "123"},
        auth=Auth(auth_type="bearer-token", credentials={"token": "test-token"}),
        timeout=Timeout(),
        retry=Retry(attempts=2, wait_random_min=3, wait_random_max=5),
        observable=None,  # TODO: add observable tests
        transport = httpx.MockTransport(lambda request: httpx.Response(200, json={"message": "Success"}))
    )
    client = BaseClient(setting)

    assert client.setting.app_name == "test"
    assert client.setting.base_url == "http://example.com/api"
    assert client.setting.headers == {"X-Test": "123"}
    
    assert isinstance(client.auth, BearerTokenAuth)
    assert client.auth.token == "test-token"

    assert client.setting.timeout.connect > 0
    assert client._client.timeout.connect == client.setting.timeout.connect
    assert client._client.timeout.read == client.setting.timeout.read
    assert client._client.timeout.write == client.setting.timeout.write
    assert client._client.timeout.pool == client.setting.timeout.pool

    assert isinstance(client.transport, RetryTransport)
    retry_fn = client.transport.retry_fn
    assert retry_fn is not None
    assert retry_fn.retry.stop.max_attempt_number == 2
    assert retry_fn.retry.wait.wait_random_min == 3
    assert retry_fn.retry.wait.wait_random_max == 5