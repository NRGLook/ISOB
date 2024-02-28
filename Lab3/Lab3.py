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


def run_attacks():
    client = Member(123, 1)
    server1 = Member(321, 3)
    server2 = HackerMember(231, 2)

    tcpResetMiddleware = TcpResetMiddleware()
    fakeIpAddressMiddleware = FakeIpAddressMiddleware(231, 2)
    rstMiddleware = RSTMiddleware()
    connectionHijack = ConnectionHijack()
    connection = Connection([client, server1, server2], [rstMiddleware])

    client.callAnyOther(connection)


run_attacks()