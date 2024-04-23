import flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import json
import traceback

app = flask.Flask(__name__)

# Initialize Flask-Limiter
limiter = Limiter(
    app,
    default_limits=["5 per minute"]  # Limit to 5 requests per minute by default
)
limiter.init_app(app)
print(get_remote_address)

# Validation function remains unchanged
def validate_payload(data):
    if "name" not in data or "age" not in data:
        return False, "Name and age are required."
    
    if len(data["name"]) > 32:
        return False, "Name should be at most 32 characters long."
    
    try:
        age = int(data["age"])
        if age < 16:
            return False, "Age should be at least 16."
    except ValueError:
        return False, "Age should be a number."
    
    return True, None

@app.route("/users", methods=["POST"])
@limiter.limit("5 per minute", key_func=get_remote_address)  # Apply rate limiting to the /users endpoint
def create_user():
    try:
        # Get JSON payload from the request
        data = flask.request.json

        # Validate the payload
        is_valid, error_message = validate_payload(data)
        if not is_valid:
            return flask.jsonify({"error": error_message}), 400

        # Return the saved user data with a 201 status code
        return flask.jsonify("Valid Data"), 201

    except Exception as e:
        # If any unexpected error occurs, return a 500 status code with the error message
        return flask.jsonify({"error": str(e)}), 500

@app.errorhandler(429)
def handle_rate_limit_exceeded(error):
    return flask.jsonify({"error": "Rate limit exceeded. Please try again later."}), 429


if __name__ == "__main__":
    app.run()