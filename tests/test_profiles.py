import pytest
from fx3u_mcprotocol.profiles import FX3U
from fx3u_mcprotocol.exceptions import SymbolError


def test_valid_range():
    FX3U.validate("D", 100, 5)


def test_invalid_range():
    with pytest.raises(SymbolError):
        FX3U.validate("D", 8000, 1)


def test_bit_range():
    FX3U.validate("M", 8000, 1)
