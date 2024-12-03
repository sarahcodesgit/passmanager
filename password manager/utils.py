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
