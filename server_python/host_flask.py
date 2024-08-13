from typing import Dict
from flask import Flask

from server_python.app import App, AppSetting
from server_python.host import Host


class FlaskHost(Host):

    def __init__(self, flask = None, flask_config: Dict = {} ):
        if flask is None:
            flask = Flask(__name__, **flask_config)
        
        self.flask = flask
        self.apps = {}

    def config(self, setting: AppSetting):
        self.setting = setting
        self.flask.config.from_object(setting)
        
    def add_app(self, app: App):
        app.register(self.flask)
        app_name = app.__class__.__name__
        self.apps[app_name] = app
    
    def get_app(self, app_name: str) -> App:
        return self.apps.get(app_name)
    
    def get_runtime(self):
        return self.flask

    def run(self):
        setting = self.setting.server
        self.flask.run(
            host=setting.host, 
            port=setting.port, 
            debug=setting.debug,
            **setting.options)
