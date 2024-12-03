from cryptography.fernet import Fernet

class EncryptionManager:
    """
    Handles encryption and decryption of sensitive data.
    """
    def __init__(self, key):
        """
        Initialize the encryption manager with a Fernet key.
        """
        self.cipher = Fernet(key)

    @staticmethod
    def generate_key():
        """
        Generate a new Fernet key and save it to a file.
        Returns:
            bytes: The generated Fernet key.
        """
        key = Fernet.generate_key()
        with open("key.key", "wb") as key_file:
            key_file.write(key)
        print(f"Generated and saved key: {key}")
        return key

    @staticmethod
    def load_key():
        """
        Load the Fernet key from the 'key.key' file.
        Returns:
            bytes: The loaded Fernet key.
        """
        try:
            with open("key.key", "rb") as key_file:
                return key_file.read()
        except FileNotFoundError:
            raise FileNotFoundError("Key file not found. Please generate a key using EncryptionManager.generate_key().")

    def encrypt(self, data):
        """
        Encrypt data using the Fernet key.
        Args:
            data (str): The data to encrypt.
        Returns:
            bytes: The encrypted data.
        """
        return self.cipher.encrypt(data.encode())

    def decrypt(self, token):
        """
        Decrypt data using the Fernet key.
        Args:
            token (bytes): The encrypted data token.
        Returns:
            str: The decrypted data.
        """
        return self.cipher.decrypt(token).decode()

# Example usage of key generation (optional)
if __name__ == "__main__":
    print("Generating a new key...")
    EncryptionManager.generate_key()
