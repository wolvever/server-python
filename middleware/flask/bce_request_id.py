import logging
import uuid

from flask import request

logger = logging.getLogger(__name__)

class BceRequestIdHeader:
    def __init__(self, app):
        self.app = app
        self.app.before_request(self.before_request)
        self.app.after_request(self.after_request)
        

    def before_request(self):
        if 'X-BCE-RequestID' not in request.headers:
            request.bce_request_id = str(uuid.uuid4())
            request.headers['X-BCE-RequestID'] = request.bce_request_id
        else:
            request.bce_request_id = request.headers.get('X-BCE-RequestID')
