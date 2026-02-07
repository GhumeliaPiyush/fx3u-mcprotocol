from fx3u_mcprotocol import FX3UClient

PLC_IP = "192.168.4.4"   # change if needed
PLC_PORT = 5001


def main():
    plc = FX3UClient(
        ip=PLC_IP,
        port=PLC_PORT,
        cpu="FX3U",
        mode="ascii",
        read_only=True,
    )

    plc.connect()

    print("=== SMOKE TEST : SINGLE PLC ===")

    print("D500–D502 :", plc.readRegs("D500", 5))
    print("D22–D24   :", plc.readRegs("D20", 5))
    print("D260–D262 :", plc.readRegs("D262", 5))
    print("D34       :", plc.readReg("D100"))

    print("M0        :", plc.readBit("M0"))
    print("M8000     :", plc.readBit("M8000"))  # RUN bit

    plc.close()
    print("=== SMOKE TEST PASSED ===")


if __name__ == "__main__":
    main()
