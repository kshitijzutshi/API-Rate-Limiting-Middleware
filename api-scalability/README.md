To make the code more scalable, you can consider the following improvements:

1. Use a configuration file or environment variables for settings like rate limiting parameters, instead of hardcoding them in the code.

2. Move the validation logic to a separate module or class to keep the code modular and maintainable.

3. Use a database or external storage to store user data instead of just returning it in the response.

4. Consider using a more robust web framework like Flask-RESTful or Flask-RestPlus for building RESTful APIs.

5. Use a production-grade web server like Gunicorn or uWSGI instead of the built-in Flask development server.

Here's an example of how you can refactor the code to incorporate some of these improvements:

```python
# app.py
from flask import Flask, request, jsonify
from middleware import RateLimitMiddleware
from validators import UserValidator
from config import RATE_LIMIT, RATE_LIMIT_WINDOW
from models import User

app = Flask(__name__)
app.wsgi_app = RateLimitMiddleware(app, limit=RATE_LIMIT, per=RATE_LIMIT_WINDOW)

@app.route("/users", methods=["POST"])
def create_user():
    try:
        data = request.json
        validator = UserValidator(data)

        if not validator.is_valid():
            return jsonify({"error": validator.error_message}), 400

        user = User(name=data["name"], age=data["age"])
        user.save()

        return jsonify(user.to_dict()), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()
```

```python
# config.py
RATE_LIMIT = 10
RATE_LIMIT_WINDOW = 60  # in seconds
```

```python
# validators.py
class UserValidator:
    def __init__(self, data):
        self.data = data
        self.error_message = None

    def is_valid(self):
        if "name" not in self.data or "age" not in self.data:
            self.error_message = "Name and age are required."
            return False

        if len(self.data["name"]) > 32:
            self.error_message = "Name should be at most 32 characters long."
            return False

        try:
            age = int(self.data["age"])
            if age < 16:
                self.error_message = "Age should be at least 16."
                return False
        except ValueError:
            self.error_message = "Age should be a number."
            return False

        return True
```

```python
# models.py
class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def save(self):
        # Save user data to a database or external storage
        pass

    def to_dict(self):
        return {
            "name": self.name,
            "age": self.age
        }
```

In this refactored code:

- The rate limiting parameters are moved to a separate `config.py` file.
- The validation logic is moved to a separate `UserValidator` class in `validators.py`.
- A `User` model is introduced in `models.py` to handle user data storage and retrieval.
- The `create_user` route focuses on handling the request, delegating validation and data storage to separate modules.

These changes make the code more modular, maintainable, and scalable. You can further enhance it by using a production-grade web server and a robust database for storing user data.