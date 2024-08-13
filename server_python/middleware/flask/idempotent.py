from flask import request
import logging

logger = logging.getLogger(__name__)

class Idempotence:
    def __init__(self, app):
        if not app.config.get("IDEMPOTENT_ENABLED", False):
            return
        
        self.app = app
        self.app.before_request(self.before_request)
        self.app.after_request(self.after_request)
        

    def before_request(self):
        logger.debug("before:", request.method, request.url)
        

    def after_request(self, response):
        logger.debug("after:", request.method, request.url)