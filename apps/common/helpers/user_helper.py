import random
import string


class GeneratePassword:
    @staticmethod
    def generate_password(length=12):
        characters = string.ascii_uppercase + string.digits + string.punctuation
        return "".join(random.choice(characters) for _ in range(length))
