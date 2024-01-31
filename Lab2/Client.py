import socket
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import pickle

# Функция для шифрования сообщения DES
def encrypt_message(key, message):
    cipher = Cipher(algorithms.TripleDES(key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()
    padded_message = message + b' ' * (8 - len(message) % 8)  # Добавляем дополнение до кратности 8
    encrypted_message = encryptor.update(padded_message) + encryptor.finalize()
    return encrypted_message

# Адрес и порт сервера
SERVER_ADDRESS = ('localhost', 12345)

# Создаем сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Подключаемся к серверу
    client_socket.connect(SERVER_ADDRESS)

    # Отправляем запрос на аутентификацию
    client_socket.sendall(b'Authentication request')

    # Получаем билет от Kerberos
    ticket = client_socket.recv(1024)  # Размер буфера для получения билета

    # Пример данных, которые могут быть зашифрованы DES
    message = b'Hello, server!'

    # Ключ DES (предварительно обмененный с Kerberos)
    des_key = b'secret_k'  # Предполагается, что ключ будет сгенерирован и обменен с Kerberos

    # Шифруем сообщение DES
    encrypted_message = encrypt_message(des_key, message)

    # Отправляем зашифрованное сообщение и билет серверу
    data_to_send = {'encrypted_message': encrypted_message, 'ticket': ticket}
    client_socket.sendall(pickle.dumps(data_to_send))

    # Получаем ответ от сервера
    response = client_socket.recv(1024)

    # Выводим ответ
    print("Response from server:", response.decode())

except Exception as e:
    print("Error:", e)

finally:
    # Закрываем сокет
    client_socket.close()
