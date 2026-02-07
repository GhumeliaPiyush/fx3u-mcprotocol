# fx3u-mcprotocol — Python MC Protocol Library for Mitsubishi FX3 PLCs

[![PyPI](https://img.shields.io/pypi/v/fx3u-mcprotocol)](https://pypi.org/project/fx3u-mcprotocol/)
[![Python](https://img.shields.io/pypi/pyversions/fx3u-mcprotocol)](https://pypi.org/project/fx3u-mcprotocol/)
[![License](https://img.shields.io/pypi/l/fx3u-mcprotocol)](LICENSE)

**fx3u-mcprotocol** is an open-source **Python MC Protocol library**
for communicating with **Mitsubishi FX3 series PLCs over Ethernet**.

It allows Python applications to read PLC memory
(**D, M, X, Y, R devices**) from Mitsubishi FX3 PLCs using  
**MC Protocol (ASCII mode)** via Ethernet (TCP/IP).

The library is tested with **FX3U + FX3U-ENET-ADP** and is suitable for
industrial automation, data acquisition, SCADA integration,
and custom monitoring systems.

---

## Why fx3u-mcprotocol?

If you are searching for:

- *MC Protocol Python library*
- *Mitsubishi FX3 PLC Python communication*
- *FX3U Ethernet Python driver*
- *Read Mitsubishi PLC data using Python*

this library is designed exactly for that use case.

Unlike generic PLC libraries, **fx3u-mcprotocol focuses specifically on FX3 PLCs**
and provides a **simple, symbol-based API** aligned with real industrial workflows.

---

## Features

- Python MC Protocol implementation for Mitsubishi FX3 PLCs
- Symbol-based addressing (`D100`, `M8000`, etc.)
- Read word devices (D, R, TN, TS, …)
- Read bit devices (M, X, Y)
- Multiple PLC connections in a single application
- CPU profile validation (FX3S / FX3G / FX3U / FX3GC)
- Modular architecture (transport, protocol, symbols, profiles)
- Pure Python (no external runtime dependencies)

---

## Installation

Install the library directly from PyPI:

```bash
pip install fx3u-mcprotocol
```


## ✅ Stable ASCII MC Protocol support (FX3 series)
## ⚠️ Binary MC Protocol support is experimental and may vary by firmware

## Example

```python
from fx3u_mcprotocol import FX3UClient

plc = FX3UClient(
    ip="192.168.4.4",
    port=5001,
    cpu="FX3U",
    mode="ascii",
)

plc.connect()

# Read PLC registers (D devices)
print(plc.readReg("D100"))
print(plc.readRegs("D100", 3))

# Read PLC bits (M devices)
print(plc.readBit("M0"))
print(plc.readBits("M8000", 1))  # RUN bit

plc.close()


```
This example demonstrates how to read Mitsubishi FX3 PLC memory
using Python over Ethernet with MC Protocol.


## Supported Mitsubishi PLCs

- Mitsubishi FX3U
- Mitsubishi FX3G
- Mitsubishi FX3S
- Mitsubishi FX3GC



## Note
- The library is tested on FX3U + FX3U-ENET-ADP.
Other FX3 models are supported based on documented memory ranges.


## Multiple PLC Example (Polling)
``` python
from fx3u_mcprotocol import FX3UClient

plcs = {
    "PLC_1": "192.168.4.2",
    "PLC_2": "192.168.4.3",
}

clients = {}

for name, ip in plcs.items():
    plc = FX3UClient(ip=ip, cpu="FX3U", mode="ascii", read_only=True)
    plc.connect()
    clients[name] = plc

for name, plc in clients.items():
    print(name, plc.readRegs("D100", 3))

```
This approach is commonly used for:

* Data logging

* Multi-machine monitoring

* SCADA gateway development


## Architecture Overview

The library is intentionally modular:

* transport — TCP/IP socket communication

* protocol — MC Protocol frame encoding/decoding

* symbols — PLC symbol parsing (D100, M8000)

* profiles — PLC CPU memory range validation

* client — High-level user API

This design allows easy extension and future support
for additional PLC families or protocols.

## Legal Notice

- This is an independent, open-source implementation
based on publicly available protocol documentation.

- This project is not affiliated with, endorsed by, or sponsored by Mitsubishi Electric.

## License

- This project is licensed under the MIT License.
- See the LICENSE
    file for details.

## Author

# Piyush Ghumelia
Industrial Automation & Python Developer

PyPI: https://pypi.org/project/fx3u-mcprotocol/
