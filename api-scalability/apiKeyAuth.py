# apiKeyAuth.py
from flask import request, jsonify

# A dictionary to store our users and their API keys
# In a real application, you would use a database for this
users = {}

def authenticate(api_key, users):
    # Get the API key from the request headers
    api_key = request.headers.get('X-API-Key')
    print(f"API key: {api_key}")

    # If the API key is not provided, return an error
    if not api_key:
        return jsonify(error='Missing API key'), 400

    # If the API key is not valid, return an error
    if api_key not in users:
        return jsonify(error='Invalid API key'), 403

    # Return the user data
    return jsonify(users[api_key])