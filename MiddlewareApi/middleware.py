# middleware.py
import time
from werkzeug.wrappers import Response, Request

class RateLimitMiddleware:
    def __init__(self, app, limit, per):
        self.app = app
        self.limit = limit
        self.per = per
        self.current_count = 0
        self.start_time = time.time()

    def __call__(self, environ, start_response):
        # request = Request(environ)
        # print(f"Method: {request.method}, Path: {request.path}")
        self.current_count += 1
        print(f"Current count: {self.current_count}")
        print(f"Limit: {self.limit}")
        print(f"Current time: {time.time()}")
        print(f"Start time: {self.start_time}")

        if self.current_count >= self.limit:
            response = Response("Too many requests", status=429)
            return response(environ, start_response)

        if time.time() - self.start_time > self.per:
            self.start_time = time.time()
            self.current_count = 0

        return self.app(environ, start_response)