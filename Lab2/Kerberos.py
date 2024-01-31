import socket
import pickle
import base64


# Функция для генерации билета
def generate_ticket(client_id, session_key):
    session_key_str = base64.b64encode(session_key).decode('utf-8')
    return {'client_id': client_id, 'session_key': session_key_str}


# Адрес и порт сервера
KERBEROS_SERVER_ADDRESS = ('localhost', 12346)
SERVER_ADDRESS = ('localhost', 12345)

# Создаем сокет для Kerberos-сервера
kerberos_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
kerberos_server_socket.bind(KERBEROS_SERVER_ADDRESS)
kerberos_server_socket.listen(1)

# Генерируем ключ сессии для клиента
# В реальности это должно быть выполнено с использованием протокола обмена ключами
session_key = b'secret_key_for_session'

while True:
    print("Kerberos server is waiting for connection...")
    kerberos_client_socket, kerberos_client_address = kerberos_server_socket.accept()
    print("Connection established with:", kerberos_client_address)

    try:
        # Получаем запрос на аутентификацию от клиента
        authentication_request = kerberos_client_socket.recv(1024)

        # Здесь вы можете выполнить аутентификацию клиента

        # Генерируем билет для клиента
        ticket = generate_ticket(b'client_id', session_key)

        # Отправляем билет клиенту
        kerberos_client_socket.sendall(pickle.dumps(ticket))
        print("Ticket sent to client:", ticket)

    except Exception as e:
        print("Error:", e)

    finally:
        # Закрываем соединение с клиентом
        kerberos_client_socket.close()
