"""
ASCII MC Protocol implementation for Mitsubishi FX3 series
via FX3U-ENET-ADP.

This module builds and parses ASCII MC Protocol frames.
It does NOT handle sockets, symbols, or CPU validation.
"""

from .exceptions import PLCError


class ASCIIProtocol:
    """
    ASCII MC Protocol backend (stable).
    """

    # ---- Fixed protocol fields (ASCII) ----
    _PC_NO = "FF"
    _MONITOR_TIMER = "000A"  # 2.5 s (recommended default)

    # ---- Device codes (ASCII, internal use only) ----
    DEVICE_CODES = {
        "D": "4420",
        "M": "4D20",
        "X": "5820",
        "Y": "5920",
        "R": "5220",
    }

    # ---- Public API ----

    @classmethod
    def build_read_words(cls, device: str, start: int, count: int) -> bytes:
        """
        Build ASCII frame to read word devices.
        """
        device_code = cls._get_device_code(device)

        address = f"{start:08X}"
        count_field = f"{count:02X}00"  # little-endian count

        frame = (
            "01"                      # command: batch read (word)
            + cls._PC_NO
            + cls._MONITOR_TIMER
            + device_code
            + address
            + count_field
        )
        return frame.encode("ascii")

    @classmethod
    def build_read_bits(cls, device: str, start: int, count: int) -> bytes:
        """
        Build ASCII frame to read bit devices.
        """
        device_code = cls._get_device_code(device)

        address = f"{start:08X}"
        count_field = f"{count:02X}00"

        frame = (
            "00"                      # command: batch read (bit)
            + cls._PC_NO
            + cls._MONITOR_TIMER
            + device_code
            + address
            + count_field
        )
        return frame.encode("ascii")

    @classmethod
    def parse_read_words(cls, response: bytes, count: int) -> list[int]:
        """
        Parse ASCII response for word reads.
        Returns a list of integers.
        """
        text = response.decode("ascii", errors="ignore")

        cls._check_completion(text)

        data = text[4:]  # skip subheader + completion
        values = []

        for i in range(count):
            raw = data[i * 4:(i + 1) * 4]
            # ASCII is high→low, value is low→high
            swapped = raw[2:4] + raw[0:2]
            values.append(int(swapped, 16))

        return values

    @classmethod
    def parse_read_bits(cls, response: bytes, count: int) -> list[bool]:
        """
        Parse ASCII response for bit reads.
        """
        text = response.decode("ascii", errors="ignore")

        cls._check_completion(text)

        data = text[4:]
        return [char == "1" for char in data[:count]]

    # ---- Internal helpers ----

    @classmethod
    def _check_completion(cls, text: str):
        completion = text[2:4]
        if completion != "00":
            raise PLCError(f"PLC error completion code: {completion}")

    @classmethod
    def _get_device_code(cls, device: str) -> str:
        try:
            return cls.DEVICE_CODES[device]
        except KeyError:
            raise PLCError(f"Unsupported device for ASCII protocol: {device}")
