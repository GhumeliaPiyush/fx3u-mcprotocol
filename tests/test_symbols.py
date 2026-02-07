import pytest
from fx3u_mcprotocol.symbols import parse_symbol
from fx3u_mcprotocol.exceptions import SymbolError


def test_parse_word_symbol():
    s = parse_symbol("D100")
    assert s.device == "D"
    assert s.index == 100
    assert not s.is_bit


def test_parse_bit_symbol():
    s = parse_symbol("M8000")
    assert s.device == "M"
    assert s.index == 8000
    assert s.is_bit


def test_invalid_symbol():
    with pytest.raises(SymbolError):
        parse_symbol("Q100")


def test_negative_index():
    with pytest.raises(SymbolError):
        parse_symbol("D-1")
