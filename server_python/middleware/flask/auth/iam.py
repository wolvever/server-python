from flask import request
import logging

logger = logging.getLogger(__name__)

class IAMLogin:
    def __init__(self, app):
        if not app.config.get("IAM_LOGIN_ENABLED", False):
            return
        
        self.app = app
        self.app.before_request(self.before_request)
        self.app.after_request(self.after_request)
        

    def before_request(self):
        logger.debug("BeforeLogin:", request.method, request.url)
        

    def after_request(self, response):
        logger.debug("AfterLogin:", request.method, request.url)


class IAMAuthentication:
    def __init__(self, app):
        if not app.config.get("IAM_AUTH_ENABLED", False):
            return
                
        self.app = app
        self.app.before_request(self.before_request)
        self.app.after_request(self.after_request)
        

    def before_request(self):
        logger.debug("BeforeLogin:", request.method, request.url)
        

    def after_request(self, response):
        logger.debug("AfterLogin:", request.method, request.url)


class IAMBearerToken:
    def __init__(self, app):
        if not app.config.get("IAM_BEARERTOKEN_ENABLED", False):
            return

        self.app = app
        self.app.before_request(self.before_request)
        self.app.after_request(self.after_request)
        

    def before_request(self):
        logger.debug("BeforeLogin:", request.method, request.url)
        

    def after_request(self, response):
        logger.debug("AfterLogin:", request.method, request.url)

