# import random
# import time
#
# import tkinter as tk
# from tkinter import messagebox
# import random
# import time
#
# from des import Des
# from ast import literal_eval as make_tuple
#
# current_milli_time = lambda: int(round(time.time() * 1000))
# hours_to_milli = lambda hour: hour * 3600 * 10000
#
#
# class DesEncrypter:
#     def encrypt(self, data, key):
#         # print('Before encrypt:', data)
#         encrypted = Des().encrypt(key=str(key), text=str(data), padding=True)
#         # print('After encrypt:', encrypted)
#         return encrypted
#
#     def decrypt(self, data, key):
#         # print('Before decrypt:', data)
#         decrypted = Des().decrypt(key=str(key), text=str(data), padding=True)
#         decrypted = make_tuple(decrypted)
#         # print('After decrypt:', decrypted)
#         return decrypted
#
#
# class KeyCreator:
#     @staticmethod
#     def create_key():
#         return random.randint(100000000, 999999999)
#
#
# class KDC:
#     available_clients = ['client1', 'client2']
#     clients_keys = [KeyCreator.create_key(), KeyCreator.create_key()]
#     available_servers = ['server1', 'server2']
#     servers_keys = [KeyCreator.create_key(), KeyCreator.create_key()]
#
#     def __init__(self):
#         self.des = DesEncrypter()
#         self.tgs_id = 1
#         self.key_tgs = KeyCreator.create_key()
#
#     def get_permission_ticket(self, client_id):
#         print('New call ticket:')
#         if client_id in self.available_clients:
#             t = current_milli_time()
#             p = hours_to_milli(48)
#             key_tgs_c = KeyCreator.create_key()
#             ticket = self.build_permission_ticket(client_id, self.tgs_id, t, p, key_tgs_c)
#             print('New call ticket:', ticket)
#
#             encrypted_ticket = self.des.encrypt(ticket, self.key_tgs)
#             bundle = (encrypted_ticket, key_tgs_c)
#
#             index = self.available_clients.index(client_id)
#             client_key = self.clients_keys[index]
#             encrypted_bundle = self.des.encrypt(bundle, client_key)
#
#             return encrypted_bundle
#
#         print('Unknown id client')
#
#     def get_server_ticket(self, permission_ticket, authority, server_id):
#         print('New call ticket')
#         permission_ticket = self.des.decrypt(permission_ticket, self.key_tgs)
#         client_id = permission_ticket[0]
#         t = permission_ticket[2]
#         p = permission_ticket[3]
#         key_tgs_c = permission_ticket[4]
#
#         print(
#             'Data ----- '
#             'id: {},'
#             'timestamp: {},'
#             'period: {}, '
#             'key TGS-Client: {}'.format(client_id, t, p, key_tgs_c))
#
#         authority = self.des.decrypt(authority, key_tgs_c)
#         auth_client_id = authority[0]
#         auth_t = authority[1]
#
#         print('Data for avtomatization ---- '
#               'client id: {}, '
#               'timestamp: {}'.format(auth_client_id, auth_t))
#
#         if client_id != auth_client_id:
#             print('Invalid client')
#             return None
#         if auth_t < t or auth_t > t + p:
#             print('Expired')
#             return None
#
#         t = current_milli_time()
#         p = hours_to_milli(48)
#         key_ss_c = KeyCreator.create_key()
#         server_ticket = self.build_server_ticket(client_id, server_id, t, p, key_ss_c)
#         print('New server ticket:', server_ticket)
#
#         index = self.available_servers.index(server_id)
#         server_key = self.servers_keys[index]
#         encrypted_server_ticket = self.des.encrypt(server_ticket, server_key)
#         bundle = (encrypted_server_ticket, key_ss_c)
#         encrypted_bundle = self.des.encrypt(bundle, key_tgs_c)
#         return encrypted_bundle
#
#     @staticmethod
#     def build_permission_ticket(client_id, tgs, t, p, key_tgs_c):
#         return client_id, tgs, t, p, key_tgs_c
#
#     @staticmethod
#     def build_server_ticket(client_id, server_id, t, p, key_ss_c):
#         return client_id, server_id, t, p, key_ss_c
#
#
# class Client:
#     def __init__(self, client_id, client_key, kdc, servers):
#         self.client_id = client_id
#         self.client_key = client_key
#         self.kdc = kdc
#         self.servers = servers
#         self.des = DesEncrypter()
#         self.permission_ticket = None
#         self.key_tgs_c = None
#
#     def make_server_call(self, server_number):
#         print()
#         print()
#         print('Call server', server_number)
#         server = self.servers[server_number]
#
#         if self.permission_ticket is None or self.key_tgs_c is None:
#             print('Attempting to take a permission ticket')
#             permission_ticket_bundle = self.kdc.get_permission_ticket(self.client_id)
#             if permission_ticket_bundle is None:
#                 return
#
#             permission_ticket_bundle = self.des.decrypt(permission_ticket_bundle, self.client_key)
#
#             permission_ticket = permission_ticket_bundle[0]
#             key_tgs_c = permission_ticket_bundle[1]
#             print('Key TGS-Client:', key_tgs_c)
#
#             self.permission_ticket = permission_ticket
#             self.key_tgs_c = key_tgs_c
#         else:
#             print('The permission ticket and TGS-Client key are already defined')
#             permission_ticket = self.permission_ticket
#             key_tgs_c = self.key_tgs_c
#
#         print()
#         print('Trying to get a ticket to the server')
#         bundle = self.__call_tgs(permission_ticket, key_tgs_c, server.server_id)
#         if bundle is None:
#             return
#         bundle = self.des.decrypt(bundle, key_tgs_c)
#
#         server_ticket = bundle[0]
#         key_ss_c = bundle[1]
#         print('Key Server-Client:', key_ss_c)
#
#         print()
#         print('Attempting to connect to the server')
#         t = current_milli_time()
#         authority = (self.client_id, t)
#         authority_enctypted = self.des.encrypt(authority, key_ss_c)
#         confirm_t = server.connect(server_ticket, authority_enctypted)
#         if confirm_t is None:
#             return
#         confirm_t = self.des.decrypt(confirm_t, key_ss_c)
#         if confirm_t != t + 1:
#             print('Server returns incorrect timestamp')
#             return
#
#         print()
#         print('Server call successful')
#
#     def __call_tgs(self, permission_ticket, key_tgs_c, server_id):
#         t = current_milli_time()
#         print('Call TGS. '
#               'Server id: {}, '
#               'timestamp: {}'.format(server_id, t))
#         authority = (self.client_id, t)
#         authority_enctypted = self.des.encrypt(authority, key_tgs_c)
#         bundle = self.kdc.get_server_ticket(permission_ticket, authority_enctypted, server_id)
#         return bundle
#
#
# class Server:
#     def __init__(self, server_id, server_key):
#         self.server_id = server_id
#         self.server_key = server_key
#         self.des = DesEncrypter()
#
#     def connect(self, server_ticket, authority):
#         print('New server connection')
#         server_ticket = self.des.decrypt(server_ticket, self.server_key)
#         client_id = server_ticket[0]
#         server_id = server_ticket[1]
#         t = server_ticket[2]
#         p = server_ticket[3]
#         key_ss_c = server_ticket[4]
#
#         print('Data ticket server ---- '
#               'Client id: {}, '
#               'timestamp: {}, '
#               'period: {},'
#               'key Server-Client: {}'.format(client_id, t, p, key_ss_c))
#
#         if server_id != self.server_id:
#             print('Unknown server')
#             return None
#
#         authority = self.des.decrypt(authority, key_ss_c)
#         auth_client_id = authority[0]
#         auth_t = authority[1]
#
#         print('Authorization data ---- '
#               'Client id: {}, '
#               'timestamp: {}'.format(auth_client_id, auth_t))
#
#         if client_id != auth_client_id:
#             print('Invalid client')
#             return None
#         if auth_t < t or auth_t > t + p:
#             print('Ticket is expired')
#             return None
#
#         confirm_t = auth_t + 1
#         print('Confirmation timestamp is', confirm_t)
#         encrypted_confirm_t = self.des.encrypt(confirm_t, key_ss_c)
#         return encrypted_confirm_t
#
#
# def initialization_client():
#     kdc = KDC()
#     server1 = Server(kdc.available_servers[0], kdc.servers_keys[0])
#     server2 = Server(kdc.available_servers[1], kdc.servers_keys[1])
#
#     client = Client(kdc.available_clients[0], kdc.clients_keys[0], kdc, [server1, server2])
#
#     print('server0 id: {}, server0 key: {}'.format(server1.server_id, server1.server_key))
#     print('server1 id: {}, server1" key: {}'.format(server2.server_id, server2.server_key))
#     print('Client id: {}, Client key: {}'.format(client.client_id, client.client_key))
#
#     return client
#
#
# # client = initialization_client()
# # client.make_server_call(0)
# # # client.make_server_call(1)
#
#
# class Application(tk.Tk):
#     def __init__(self):
#         super().__init__()
#         self.title("Client Server Communication")
#         self.geometry("400x300")
#         self.client = initialization_client()
#         self.create_widgets()
#
#     def create_widgets(self):
#         self.server1_button = tk.Button(self, text="Call Server 1", command=self.call_server_1)
#         self.server1_button.pack(pady=(50, 10), padx=10, fill="x")
#
#         self.server2_button = tk.Button(self, text="Call Server 2", command=self.call_server_2)
#         self.server2_button.pack(pady=(100, 10), padx=10, fill="x")
#
#     def call_server_1(self):
#         self.make_server_call(0)
#
#     def call_server_2(self):
#         self.make_server_call(1)
#
#     def make_server_call(self, server_number):
#         try:
#             self.client.make_server_call(server_number)
#             messagebox.showinfo("Success", "Server call successful")
#         except Exception as e:
#             messagebox.showerror("Error", str(e))
#
#
# if __name__ == "__main__":
#     app = Application()
#     app.mainloop()
import tkinter as tk
from tkinter import messagebox
import random
import time
from des import Des
from ast import literal_eval as make_tuple

current_milli_time = lambda: int(round(time.time() * 1000))
hours_to_milli = lambda hour: hour * 3600 * 10000


class DesEncrypter:
    def __init__(self):
        self.logs = ""

    def encrypt(self, data, key):
        encrypted = Des().encrypt(key=str(key), text=str(data), padding=True)
        return encrypted

    def decrypt(self, data, key):
        decrypted = Des().decrypt(key=str(key), text=str(data), padding=True)
        decrypted = make_tuple(decrypted)
        return decrypted

    def log(self, message):
        self.logs += message + "\n"


class KeyCreator:
    @staticmethod
    def create_key():
        return random.randint(100000000, 999999999)


class KDC:
    available_clients = ['client1', 'client2']
    clients_keys = [KeyCreator.create_key(), KeyCreator.create_key()]
    available_servers = ['server1', 'server2']
    servers_keys = [KeyCreator.create_key(), KeyCreator.create_key()]

    def __init__(self, logger):
        self.des = DesEncrypter()
        self.tgs_id = 1
        self.key_tgs = KeyCreator.create_key()
        self.logger = logger

    def get_permission_ticket(self, client_id):
        self.logger.log('New call ticket:')
        if client_id in self.available_clients:
            t = current_milli_time()
            p = hours_to_milli(48)
            key_tgs_c = KeyCreator.create_key()
            ticket = self.build_permission_ticket(client_id, self.tgs_id, t, p, key_tgs_c)
            self.logger.log('New call ticket: {}'.format(ticket))

            encrypted_ticket = self.des.encrypt(ticket, self.key_tgs)
            bundle = (encrypted_ticket, key_tgs_c)

            index = self.available_clients.index(client_id)
            client_key = self.clients_keys[index]
            encrypted_bundle = self.des.encrypt(bundle, client_key)

            return encrypted_bundle

        self.logger.log('Unknown id client')

    def get_server_ticket(self, permission_ticket, authority, server_id):
        self.logger.log('New call ticket')
        permission_ticket = self.des.decrypt(permission_ticket, self.key_tgs)
        client_id = permission_ticket[0]
        t = permission_ticket[2]
        p = permission_ticket[3]
        key_tgs_c = permission_ticket[4]

        self.logger.log(
            'Data ----- '
            'id: {},'
            'timestamp: {},'
            'period: {}, '
            'key TGS-Client: {}'.format(client_id, t, p, key_tgs_c))

        authority = self.des.decrypt(authority, key_tgs_c)
        auth_client_id = authority[0]
        auth_t = authority[1]

        self.logger.log('Data for avtomatization ---- '
                        'client id: {}, '
                        'timestamp: {}'.format(auth_client_id, auth_t))

        if client_id != auth_client_id:
            self.logger.log('Invalid client')
            return None
        if auth_t < t or auth_t > t + p:
            self.logger.log('Expired')
            return None

        t = current_milli_time()
        p = hours_to_milli(48)
        key_ss_c = KeyCreator.create_key()
        server_ticket = self.build_server_ticket(client_id, server_id, t, p, key_ss_c)
        self.logger.log('New server ticket: {}'.format(server_ticket))

        index = self.available_servers.index(server_id)
        server_key = self.servers_keys[index]
        encrypted_server_ticket = self.des.encrypt(server_ticket, server_key)
        bundle = (encrypted_server_ticket, key_ss_c)
        encrypted_bundle = self.des.encrypt(bundle, key_tgs_c)
        return encrypted_bundle

    @staticmethod
    def build_permission_ticket(client_id, tgs, t, p, key_tgs_c):
        return client_id, tgs, t, p, key_tgs_c

    @staticmethod
    def build_server_ticket(client_id, server_id, t, p, key_ss_c):
        return client_id, server_id, t, p, key_ss_c


class Client:
    def __init__(self, client_id, client_key, kdc, servers, logger):
        self.client_id = client_id
        self.client_key = client_key
        self.kdc = kdc
        self.servers = servers
        self.des = DesEncrypter()
        self.permission_ticket = None
        self.key_tgs_c = None
        self.logger = logger

    def make_server_call(self, server_number):
        self.logger.log('')
        self.logger.log('')
        self.logger.log('Call server {}'.format(server_number))
        server = self.servers[server_number]

        if self.permission_ticket is None or self.key_tgs_c is None:
            self.logger.log('Attempting to take a permission ticket')
            permission_ticket_bundle = self.kdc.get_permission_ticket(self.client_id)
            if permission_ticket_bundle is None:
                return

            permission_ticket_bundle = self.des.decrypt(permission_ticket_bundle, self.client_key)

            permission_ticket = permission_ticket_bundle[0]
            key_tgs_c = permission_ticket_bundle[1]
            self.logger.log('Key TGS-Client: {}'.format(key_tgs_c))

            self.permission_ticket = permission_ticket
            self.key_tgs_c = key_tgs_c
        else:
            self.logger.log('The permission ticket and TGS-Client key are already defined')
            permission_ticket = self.permission_ticket
            key_tgs_c = self.key_tgs_c

        self.logger.log('')
        self.logger.log('Trying to get a ticket to the server')
        bundle = self.__call_tgs(permission_ticket, key_tgs_c, server.server_id)
        if bundle is None:
            return
        bundle = self.des.decrypt(bundle, key_tgs_c)

        server_ticket = bundle[0]
        key_ss_c = bundle[1]
        self.logger.log('Key Server-Client: {}'.format(key_ss_c))

        self.logger.log('')
        self.logger.log('Attempting to connect to the server')
        t = current_milli_time()
        authority = (self.client_id, t)
        authority_enctypted = self.des.encrypt(authority, key_ss_c)
        confirm_t = server.connect(server_ticket, authority_enctypted)
        if confirm_t is None:
            return
        confirm_t = self.des.decrypt(confirm_t, key_ss_c)
        if confirm_t != t + 1:
            self.logger.log('Server returns incorrect timestamp')
            return

        self.logger.log('')
        self.logger.log('Server call successful')

    def __call_tgs(self, permission_ticket, key_tgs_c, server_id):
        t = current_milli_time()
        self.logger.log('Call TGS. '
                        'Server id: {}, '
                        'timestamp: {}'.format(server_id, t))
        authority = (self.client_id, t)
        authority_enctypted = self.des.encrypt(authority, key_tgs_c)
        bundle = self.kdc.get_server_ticket(permission_ticket, authority_enctypted, server_id)
        return bundle


class Server:
    def __init__(self, server_id, server_key, logger):
        self.server_id = server_id
        self.server_key = server_key
        self.des = DesEncrypter()
        self.logger = logger

    def connect(self, server_ticket, authority):
        self.logger.log('New server connection')
        server_ticket = self.des.decrypt(server_ticket, self.server_key)
        client_id = server_ticket[0]
        server_id = server_ticket[1]
        t = server_ticket[2]
        p = server_ticket[3]
        key_ss_c = server_ticket[4]

        self.logger.log('Data ticket server ---- '
                        'Client id: {}, '
                        'timestamp: {}, '
                        'period: {},'
                        'key Server-Client: {}'.format(client_id, t, p, key_ss_c))

        if server_id != self.server_id:
            self.logger.log('Unknown server')
            return None

        authority = self.des.decrypt(authority, key_ss_c)
        auth_client_id = authority[0]
        auth_t = authority[1]

        self.logger.log('Authorization data ---- '
                        'Client id: {}, '
                        'timestamp: {}'.format(auth_client_id, auth_t))

        if client_id != auth_client_id:
            self.logger.log('Invalid client')
            return None
        if auth_t < t or auth_t > t + p:
            self.logger.log('Ticket is expired')
            return None

        confirm_t = auth_t + 1
        self.logger.log('Confirmation timestamp is {}'.format(confirm_t))
        encrypted_confirm_t = self.des.encrypt(confirm_t, key_ss_c)
        return encrypted_confirm_t


class Logger:
    def __init__(self):
        self.logs = ""

    def log(self, message):
        self.logs += message + "\n"


def initialization_client(logger):
    kdc = KDC(logger)
    server1 = Server(kdc.available_servers[0], kdc.servers_keys[0], logger)
    server2 = Server(kdc.available_servers[1], kdc.servers_keys[1], logger)

    client = Client(kdc.available_clients[0], kdc.clients_keys[0], kdc, [server1, server2], logger)

    logger.log('server0 id: {}, server0 key: {}'.format(server1.server_id, server1.server_key))
    logger.log('server1 id: {}, server1" key: {}'.format(server2.server_id, server2.server_key))
    logger.log('Client id: {}, Client key: {}'.format(client.client_id, client.client_key))

    return client, kdc


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Client Server Communication")
        self.geometry("400x300")
        self.logger = Logger()
        self.client, self.kdc = initialization_client(self.logger)
        self.create_widgets()
        self.create_logger_window()

    def create_widgets(self):
        self.server1_button = tk.Button(self, text="Call Server 0", command=self.call_server_1)
        self.server1_button.pack(pady=(50, 10), padx=10, fill="x")

        self.server2_button = tk.Button(self, text="Call Server 1", command=self.call_server_2)
        self.server2_button.pack(pady=(100, 10), padx=10, fill="x")

    def create_logger_window(self):
        self.logger_window = tk.Toplevel(self)
        self.logger_window.title("Logs")
        self.logger_text = tk.Text(self.logger_window, wrap="word")
        self.logger_text.pack(expand=True, fill="both")
        self.logger_text.insert(tk.END, self.logger.logs)
        self.logger_text.config(state=tk.DISABLED)

    def update_logger_window(self):
        self.logger_text.config(state=tk.NORMAL)
        self.logger_text.delete("1.0", tk.END)
        self.logger_text.insert(tk.END, self.logger.logs)
        self.logger_text.config(state=tk.DISABLED)

    def call_server_1(self):
        self.client.make_server_call(0)
        self.update_logger_window()

    def call_server_2(self):
        self.client.make_server_call(1)
        self.update_logger_window()


if __name__ == "__main__":
    app = Application()
    app.mainloop()
