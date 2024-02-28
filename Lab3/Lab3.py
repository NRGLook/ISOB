import time

from Members import Member, HackerMember
from Middleware import TcpResetMiddleware, FakeIpAddressMiddleware, RSTMiddleware
from Connection import ConnectionHijack, Connection


def print_package(package):
    try:
        time.sleep(1.5)
    except KeyboardInterrupt:
        raise BaseException("Interrupted by user")

    print("Next package. {}".format(package))


def initialize_network():
    client = Member(123, 1)
    server1 = Member(321, 3)
    server2 = HackerMember(231, 2)
    return client, server1, server2


def initialize_middlewares():
    tcp_reset_middleware = TcpResetMiddleware()
    fake_ip_address_middleware = FakeIpAddressMiddleware(231, 2)
    rst_middleware = RSTMiddleware()
    connection_hijack = ConnectionHijack()
    return tcp_reset_middleware, fake_ip_address_middleware, rst_middleware, connection_hijack


def create_connection(client, server1, server2, middlewares):
    connection = Connection([client, server1, server2], middlewares)
    return connection


def run_attacks():
    client, server1, server2 = initialize_network()
    middlewares = initialize_middlewares()
    connection = create_connection(client, server1, server2, middlewares)

    client.callAnyOther(connection)


run_attacks()
