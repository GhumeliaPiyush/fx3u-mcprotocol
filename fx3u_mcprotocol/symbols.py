"""
Symbol parsing utilities for fx3u-mcprotocol.

This module converts user-facing symbols like:
    D100, M8000, X10, Y20, R5

into a normalized internal representation.

No protocol or transport logic belongs here.
"""

import re
from dataclasses import dataclass
from .exceptions import SymbolError

# Supported devices
BIT_DEVICES = {"M", "X", "Y"}
WORD_DEVICES = {"D", "R", "TN", "TS", "CN", "CS"}

# Regex: device letters + decimal index
_SYMBOL_RE = re.compile(r"^([A-Za-z]+)(\d+)$")


@dataclass(frozen=True)
class Symbol:
    device: str
    index: int
    is_bit: bool


def parse_symbol(symbol: str) -> Symbol:
    """
    Parse a PLC memory symbol (e.g. 'D100', 'M8000').

    Returns:
        Symbol(device, index, is_bit)

    Raises:
        SymbolError if the symbol is invalid or unsupported.
    """
    if not isinstance(symbol, str):
        raise SymbolError("Symbol must be a string")

    match = _SYMBOL_RE.match(symbol.strip().upper())
    if not match:
        raise SymbolError(f"Invalid symbol format: {symbol}")

    device, index_str = match.groups()
    index = int(index_str)

    if device in BIT_DEVICES:
        is_bit = True
    elif device in WORD_DEVICES:
        is_bit = False
    else:
        raise SymbolError(f"Unsupported device type: {device}")

    if index < 0:
        raise SymbolError("Symbol index must be non-negative")

    return Symbol(device=device, index=index, is_bit=is_bit)
