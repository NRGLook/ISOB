import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import subprocess

LICENSE_FILE = "license.txt"

def request_license_key():
    license_key = simpledialog.askstring("License Key", "Please enter your license key:")
    return license_key

def generate_license_key():
    # Generate a random license key
    license_key = ''.join(random.choice('0123456789') for _ in range(10))
    return license_key

def check_license_key(license_key):
    # Check if the license key is exactly 10 characters long and contains only digits
    return len(license_key) == 10 and license_key.isdigit()

def write_license_key_to_file(license_key):
    with open(LICENSE_FILE, "w") as file:
        file.write(license_key)

def read_license_key_from_file():
    try:
        with open(LICENSE_FILE, "r") as file:
            license_key = file.read().strip()
            return license_key
    except FileNotFoundError:
        return None

def install_application():
    subprocess.run(["D:\Study\ISOB\Lab4\lab45\dist\main.exe"])

def main():
    # Check if license file exists and is not empty
    license_key = read_license_key_from_file()
    if license_key is None or not check_license_key(license_key):
        # Request license key from user
        license_key = request_license_key()
        if not check_license_key(license_key):
            messagebox.showerror("Error", "Invalid license key. Installation aborted.")
            return
        # Write license key to file
        write_license_key_to_file(license_key)

    # Proceed with installation
    install_application()
    messagebox.showinfo("Installation Complete", "Application installed successfully.")

if __name__ == "__main__":
    main()
