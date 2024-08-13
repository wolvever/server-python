import time
from flask import request
from prometheus_client import Counter, Histogram, CollectorRegistry

class Metrics:
    def __init__(self, app):
        if not app.config.get("METRICS_ENABLED", False):
            return
        
        self.app = app
        registry = CollectorRegistry()
        buckets = [0.1, 0.3, 1.5, 10.5]
        self.registry = registry

        self.metrics_request_latency = Histogram(
            "request_seconds",
            "records in a histogram the number of http requests and their duration in seconds",
            ["type", "status", "method", "addr", "version"],
            buckets=buckets,
            registry=registry
        )

        self.metrics_request_size = Counter(
            "response_size_bytes",
            "counts the size of each http response",
            ["type", "status", "method", "addr", "version"],
            registry=registry
        )
        
        self.app_version = app.config.get("APP_VERSION", "1.0.0")
        self.app.before_request(self.before_request)
        self.app.after_request(self.after_request)

    def before_request(self):
        """
        Get start time of a request
        """
        request._metrics_request_start_time = time.time()

    def after_request(self, response):
        """
        Register Prometheus metrics after each request
        """
        size_request = int(response.headers.get("Content-Length", 0))
        request_latency = time.time() - request._metrics_request_start_time
        
        self.metrics_request_latency \
            .labels("http", response.status_code, request.method, request.path, self.app_version) \
            .observe(request_latency)
        self.metrics_request_size.labels(
            "http", response.status_code, request.method, request.path, self.app_version
        ).inc(size_request)
        return response

