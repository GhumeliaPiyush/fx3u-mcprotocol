"""
TCP transport layer for fx3u-mcprotocol.

This module is responsible ONLY for socket communication.
It has no knowledge of MC Protocol, symbols, or PLC memory.
"""

import socket
from .exceptions import ConnectionError


class TCPTransport:
    def __init__(self, ip: str, port: int, timeout: float = 5.0):
        self.ip = ip
        self.port = port
        self.timeout = timeout
        self._sock: socket.socket | None = None

    def connect(self):
        """
        Establish a TCP connection to the PLC Ethernet adapter.
        """
        if self._sock is not None:
            return

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            sock.connect((self.ip, self.port))
            self._sock = sock
        except Exception as exc:
            self._sock = None
            raise ConnectionError(
                f"Failed to connect to {self.ip}:{self.port} - {exc}"
            )

    def send(self, data: bytes):
        """
        Send raw bytes to the PLC.
        """
        if not self._sock:
            raise ConnectionError("Not connected to PLC")

        try:
            self._sock.sendall(data)
        except Exception as exc:
            raise ConnectionError(f"Failed to send data: {exc}")

    def receive(self, size: int = 4096) -> bytes:
        """
        Receive raw bytes from the PLC.
        """
        if not self._sock:
            raise ConnectionError("Not connected to PLC")

        try:
            return self._sock.recv(size)
        except Exception as exc:
            raise ConnectionError(f"Failed to receive data: {exc}")

    def close(self):
        """
        Close the TCP connection.
        """
        if self._sock:
            try:
                self._sock.close()
            finally:
                self._sock = None
