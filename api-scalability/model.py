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