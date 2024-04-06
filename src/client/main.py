import socket

from utils import network


def main():
    # test
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("", 12345))
    obj = {
        "test": [1, 2, 3],
        "test2": True,
    }
    print("obj:", obj)
    network.send(sock, obj)
    print("recv:", network.recv(sock))


if __name__ == "__main__":
    main()
