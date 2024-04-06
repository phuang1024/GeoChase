import argparse
import socket

from utils import *


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="")
    parser.add_argument("--port", type=int, default=6645)
    args = parser.parse_args()

    # test
    resp = request(args.host, args.port, {"type": "echo", "echo": "Hello, world!"})
    print(resp)


if __name__ == "__main__":
    main()
