import tkinter as tk
from tkinter import messagebox
from encryption import EncryptionManager
from password_manager import PasswordManager

class PasswordManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Manager")

        # Load encryption key
        self.key = EncryptionManager.load_key()
        self.manager = PasswordManager(self.key)

        # Create UI elements
        self.service_label = tk.Label(root, text="Service:")
        self.service_label.grid(row=0, column=0, padx=10, pady=10)
        self.service_entry = tk.Entry(root, width=30)
        self.service_entry.grid(row=0, column=1, padx=10, pady=10)

        self.username_label = tk.Label(root, text="Username:")
        self.username_label.grid(row=1, column=0, padx=10, pady=10)
        self.username_entry = tk.Entry(root, width=30)
        self.username_entry.grid(row=1, column=1, padx=10, pady=10)

        self.password_label = tk.Label(root, text="Password:")
        self.password_label.grid(row=2, column=0, padx=10, pady=10)
        self.password_entry = tk.Entry(root, width=30)
        self.password_entry.grid(row=2, column=1, padx=10, pady=10)

        self.add_button = tk.Button(root, text="Add Password", command=self.add_password)
        self.add_button.grid(row=3, column=0, padx=10, pady=10)

        self.retrieve_button = tk.Button(root, text="Retrieve Password", command=self.retrieve_password)
        self.retrieve_button.grid(row=3, column=1, padx=10, pady=10)

    def add_password(self):
        service = self.service_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        if service and username and password:
            self.manager.add_password(service, username, password)
            messagebox.showinfo("Success", "Password added successfully!")
            self.service_entry.delete(0, tk.END)
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "All fields must be filled!")

    def retrieve_password(self):
        service = self.service_entry.get()

        if service:
            result = self.manager.get_password(service)
            if result:
                username, password = result
                messagebox.showinfo("Password Retrieved", f"Username: {username}\nPassword: {password}")
            else:
                messagebox.showerror("Error", "Service not found!")
        else:
            messagebox.showerror("Error", "Service field must be filled!")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManagerApp(root)
    root.mainloop()
