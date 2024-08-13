from typing import Dict
from server_python.app import App, AppSetting
from server_python.host import Host


class FlaskHost(Host):
    from flask import Flask

    def __init__(self, flask_obj = None, flask_config: Dict = {}):
        if flask_obj is None:
            flask_obj = self.Flask(__name__, **flask_config)
        
        self.app = flask_obj
        self.apps = {}

    def config(self, setting: AppSetting):
        self.setting = setting
        self.app.config.from_object(setting)
        
    def add_app(self, app: App):
        app.register(self.app)
        app_name = app.__class__.__name__
        self.apps[app_name] = app
    
    def get_app(self, app_name: str) -> App:
        return self.apps.get(app_name)
    
    def get_runtime(self):
        return self.app

    def run(self):
        setting = self.setting.server
        self.app.run(
            host=setting.host, 
            port=setting.port, 
            debug=setting.debug,
            **setting.options)
