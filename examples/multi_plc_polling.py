import time
from fx3u_mcprotocol import FX3UClient

PLCS = {
    "PLC_1": "192.168.4.2",
    "PLC_2": "192.168.4.3",
    "PLC_3": "192.168.4.4",
    "PLC_4": "192.168.4.5",
}

POLL_INTERVAL = 1.0  # seconds


def main():
    clients = {}

    # Connect all PLCs
    for name, ip in PLCS.items():
        plc = FX3UClient(
            ip=ip,
            port=5001,
            cpu="FX3U",
            mode="ascii",
            read_only=True,
        )
        plc.connect()
        clients[name] = plc

    print("=== MULTI-PLC POLLING STARTED ===")

    try:
        while True:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

            for name, plc in clients.items():
                d100 = plc.readRegs("D100", 3)
                m0 = plc.readBit("M0")

                print(f"{timestamp} | {name} | D100–102={d100} | M0={m0}")

            time.sleep(POLL_INTERVAL)

    except KeyboardInterrupt:
        print("Stopping polling...")

    finally:
        for plc in clients.values():
            plc.close()


if __name__ == "__main__":
    main()
