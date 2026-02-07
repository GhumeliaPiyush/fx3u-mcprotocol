"""
PLC CPU memory profiles for fx3u-mcprotocol.

This module defines valid memory ranges for different FX3 CPUs.
Ranges are based on publicly available Mitsubishi documentation
and may vary depending on firmware or expansion modules.
"""

from .exceptions import SymbolError


class PLCProfile:
    """
    Defines valid memory ranges for a PLC CPU model.
    """

    def __init__(self, name: str, limits: dict[str, int]):
        self.name = name
        self.limits = limits

    def validate(self, device: str, start: int, count: int = 1):
        """
        Validate that a memory access is legal for this CPU.

        Raises:
            SymbolError if the access is out of range.
        """
        if device not in self.limits:
            # Devices without defined limits are allowed for now
            return

        if count <= 0:
            raise SymbolError("Count must be positive")

        end = start + count - 1
        max_addr = self.limits[device]

        if start < 0 or end > max_addr:
            raise SymbolError(
                f"{device}{start}..{device}{end} out of range for {self.name} "
                f"(max {device}{max_addr})"
            )


# ----------------------------
# FX3 CPU PROFILES
# ----------------------------

FX3S = PLCProfile(
    "FX3S",
    limits={
        "D": 7999,
        "M": 4095,
        "X": 255,
        "Y": 255,
        "R": 7999,
    },
)

FX3G = PLCProfile(
    "FX3G",
    limits={
        "D": 7999,
        "M": 8191,
        "X": 511,
        "Y": 511,
        "R": 7999,
    },
)

FX3GC = PLCProfile(
    "FX3GC",
    limits={
        "D": 7999,
        "M": 8191,
        "X": 511,
        "Y": 511,
        "R": 7999,
    },
)

FX3U = PLCProfile(
    "FX3U",
    limits={
        "D": 7999,
        "M": 16383,
        "X": 1023,
        "Y": 1023,
        "R": 7999,
    },
)

# Public registry
PROFILES = {
    "FX3S": FX3S,
    "FX3G": FX3G,
    "FX3GC": FX3GC,
    "FX3U": FX3U,
}
