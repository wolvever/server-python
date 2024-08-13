import logging

from typing import Dict, Any
from server_python.pydantic_model import SettingModel, Field


class ServerSetting(SettingModel):
    host: str = "0.0.0.0"
    port: int = 8080
    debug: bool = True
    options: Dict[str, Any] = Field(default_factory=dict)


class AppSetting(SettingModel):
    app_name: str = "app"
    app_version: str = "1.0"
    log_level: str = "INFO"
    
    server: ServerSetting = Field(default_factory=ServerSetting)
    base_url: str = "/api/v1"
    sections: Dict[str, Any] = Field(default_factory=dict)


class App:
    def __init__(self, setting: AppSetting):
        self.logger = logging.getLogger(setting.app_name)
        self.logger.setLevel(setting.log_level)

    def register(self, root):
        """Register application to the given root runtime, it could be Flask or FastAPI instance."""
        pass

    def start(self):
        pass

    def stop(self):
        pass
