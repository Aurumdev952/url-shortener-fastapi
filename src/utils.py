import uuid
import validators
import secrets
import string



def is_valid_url(url: str):
    return validators.url(url)


# def generate_unique_string():
#     unique_string = str(uuid.uuid4().hex)[:5]
#     return unique_string


def generate_unique_string(length=5):
    characters = string.ascii_letters + string.digits
    unique_string = ''.join(secrets.choice(characters) for _ in range(length))
    return unique_string


