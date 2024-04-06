"""
Networking utilities submodule.

Serialization is done with zlib_compress(json(obj))

Message protocol is:
Length of message as 4 bytes little-endian
Message (bytes).
"""

import json
import struct
import time
import zlib


def serialize(obj) -> bytes:
    return zlib.compress(json.dumps(obj).encode("utf-8"))


def deserialize(data: bytes):
    return json.loads(zlib.decompress(data).decode("utf-8"))


def send(sock, obj) -> None:
    data = serialize(obj)
    sock.sendall(struct.pack("<I", len(data)) + data)


def recv_len(sock, length: int, timeout: float = 3) -> bytes:
    """
    Receives until the specified length is reached.

    If the timeout is reached, raises exception.
    """
    sock.setblocking(False)
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
