import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3

class AdminWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Admin Window")
        self.configure(bg="#f0f0f0")  # Нейтральный фон

        self.create_widgets()
        self.load_products()

    def create_widgets(self):
        # Отображение списка продуктов
        self.product_label = tk.Label(self, text="Groups Management System", bg="#f0f0f0", fg="#333333", font=("Arial", 16, "bold"))
        self.product_label.pack(pady=10)

        self.product_listbox = tk.Listbox(self, bg="white", fg="#333333", font=("Arial", 12), selectbackground="#4CAF50", selectforeground="white")
        self.product_listbox.pack(fill="both", expand=True, padx=10, pady=5)

        # Кнопки для CRUD операций
        button_frame = tk.Frame(self, bg="#f0f0f0")  # Контейнер для кнопок
        button_frame.pack(pady=5)

        self.add_button = tk.Button(button_frame, text="Add", command=self.add_product, bg="#4CAF50", fg="white", font=("Arial", 12))
        self.add_button.pack(side="left", padx=5)

        self.edit_button = tk.Button(button_frame, text="Edit", command=self.edit_product, bg="#FFC107", fg="white", font=("Arial", 12))
        self.edit_button.pack(side="left", padx=5)

        self.delete_button = tk.Button(button_frame, text="Delete", command=self.delete_product, bg="#F44336", fg="white", font=("Arial", 12))
        self.delete_button.pack(side="left", padx=5)

    def load_products(self):
        conn = sqlite3.connect("D:/Study/ISOB/Lab4/lab45/data/products.db")
        c = conn.cursor()
        c.execute("SELECT * FROM products")
        products = c.fetchall()
        conn.close()

        for product in products:
            self.product_listbox.insert(tk.END, product[1])

    def add_product(self):
        name = self.validate_input(simpledialog.askstring("Add Product", "Enter product name:"))
        if name:
            conn = sqlite3.connect("D:/Study/ISOB/Lab4/lab45/data/products.db")
            c = conn.cursor()
            c.execute("INSERT INTO products (name) VALUES (?)", (name,))
            conn.commit()
            conn.close()
            self.product_listbox.insert(tk.END, name)

    def edit_product(self):
        selected_index = self.product_listbox.curselection()
        if selected_index:
            name = self.validate_input(simpledialog.askstring("Edit Product", "Enter new name:",
                                                              initialvalue=self.product_listbox.get(selected_index)))
            if name:
                conn = sqlite3.connect("D:/Study/ISOB/Lab4/lab45/data/products.db")
                c = conn.cursor()
                c.execute("UPDATE products SET name=? WHERE id=?", (name, selected_index[0] + 1))
                conn.commit()
                conn.close()
                self.product_listbox.delete(selected_index)
                self.product_listbox.insert(selected_index, name)

    def delete_product(self):
        selected_index = self.product_listbox.curselection()
        if selected_index:
            conn = sqlite3.connect("D:/Study/ISOB/Lab4/lab45/data/products.db")
            c = conn.cursor()
            c.execute("DELETE FROM products WHERE id=?", (selected_index[0] + 1,))
            conn.commit()
            conn.close()
            self.product_listbox.delete(selected_index)

    # Защита от переполнения буфера
    def validate_input(self, value):
        if value is not None and len(value) > 50:
            messagebox.showerror("Error", "Input exceeds 50 characters.")
            return None
        return value
