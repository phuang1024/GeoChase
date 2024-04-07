__all__ = (
    "send",
    "recv",
    "request",
)

"""
Networking utilities submodule.

Serialization is done with pickle(obj)

Message protocol is:
Length of message as 4 bytes little-endian
Message (bytes).
"""

import pickle
import socket
import struct
import time


def serialize(obj) -> bytes:
    return pickle.dumps(obj)


def deserialize(data: bytes):
    return pickle.loads(data)


def send(sock, obj) -> None:
    data = serialize(obj)
    sock.sendall(struct.pack("<I", len(data)) + data)


def recv_len(sock, length: int, timeout: float = 300) -> bytes:
    """
    Receives until the specified length is reached.

    If the timeout is reached, raises exception.
    """
    time_start = time.time()

    data = b""
    while len(data) < length:
        data += sock.recv(length - len(data))
        if time.time() - time_start > timeout:
            raise TimeoutError()

    return data

def recv(sock):
    length = struct.unpack("<I", recv_len(sock, 4))[0]
    return deserialize(recv_len(sock, length))


def request(ip, port, obj):
    """
    Shorthand for creating sock, sending obj, and receiving response.

    Used client-side.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    send(sock, obj)
    response = recv(sock)
    sock.close()
    return response
