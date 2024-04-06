"""
Networking utilities submodule.

Serialization is done with pickle(obj)

Message protocol is:
Length of message as 4 bytes little-endian
Message (bytes).
"""

import pickle
import struct
import time


def serialize(obj) -> bytes:
    return pickle.dumps(obj)


def deserialize(data: bytes):
    return pickle.loads(data)


def send(sock, obj) -> None:
    data = serialize(obj)
    sock.sendall(struct.pack("<I", len(data)) + data)


def recv_len(sock, length: int, timeout: float = 3) -> bytes:
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
