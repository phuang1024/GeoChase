import socket

import network


def main():
    # test
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("", 12345))
    sock.listen(1)
    conn, addr = sock.accept()
    print(addr)
    while True:
        obj = network.recv(conn)
        print(obj)
        network.send(conn, obj)


if __name__ == "__main__":
    main()
