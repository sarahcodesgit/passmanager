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
