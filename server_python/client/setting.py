import httpx

from typing import Dict, Optional
from server_python.pydantic_model import SettingModel, Field
from server_python.host import Host


class Auth(SettingModel):
    auth_type: str = 'bearer-token'
    credentials: Dict[str, str] = Field(default_factory=dict)


class Timeout(SettingModel):
     connect: Optional[int] = Field(default=10)
     read: Optional[int] = Field(default=10)
     write: Optional[int] = Field(default=10)
     pool: Optional[int] = Field(default=10)


class Retry(SettingModel):
    attempts: Optional[int] = Field(default=3)
    wait_fix: Optional[int] = Field(default=0.1)
    wait_random_min: Optional[int] = Field(default=0)
    wait_random_max: Optional[int] = Field(default=1)
    wait_exponential_min: Optional[int] = Field(default=0)
    wait_exponential_max: Optional[int] = Field(default=10)
    is_exponential: bool = False
    is_random: bool = True


class Observable(SettingModel):
    log_name: Optional[str] = None
    log_level: str = 'INFO'
    trace_server: Optional[str] = None
    stats_server: Optional[str] = None


class ClientSetting(SettingModel):
     app_name: str = None
     base_url: str = ''
     headers: Dict[str, str] = Field(default_factory=dict)
     auth: Optional[Auth] = None
     timeout: Optional[Timeout] = Field(default_factory=lambda : Timeout())
     retry: Optional[Retry] = Field(default_factory=lambda : Retry())
     observable: Optional[Observable] = None
     transport: Optional[httpx.BaseTransport] = None
     host: Optional[Host] = None