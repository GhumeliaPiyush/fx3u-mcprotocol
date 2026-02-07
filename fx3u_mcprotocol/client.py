"""
Public client API for fx3u-mcprotocol.

This module exposes a symbol-based interface for reading and writing
PLC memory while hiding protocol, transport, and CPU-specific details.
"""

from .transport import TCPTransport
from .symbols import parse_symbol
from .profiles import PROFILES
from .exceptions import (
    FX3UError,
    PLCError,
    SymbolError,
)

from .protocol_ascii import ASCIIProtocol
from .protocol_binary import BinaryProtocol


class FX3UClient:
    """
    Client for Mitsubishi FX3 series PLCs via FX3U-ENET-ADP.
    """

    def __init__(
        self,
        ip: str,
        port: int = 5001,
        cpu: str = "FX3U",
        mode: str = "ascii",
        timeout: float = 5.0,
        read_only: bool = False,
    ):
        self.ip = ip
        self.port = port
        self.mode = mode.lower()
        self.read_only = read_only

        # Select CPU profile
        cpu = cpu.upper()
        if cpu not in PROFILES:
            raise ValueError(
                f"Unsupported CPU '{cpu}'. Supported: {list(PROFILES.keys())}"
            )
        self.profile = PROFILES[cpu]

        # Select protocol backend
        if self.mode == "ascii":
            self.protocol = ASCIIProtocol
        elif self.mode == "binary":
            self.protocol = BinaryProtocol
        else:
            raise ValueError("mode must be 'ascii' or 'binary'")

        self.transport = TCPTransport(ip, port, timeout)

    # -------------------------------------------------
    # Connection handling
    # -------------------------------------------------

    def connect(self):
        """Connect to the PLC."""
        self.transport.connect()

    def close(self):
        """Close the PLC connection."""
        self.transport.close()

    # -------------------------------------------------
    # Read API
    # -------------------------------------------------

    def readReg(self, symbol: str) -> int:
        """Read a single word register."""
        values = self.readRegs(symbol, 1)
        return values[0]

    def readRegs(self, start: str, count: int) -> list[int]:
        """Read multiple word registers."""
        sym = parse_symbol(start)

        if sym.is_bit:
            raise SymbolError(f"{start} is a bit device; use readBit(s)")

        self.profile.validate(sym.device, sym.index, count)

        frame = self.protocol.build_read_words(
            sym.device, sym.index, count
        )
        self.transport.send(frame)
        response = self.transport.receive()

        return self.protocol.parse_read_words(response, count)

    def readBit(self, symbol: str) -> bool:
        """Read a single bit."""
        values = self.readBits(symbol, 1)
        return values[0]

    def readBits(self, start: str, count: int) -> list[bool]:
        """Read multiple bits."""
        sym = parse_symbol(start)

        if not sym.is_bit:
            raise SymbolError(f"{start} is a word device; use readReg(s)")

        self.profile.validate(sym.device, sym.index, count)

        frame = self.protocol.build_read_bits(
            sym.device, sym.index, count
        )
        self.transport.send(frame)
        response = self.transport.receive()

        return self.protocol.parse_read_bits(response, count)

    # -------------------------------------------------
    # Write API
    # -------------------------------------------------

    def writeReg(self, symbol: str, value: int):
        """Write a single word register."""
        self.writeRegs(symbol, [value])

    def writeRegs(self, start: str, values: list[int]):
        """Write multiple word registers."""
        if self.read_only:
            raise FX3UError("Client is in read-only mode")

        sym = parse_symbol(start)

        if sym.is_bit:
            raise SymbolError(f"{start} is a bit device; use writeBit(s)")

        self.profile.validate(sym.device, sym.index, len(values))

        if not hasattr(self.protocol, "build_write_words"):
            raise FX3UError("Write not supported by selected protocol")

        frame = self.protocol.build_write_words(
            sym.device, sym.index, values
        )
        self.transport.send(frame)
        response = self.transport.receive()

        # completion check
        self.protocol.parse_write_response(response)

    def writeBit(self, symbol: str, value: bool):
        """Write a single bit."""
        self.writeBits(symbol, [value])

    def writeBits(self, start: str, values: list[bool]):
        """Write multiple bits."""
        if self.read_only:
            raise FX3UError("Client is in read-only mode")

        sym = parse_symbol(start)

        if not sym.is_bit:
            raise SymbolError(f"{start} is a word device; use writeReg(s)")

        self.profile.validate(sym.device, sym.index, len(values))

        if not hasattr(self.protocol, "build_write_bits"):
            raise FX3UError("Write not supported by selected protocol")

        frame = self.protocol.build_write_bits(
            sym.device, sym.index, values
        )
        
        
        self.transport.send(frame)
        response = self.transport.receive()

        self.protocol.parse_write_response(response)
