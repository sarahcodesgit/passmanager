from encryption import EncryptionManager
from database import DatabaseManager

class PasswordManager:
    def __init__(self, key):
        self.encryption = EncryptionManager(key)
        self.db = DatabaseManager()

    def add_password(self, service, username, password):
        encrypted_password = self.encryption.encrypt(password)
        self.db.add_password(service, username, encrypted_password)

    def get_password(self, service):
        result = self.db.get_password(service)
        if result:
            username, encrypted_password = result
            password = self.encryption.decrypt(encrypted_password)
            return username, password
        return None