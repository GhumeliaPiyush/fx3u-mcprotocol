"""
Exception hierarchy for fx3u-mcprotocol.

All library-specific exceptions inherit from FX3UError so that users
can catch errors at different levels of granularity.
"""


class FX3UError(Exception):
    """
    Base exception for all fx3u-mcprotocol errors.
    """
    pass


class ConnectionError(FX3UError):
    """
    Raised when TCP connection or communication fails.
    """
    pass


class PLCError(FX3UError):
    """
    Raised when the PLC returns an error completion code.
    """
    pass


class SymbolError(FX3UError):
    """
    Raised when an invalid or unsupported PLC memory symbol is used.
    """
    pass
