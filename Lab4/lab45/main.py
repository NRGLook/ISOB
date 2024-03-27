import tkinter as tk
from tkinter import messagebox
from authentication_system.admin_window import AdminWindow
from authentication_system.user_window import UserWindow
from authentication_system.database import authenticate, create_users_table, create_products_table

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Authentication System")
        self.geometry("500x250")  # Увеличиваем размер окна

        # Кастомные цвета
        bg_color = "#f0f0f0"
        fg_color = "#333333"
        button_bg = "#4CAF50"
        button_fg = "white"

        # Создание и размещение элементов интерфейса
        self.configure(bg=bg_color)  # Нейтральный фон

        # Центрирование полей ввода
        self.columnconfigure(1, weight=1)

        self.username_label = tk.Label(self, text="Username:", bg=bg_color, fg=fg_color)
        self.username_label.grid(row=0, column=0, padx=(50, 10), pady=10, sticky="e")
        self.username_entry = tk.Entry(self, bg=bg_color, fg=fg_color, font=("Arial", 12))
        self.username_entry.grid(row=0, column=1, padx=(0, 50), pady=10, sticky="ew")

        self.password_label = tk.Label(self, text="Password:", bg=bg_color, fg=fg_color)
        self.password_label.grid(row=1, column=0, padx=(50, 10), pady=10, sticky="e")
        self.password_entry = tk.Entry(self, show="*", bg=bg_color, fg=fg_color, font=("Arial", 12))
        self.password_entry.grid(row=1, column=1, padx=(0, 50), pady=10, sticky="ew")

        self.login_button = tk.Button(self, text="Login", command=self.login, bg=button_bg, fg=button_fg, font=("Arial", 12))
        self.login_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    def login(self):
        # create_users_table()
        # create_products_table()
        username = self.validate_input(self.username_entry.get())
        password = self.validate_input(self.password_entry.get())
        user = authenticate(username, password)
        if user:
            if user[2] == "admin":
                AdminWindow(self)
            else:
                UserWindow(self)
            # self.destroy()  # Закрываем главное окно после успешной аутентификации
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    # defense from buffer overflow
    def validate_input(self, value):
        if value is not None and len(value) > 50:
            return None
        return value

def main():
    app = MainWindow()
    app.mainloop()

main()
