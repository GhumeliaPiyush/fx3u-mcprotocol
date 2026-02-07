"""
Binary MC Protocol implementation for Mitsubishi FX3 series.

EXPERIMENTAL: Binary support depends on PLC firmware and adapter settings.
"""

from .exceptions import PLCError
import struct


class BinaryProtocol:
    """
    Binary MC Protocol backend (experimental).
    """

    _PC_NO = 0xFF
    _MONITOR_TIMER = 0x000A

    DEVICE_CODES = {
        "D": 0x4420,
        "M": 0x4D20,
        "X": 0x5820,
        "Y": 0x5920,
        "R": 0x5220,
    }

    @classmethod
    def build_read_words(cls, device: str, start: int, count: int) -> bytes:
        code = cls._get_device_code(device)

        return struct.pack(
            "<BBH H I H",
            0x01,              # command
            cls._PC_NO,
            cls._MONITOR_TIMER,
            code,
            start,
            count,
        )

    @classmethod
    def parse_read_words(cls, response: bytes, count: int) -> list[int]:
        if len(response) < 4:
            raise PLCError("Binary response too short")

        completion = struct.unpack_from("<H", response, 2)[0]
        if completion != 0:
            raise PLCError(f"PLC error completion code: {completion:04X}")

        values = []
        offset = 2
        for _ in range(count):
            values.append(struct.unpack_from("<H", response, offset)[0])
            offset += 2

        return values

    @classmethod
    def _get_device_code(cls, device: str) -> int:
        try:
            return cls.DEVICE_CODES[device]
        except KeyError:
            raise PLCError(f"Unsupported device for binary protocol: {device}")
