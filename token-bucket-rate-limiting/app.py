from flask import Flask, request, jsonify
import time

app = Flask(__name__)

# Define the rate limit parameters
TOKENS = 10
FILL_RATE = 0.2  # 1 token per second
last_checked = time.time()
bucket = TOKENS

def rate_limit():
    global last_checked, bucket
    now = time.time()
    elapsed = now - last_checked
    # Refill the bucket
    bucket += elapsed * FILL_RATE
    if bucket > TOKENS:
        bucket = TOKENS
    last_checked = now
    if bucket < 1:
        return False  # Bucket is empty
    bucket -= 1
    return True

@app.before_request
def check_rate_limit():
    if not rate_limit():
        return jsonify({"error": "Rate limit exceeded. Please try again later."}), 429

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
def create_user():
    try:
        # Get JSON payload from the request
        data = request.json

        # Validate the payload
        is_valid, error_message = validate_payload(data)
        if not is_valid:
            return jsonify({"error": error_message}), 400

        # Return the saved user data with a 201 status code
        return jsonify("Valid Data"), 201

    except Exception as e:
        # If any unexpected error occurs, return a 500 status code with the error message
        return jsonify({"error": str(e)}), 500

@app.errorhandler(429)
def handle_rate_limit_exceeded(error):
    return jsonify({"error": "Rate limit exceeded. Please try again later."}), 429

if __name__ == '__main__':
    app.run(debug=True)