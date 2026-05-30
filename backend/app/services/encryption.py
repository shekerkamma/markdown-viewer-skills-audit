import base64

from cryptography.fernet import Fernet

from app.config import settings

_fernet = None


def _get_fernet() -> Fernet:
    global _fernet
    if _fernet is None:
        key = settings.encryption_key
        if not key:
            raise RuntimeError("ENCRYPTION_KEY must be set for token encryption")
        # Accept raw 32-byte key or Fernet-compatible base64 key
        if len(key) == 32:
            key = base64.urlsafe_b64encode(key.encode()).decode()
        _fernet = Fernet(key.encode() if isinstance(key, str) else key)
    return _fernet


def encrypt(plaintext: str) -> str:
    return _get_fernet().encrypt(plaintext.encode()).decode()


def decrypt(ciphertext: str) -> str:
    return _get_fernet().decrypt(ciphertext.encode()).decode()
