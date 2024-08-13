import logging
import uuid
import json

from flask import request
from error import AppError
from werkzeug.exceptions import HTTPException

class Wrong:
    def __init__(self, app):
        self.app = app
        self.register_error_handlers()
        
    def register_error_handlers(self):
        @self.app.errorhandler(AppError)
        def handle_app_error(error):
            body = json.dumps({"code": error.code, "message": error.message})
            resp = error.get_response()
            resp.headers["X-BCE-RequestID"] = "application/json"
            resp.data = body
            resp.status_code = error.status_code
            return resp

        @self.app.errorhandler(HTTPException)
        def handle_generic_error(error):
            body = json.dumps({"code": "InternalServerError", "message": "Something went wrong."})
            resp = error.get_response()
            resp.headers["X-BCE-RequestID"] = "application/json"
            resp.data = body
            resp.status_code = error.status_code
            return resp