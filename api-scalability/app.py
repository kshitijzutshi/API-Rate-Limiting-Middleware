# app.py
from flask import Flask, request, jsonify
# import sys
# sys.path.insert(0, '/Users/kshitijzutshi/Desktop/GitHub-Repos/Python_Power_Scripts/API-testing')
# from MiddlewareApi.middleware import RateLimitMiddleware
from validators import UserValidator
from middleware import RateLimitMiddleware
from config import RATE_LIMIT, RATE_LIMIT_WINDOW
from model import User
import secrets
from apiKeyAuth import authenticate

print("before middleware")
app = Flask(__name__)
app.debug = True
rate_limiter = RateLimitMiddleware(limit=RATE_LIMIT, per=RATE_LIMIT_WINDOW)
print("after middleware")

users = {}

@app.route("/users", methods=["POST"])
def create_user():
    client_ip = request.remote_addr

    if not rate_limiter.allow_request(client_ip):
        return jsonify(error="Too many requests"), 429

    # Get the user data from the request
    user_data = request.get_json()

    # Generate a secure random API key for the user
    api_key = secrets.token_urlsafe(64)

    # Store the user data and API key in our "database"
    users[api_key] = user_data

    # Return the API key to the user
    return jsonify(api_key=api_key)

@app.route("/users", methods=["GET"])
def get_user():
    return authenticate(request, users)

if __name__ == '__main__':
    app.run(debug=True, port=8000)