from server_python.client.auth import BearerTokenAuth, IAMAuth, IDaaSAuth

def test_token_auth():
    credential = {"token": "1234567890"}
    auth = BearerTokenAuth(**credential)

    assert auth.token == credential["token"]

