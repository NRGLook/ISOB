import sqlite3


def create_products_table():
    conn = sqlite3.connect("D:/Study/ISOB/Lab4/lab45/data/products.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products
                 (id INTEGER PRIMARY KEY, name TEXT, description TEXT)''')
    conn.commit()
    conn.close()


def create_users_table():
    conn = sqlite3.connect("D:/Study/ISOB/Lab4/lab45/data/users.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password TEXT, role TEXT)''')
    conn.commit()
    conn.close()


def add_user(username, password, role):
    conn = sqlite3.connect("D:/Study/ISOB/Lab4/lab45/data/users.db")
    c = conn.cursor()
    c.execute("INSERT INTO users VALUES (?, ?, ?)", (username, password, role))
    conn.commit()
    conn.close()


# defense from SQL-injection - parameters in SQL-query
def authenticate(username, password):
    conn = sqlite3.connect("D:/Study/ISOB/Lab4/lab45/data/users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    return user
