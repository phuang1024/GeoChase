import argparse
import socket
from threading import Thread

from utils import *


def handle_client(conn, addr):
    obj = recv(conn)

    if not isinstance(obj, dict) or "type" not in obj:
        print(f"{addr}: Invalid message")
        conn.close()
        return

    print(f"{addr}: {obj['type']}")

    if obj["type"] == "echo":
        send(conn, obj["echo"])

    # TODO stuff.


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="")
    parser.add_argument("--port", type=int, default=6645)
    args = parser.parse_args()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((args.host, args.port))
    sock.listen()
    print(f"Listening on {args.host}:{args.port}")

    while True:
        conn, addr = sock.accept()
        Thread(target=handle_client, args=(conn, addr)).start()


if __name__ == "__main__":
    main()
