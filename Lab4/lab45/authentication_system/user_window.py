import tkinter as tk
from tkinter import filedialog, messagebox
import sqlite3
import os

MAX_FILE_SIZE = 1024 * 1024  # 1 MB


class UserWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("User Window")

        # Displaying the list of products
        self.product_label = tk.Label(self, text="Groups IiTP", font=("Helvetica", 16))
        self.product_label.pack(pady=10)

        self.product_listbox = tk.Listbox(self, font=("Helvetica", 12))
        self.product_listbox.pack(fill="both", expand=True, padx=10)

        # Connecting to the database and loading products
        self.load_products()

        self.select_file_button = tk.Button(self, text="Select File", command=self.select_file, font=("Helvetica", 12))
        self.select_file_button.pack(pady=10)

    def load_products(self):
        conn = sqlite3.connect("D:/Study/ISOB/Lab4/lab45/data/products.db")
        c = conn.cursor()
        c.execute("SELECT * FROM products")
        products = c.fetchall()
        conn.close()

        for product in products:
            self.product_listbox.insert(tk.END, product[1])  # Assuming the product name is in the second column

    def select_file(self):
        # Getting the path to the 'data' folder within the project
        data_folder = "D:/Study/ISOB/Lab4/lab45/data"

        # Opening a file dialog to choose a file from the 'data' folder
        selected_file = filedialog.askopenfilename(initialdir=data_folder, title="Select File",
                                                   filetypes=[("Text files", "*.txt")])

        if selected_file:
            # Checking if the selected file is inside the 'data' folder
            if os.path.dirname(selected_file) != data_folder:
                messagebox.showerror("Error", "Selected file is not in the data folder.")
                return

            # Checking the size of the selected file
            file_size = os.path.getsize(selected_file)
            if file_size > MAX_FILE_SIZE:
                messagebox.showerror("Error", "Selected file size exceeds the maximum allowed size.")
            else:
                # Reading the content of the file and displaying it in a messagebox
                try:
                    with open(selected_file, 'r') as file:
                        file_content = file.read()
                        messagebox.showinfo("File Content", file_content)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to read file: {e}")
