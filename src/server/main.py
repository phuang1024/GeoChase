import argparse
import socket
from threading import Thread

from daemon import daemon
from handler import handle_client


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="")
    parser.add_argument("--port", type=int, default=4580)
    args = parser.parse_args()

    games = {}

    Thread(target=daemon, args=(games,)).start()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((args.host, args.port))
    sock.listen()
    print(f"Listening on {args.host}:{args.port}")

    while True:
        conn, addr = sock.accept()
        Thread(target=handle_client, args=(conn, addr, games)).start()


if __name__ == "__main__":
    main()
