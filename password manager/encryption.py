from cryptography.fernet import Fernet

class EncryptionManager:
    def __init__(self, key):
        self.cipher = Fernet(key)

    @staticmethod
    def generate_key():
        return Fernet.generate_key()

    def encrypt(self, data):
        return self.cipher.encrypt(data.encode())

    def decrypt(self, token):
        return self.cipher.decrypt(token).decode()