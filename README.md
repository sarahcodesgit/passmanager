# Password Manager

### **Steps to Create a Password Manager**

#### 1. **Requirements**
- **Features:**
  - Add, update, delete, and retrieve passwords.
  - Generate strong passwords.
  - Securely encrypt passwords.
  - Authenticate the user before access.
  - Backup and restore functionality.
- **Security:**
  - Encryption (e.g., AES).
  - Use a master password for access.
  - Implement secure storage for encryption keys.

#### 2. **Tech Stack**
- **Programming Language:** Python.
- **Database:** SQLite (for a simple tool), or a cloud database if needed.
- **Encryption Library:** e.g., `cryptography` for Python.

#### 3. **Plan the Architecture**
- **Core Components:**
  - **User Interface (UI):** CLI or GUI (Tkinter, PyQt for Python, or a web app).
  - **Storage Layer:** Store encrypted passwords in a database or a local file.
  - **Encryption Module:** Encrypt and decrypt passwords.
  - **Authentication Module:** Validate the master password.

---

### **Implementation Outline**

#### 1. **Initialize the Project**
**Create a Folder**:
Open VSCode, click on `File > Open Folder`, and create/select a folder for your project (e.g., `PasswordManager`).
Create a new project structure. For example:
```
password_manager/
├── main.py
├── encryption.py
├── database.py
├── ui.py
├── utils.py
├── password_manager.py
├── generate_key.py
└── requirements.txt
```

#### 2. **Set Up Dependencies**
1. **Add Dependencies** to `requirements.txt`:
   ```plaintext
   cryptography
   ```

2. **Install Dependencies**:
   Use `pip` to install:
   ```bash
   pip install -r requirements.txt
   ```

#### 3. **Develop the Encryption Module**
Use AES for encryption in encryption.py:
```python
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
```

#### 4. **Database Layer**
Store passwords securely in database.py:
```python
import sqlite3

class DatabaseManager:
    def __init__(self, db_name="passwords.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY,
            service TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def add_password(self, service, username, password):
        query = "INSERT INTO passwords (service, username, password) VALUES (?, ?, ?)"
        self.conn.execute(query, (service, username, password))
        self.conn.commit()

    def get_password(self, service):
        query = "SELECT username, password FROM passwords WHERE service = ?"
        return self.conn.execute(query, (service,)).fetchone()
```

#### 5. **Integrate Components**
Combine encryption and database in password_manager.py:
```python
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
```
#### 6. **Create main file**
Here’s how main.py should look if everything is set up correctly:
```python
from password_manager import PasswordManager
from encryption import EncryptionManager

def main():
    key = EncryptionManager.load_key()  # Properly load the key
    manager = PasswordManager(key)

    while True:
        print("1. Add Password\n2. Retrieve Password\n3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            service = input("Enter service name: ")
            username = input("Enter username: ")
            password = input("Enter password: ")
            manager.add_password(service, username, password)
            print("Password added successfully.")
        elif choice == "2":
            service = input("Enter service name: ")
            result = manager.get_password(service)
            if result:
                print(f"Username: {result[0]}, Password: {result[1]}")
            else:
                print("Service not found.")
        elif choice == "3":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
```

#### 7. **Create a User Interface (optional)**
For a simple CLI in ui.py:
```python
from password_manager import PasswordManager

def main():
    key = b'your_generated_key_here'  # Store securely or generate dynamically
    manager = PasswordManager(key)

    while True:
        print("1. Add Password\n2. Retrieve Password\n3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            service = input("Enter service name: ")
            username = input("Enter username: ")
            password = input("Enter password: ")
            manager.add_password(service, username, password)
            print("Password added successfully.")
        elif choice == "2":
            service = input("Enter service name: ")
            result = manager.get_password(service)
            if result:
                print(f"Username: {result[0]}, Password: {result[1]}")
            else:
                print("Service not found.")
        elif choice == "3":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
```

#### 8. **Secure the Master Key**
For a great place to store helper functions and utilities in utils.py:

```python
import random
import string
import shutil
import os
import hashlib

def generate_password(length=16):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def validate_service_name(service):
    if not service.strip():
        raise ValueError("Service name cannot be empty.")
    return service

def validate_password_strength(password):
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long.")
    if not any(char.isdigit() for char in password):
        raise ValueError("Password must include at least one number.")
    if not any(char.isupper() for char in password):
        raise ValueError("Password must include at least one uppercase letter.")
    if not any(char.islower() for char in password):
        raise ValueError("Password must include at least one lowercase letter.")
    if not any(char in string.punctuation for char in password):
        raise ValueError("Password must include at least one special character.")
    return password

def backup_database(source_file="passwords.db", backup_file="backup_passwords.db"):
    shutil.copy(source_file, backup_file)
    print(f"Backup created: {backup_file}")

def restore_database(backup_file="backup_passwords.db", target_file="passwords.db"):
    shutil.copy(backup_file, target_file)
    print(f"Database restored from: {backup_file}")

def get_env_variable(var_name, default=None):
    value = os.getenv(var_name)
    if value is None and default is None:
        raise ValueError(f"Environment variable {var_name} is not set.")
    return value or default

def format_service_display(service, username, password):
    return f"Service: {service}\nUsername: {username}\nPassword: {password}\n"

def hash_master_password(master_password, salt):
    return hashlib.pbkdf2_hmac('sha256', master_password.encode(), salt, 100000)
```


#### 9. **Initialize a Git Repository**
   Run the following commands in the integrated terminal:
   ```bash
   git init
   ```
   This initializes version control for your project.

**Add `.gitignore`**:
   Prevent sensitive files from being pushed to GitHub by adding a `.gitignore` file with:
   ```
   __pycache__/
   *.pyc
   passwords.db
   env/
   ```
#### **Step 10: Generating an Encryption Key**
You can generate a secure encryption key using the `cryptography` library. Here's how:

### **Generate the Key**
1. **Create a script (e.g., `generate_key.py`)**:
   ```python
   from cryptography.fernet import Fernet

   def generate_key():
       # Generates a secure encryption key
       key = Fernet.generate_key()
       # Save the key to a file for reuse
       with open("key.key", "wb") as key_file:
           key_file.write(key)
       print("Key generated and saved to 'key.key'")

   if __name__ == "__main__":
       generate_key()
   ```

2. **Run the Script**:
   In VSCode terminal, execute:
   ```bash
   python generate_key.py
   ```
   This generates a key file named `key.key` in your project directory.

3. **Secure the Key**:
   - **Never Hardcode the Key** in your code. Always load it dynamically from the file or an environment variable.
   - **Restrict File Permissions**:
     - On Linux/macOS:
       ```bash
       chmod 600 key.key
       ```
     - On Windows, adjust file properties to restrict access.

---

#### **Step 11: Create a Virtual Environment**
1. **Create Virtual Environment**:
   ```bash
   python -m venv env
   ```

2. **Activate the Environment**:
   - On Windows:
     ```bash
     .\env\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source env/bin/activate
     ```


#### **Step 12: Test Your Application**
1. **Run the App**:
   Press `Ctrl+` (or `F5` in VSCode) to run the `main.py`.

2. **Test Scenarios**:
   - Add a password for a service.
   - Retrieve the password for a service.
Example:
```
password manager> python main.py
1. Add Password
2. Retrieve Password
3. Exit
Choose an option: 1
Enter service name: Github
Enter username: sarahcodesgit
Enter password: notmyrealpassword
Password added successfully.
1. Add Password
2. Retrieve Password
3. Exit
Choose an option: 2
Enter service name: Github
Username: sarahcodesgit, Password: notmyrealpassword
1. Add Password
2. Retrieve Password
3. Exit
Choose an option:
```
---

