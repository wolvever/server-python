import httpx

from unittest.mock import patch, MagicMock
from server_python.client.client import BaseClient, ClientSetting, Auth, Retry, Timeout, Observable, RetryTransport
from server_python.client.auth import BearerTokenAuth


def test_new_client_default():
    client = BaseClient()

    assert isinstance(client, BaseClient)
    assert client.setting is not None
    assert isinstance(client.setting, ClientSetting)
    assert client.setting.app_name is None
    assert client.setting.host is None
    assert client.base_url == ''
    assert client.headers == {}
    assert client.logger is not None
    assert client.auth is None
    assert client.timeout.write == 10
    assert client.timeout.read == 10
    assert client.timeout.connect == 10
    assert client.timeout.pool == 10
    assert client.transport is not None

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


@patch('httpx.Client._send_handling_auth')
def test_client_request_default(mock_client):
    mock_resp = MagicMock()
    mock_resp.raise_for_status = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"name_default": "bob"}
    mock_client.return_value = mock_resp 

    client = BaseClient()
    resp = client.request("POST", "http://localhost:8000/default", data={"name": "foo"})
    assert resp.status_code == 200
    assert resp.json() == {"name_default": "bob"}


@patch('httpx.Client._send_handling_auth')
def test_client_request_base_url(mock_client):
    mock_resp = MagicMock()
    mock_resp.raise_for_status = MagicMock()
    mock_resp.status_code = 200
    mock_client.return_value = mock_resp

    client = BaseClient(base_url="https://demo.org:8000/api/v1")
    client.request("POST", "/endpoint", data={"name": "foo"})
    
    req = mock_client.call_args[0][0]
    assert req.url.scheme == "https"
    assert req.url.host == "demo.org"
    assert req.url.port == 8000
    assert req.url.path == "/api/v1/endpoint"


def test_client_auth_bearer_token():
    state = {}
    def handler(request):
        state["request"] = request
        return httpx.Response(200, json={"message": "Success"})

    setting = ClientSetting(
        app_name="test",
        base_url="http://example.com/api",
        headers={"X-Test": "123"},
        auth=Auth(auth_type="bearer-token", credentials={"token": "test-token"}),
        timeout=Timeout(),
        retry=Retry(attempts=2, wait_random_min=3, wait_random_max=5),
        observable=None,  # TODO: add observable tests
        transport = httpx.MockTransport(handler)
    )
    client = BaseClient(setting)

    response = client.request("GET", "/test", params={"param1": "value1"})
    assert response.status_code == 200
    assert response.json() == {"message": "Success"}

    req = state.get("request")
    assert req is not None
    assert req.method == "GET"
    assert req.url.host == "example.com"
    assert req.url.path == "/api/test"
    assert req.url.params["param1"] == "value1"
    assert req.headers["X-Test"] == "123"
    assert req.headers["Authorization"] == "Bearer test-token"