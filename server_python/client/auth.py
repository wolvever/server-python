from httpx import Auth


class BearerTokenAuth(Auth):
    def __init__(self, token: str) -> None:
        self.token = token

    def auth_flow(self, request):
        request.headers["Authorization"] = f"Bearer {self.token}"
        yield request


class IAMAuth(Auth):
    def __init__(self, access_key: str, secret_key: str) -> None:
        self.access_key = access_key
        self.secret_key = secret_key
    
    def auth_flow(self, request):
        yield request
        

class IDaaSAuth(Auth):
    def __init__(self, access_key: str, secret_key: str) -> None:
        self.access_key = access_key
        self.secret_key = secret_key
    
    def auth_flow(self, request):
        yield request


class OAuth20Auth(Auth):
    def __init__(self, client_id: str, client_secret: str) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
    
    def auth_flow(self, request):
        yield request