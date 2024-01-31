from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import socket
import pickle
import base64

# Функция для расшифровки сообщения DES
def decrypt_message(key, encrypted_message):
    cipher = Cipher(algorithms.TripleDES(key), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(encrypted_message) + decryptor.finalize()
    return decrypted_message.rstrip(b' ')  # Удаляем дополнение

# Адрес и порт сервера
SERVER_ADDRESS = ('localhost', 12345)
KERBEROS_SERVER_ADDRESS = ('localhost', 12346)

# Создаем сокет для сервера
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(SERVER_ADDRESS)
server_socket.listen(1)

# Соединяемся с Kerberos-сервером для получения билета
kerberos_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
kerberos_client_socket.connect(KERBEROS_SERVER_ADDRESS)

try:
    # Отправляем запрос на аутентификацию к Kerberos-серверу
    kerberos_client_socket.sendall(b'Authentication request')

    # Получаем билет от Kerberos-сервера
    ticket = kerberos_client_socket.recv(1024)
    ticket = pickle.loads(ticket)  # Десериализуем билет

    print("Ticket received from Kerberos server:", ticket)

    while True:
        print("Server is waiting for connection...")
        client_socket, client_address = server_socket.accept()
        print("Connection established with:", client_address)

        try:
            # Получаем данные от клиента (зашифрованное сообщение и билет)
            data_from_client = client_socket.recv(1024)
            data_from_client = pickle.loads(data_from_client)
            received_ticket = pickle.loads(data_from_client['ticket'])
            encrypted_message = data_from_client['encrypted_message']

            # Декодируем билет с использованием ключа сессии
            # В реальном приложении здесь должна быть проверка на валидность билета и проверка аутентификации
            if received_ticket == ticket:
                session_key = base64.b64decode(ticket['session_key'].encode('utf-8'))

                # Расшифровываем сообщение с использованием ключа сессии
                decrypted_message = decrypt_message(session_key, encrypted_message)
                print("Decrypted message from client:", decrypted_message.decode())

                # Отправляем ответ клиенту
                response = b"Message received!"
                client_socket.sendall(response)

            else:
                print("Invalid ticket received from client!")

        except Exception as e:
            print("Error:", e)

        finally:
            # Закрываем соединение с клиентом
            client_socket.close()

finally:
    # Закрываем соединение с Kerberos-сервером
    kerberos_client_socket.close()
