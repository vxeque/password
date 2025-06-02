from cryptography.fernet import Fernet
from django.conf import settings

fernet = Fernet(settings.FERNET_KEY.encode())

def encrypt_password(plain_text_password: str) -> str:
    return fernet.encrypt(plain_text_password.encode()).decode()

def decrypt_password(encrypted_password: str) -> str:
    return fernet.decrypt(encrypted_password.encode()).decode()
