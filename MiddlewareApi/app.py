# app.py
from flask import Flask, request, jsonify
from middleware import RateLimitMiddleware

app = Flask(__name__)
app.wsgi_app = RateLimitMiddleware(app, limit=10, per=20)  # 10 requests per minute

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

if __name__ == '__main__':
    app.run(debug=False, use_reloader=False)