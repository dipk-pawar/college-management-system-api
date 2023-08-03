import random
import string


class GenerateRandomChar:
    @staticmethod
    def generate_password(length=12):
        characters = string.ascii_uppercase + string.digits + string.punctuation
        return "".join(random.choice(characters) for _ in range(length))

    @staticmethod
    def generate_username(group_name, length=15):
        # Remove any spaces and convert to lowercase
        group_name = group_name.strip().lower()
        username_base = group_name[:10]

        # Generate a random integer between 1000 and 9999
        random_number = random.randint(1000, 9999)
        username = f"{username_base}{random_number}"
        username = username.upper()

        # Check if the length of the username is less than the specified length
        if len(username) < length:
            # Calculate the number of characters to add
            chars_to_add = length - len(username)

            # Generate a random string of the required length
            random_string = "".join(
                random.choices(string.ascii_uppercase + string.digits, k=chars_to_add)
            )

            # Append the random string to the username
            username += random_string

        return username
