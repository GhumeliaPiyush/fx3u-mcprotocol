# fx3u-mcprotocol

An independent, open-source Python library for communicating with
Mitsubishi FX3-series PLCs via Ethernet using the MC Protocol
(ASCII and Binary) over TCP.

## Supported Hardware
- FX3U / FX3G / FX3S / FX3GC
- FX3U-ENET-ADP Ethernet adapter

## Disclaimer

- This project is an independent, open-source implementation of the MC Protocol
for interoperability and educational purposes.

- Mitsubishi Electric, FX3U, FX3G, FX3S, and related names are trademarks of
Mitsubishi Electric Corporation.

- This project is not affiliated with, endorsed by, or supported by
Mitsubishi Electric Corporation.

## Features
- Symbol-based memory access (D, M, X, Y, R)
- ASCII MC Protocol (stable)
- Binary MC Protocol (experimental)
- CPU-aware memory validation
- Cross-platform (Windows / Linux)

## ✅ Stable ASCII MC Protocol support (FX3 series)
## ⚠️ Binary MC Protocol support is experimental and may vary by firmware

## Example

```python
from fx3u_mcprotocol import FX3UClient

plc = FX3UClient(
    ip="192.168.4.4",
    port=5001,
    cpu="FX3U",
    mode="ascii"
)

plc.connect()

print(plc.readReg("D100"))
print(plc.readBits("M0", 8))

plc.close()


