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