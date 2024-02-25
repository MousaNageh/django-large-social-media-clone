from cryptography.fernet import Fernet
import os


class CryptoUtilities:
    SYSTEM_ENCRYPTION_KEY = os.environ.get("CRYPTO_KEY")
    system_fernet = Fernet(SYSTEM_ENCRYPTION_KEY)

    @staticmethod
    def generate_crypto_key():
        return Fernet.generate_key().decode("utf-8")

    @classmethod
    def encrypt(cls, plain, key=None):
        fernet = cls._get_fernet(key)
        return fernet.encrypt(plain.encode("utf-8")).decode("utf-8")

    @classmethod
    def decrypt(cls, cipher, key=None):
        fernet = cls._get_fernet(key)
        return fernet.decrypt(cipher.encode("utf-8")).decode("utf-8")

    @classmethod
    def generate_encrypted_key(cls):
        key = cls.generate_crypto_key()
        return cls.encrypt(plain=key)

    @classmethod
    def _get_fernet(cls, key):
        if not key:
            return cls.system_fernet
        else:
            return Fernet(key)
