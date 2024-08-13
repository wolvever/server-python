import logging

from typing import Dict, Any
from server_python.pydantic_model import SettingModel, Field
from server_python.app import App, AppSetting


class FlaskApp(App):
    def __init__(self, setting: AppSetting):
        self.logger = logging.getLogger(setting.app_name)
        self.logger.setLevel(setting.log_level)

    def register(self, root):
        """Register application to the given root runtime, it could be Flask or FastAPI instance."""
        pass

    def add_middleware(self, root):
        pass

    def start(self):
        pass

    def stop(self):
        pass

