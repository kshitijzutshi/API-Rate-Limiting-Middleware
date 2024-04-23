# app.py
from flask import Flask, request, jsonify
# import sys
# sys.path.insert(0, '/Users/kshitijzutshi/Desktop/GitHub-Repos/Python_Power_Scripts/API-testing')
# from MiddlewareApi.middleware import RateLimitMiddleware
from validators import UserValidator
from middleware import RateLimitMiddleware
from config import RATE_LIMIT, RATE_LIMIT_WINDOW
from model import User

print("before middleware")
app = Flask(__name__)
app.debug = True
rate_limiter = RateLimitMiddleware(limit=RATE_LIMIT, per=RATE_LIMIT_WINDOW)
print("after middleware")

@app.route("/users", methods=["POST"])
def create_user():
    print("Creating user...")
    client_ip = request.remote_addr

    if not rate_limiter.allow_request(client_ip):
        return jsonify({"error": "Too many requests"}), 429
    try:
        data = request.json
        validator = UserValidator(data)

        if not validator.is_valid():
            print("Invalid user data")
            return jsonify({"error": validator.error_message}), 400

        user = User(name=data["name"], age=data["age"])
        user.save()
        print("User created successfully")

        return jsonify(user.to_dict()), 201

    except Exception as e:
        print(f"Error creating user: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()