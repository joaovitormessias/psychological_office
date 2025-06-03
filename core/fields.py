from django.db import models
from django.conf import settings
from cryptography.fernet import Fernet, InvalidToken
import base64

_cipher = None

def get_cipher():
    global _cipher
    if _cipher is None:
        key = getattr(settings, 'FERNET_KEY', None)
        if not key:
            raise ValueError("DJANGO_FERNET_KEY is not set in settings.py.")
        if isinstance(key, str): # Ensure it's bytes for Fernet
            key = key.encode('utf-8')
        try:
            _cipher = Fernet(key)
        except Exception as e:
            raise ValueError(f"Invalid Fernet key: {e}")
    return _cipher

class EncryptedTextField(models.TextField):
    description = "A TextField that stores data encrypted using Fernet."

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        try:
            decoded_value = base64.urlsafe_b64decode(value.encode('utf-8'))
            decrypted_bytes = get_cipher().decrypt(decoded_value)
            return decrypted_bytes.decode('utf-8')
        except (InvalidToken, TypeError, ValueError, Exception):
            # Log the error or handle more gracefully in production
            # For now, returning a placeholder indicates a decryption issue.
            return "DECRYPTION_ERROR" # Placeholder for unrecoverable decryption

    def to_python(self, value):
        # This method is called to convert the value from the database (after from_db_value)
        # or from a serializer into a Python object.
        # If it's already a string (from from_db_value or serializer), keep it.
        if isinstance(value, str) or value is None:
            return value
        # If it's some other type (e.g. bytes from an earlier stage), convert to string.
        return str(value)

    def get_prep_value(self, value):
        # This method is called to convert the Python object back into a database-storable format.
        if value is None:
            return None
        # Prevent saving the placeholder if it was somehow set directly
        if value == "DECRYPTION_ERROR":
            raise ValueError("Attempted to save DECRYPTION_ERROR placeholder.")

        encrypted_bytes = get_cipher().encrypt(str(value).encode('utf-8'))
        return base64.urlsafe_b64encode(encrypted_bytes).decode('utf-8')
