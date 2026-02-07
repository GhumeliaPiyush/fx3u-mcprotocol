import pytest
from fx3u_mcprotocol.client import FX3UClient
from fx3u_mcprotocol.exceptions import SymbolError


def test_client_init():
    plc = FX3UClient("127.0.0.1", cpu="FX3U")
    assert plc.profile.name == "FX3U"


def test_wrong_cpu():
    with pytest.raises(ValueError):
        FX3UClient("127.0.0.1", cpu="FX1S")


def test_bit_vs_word_guard():
    plc = FX3UClient("127.0.0.1")

    with pytest.raises(SymbolError):
        plc.readRegs("M100", 1)

    with pytest.raises(SymbolError):
        plc.readBits("D100", 1)
