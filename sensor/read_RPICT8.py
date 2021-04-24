#!/usr/bin/env python3
from dataclasses import dataclass
import time
from datetime import datetime

from dataclasses_json import dataclass_json
from loguru import logger
import serial

from save_data import upload_data
from config import RPICT8_PORT, RPICT8_MAPPING


@dataclass_json
@dataclass
class CTData:
    # pylint: disable=C0103
    current: float = float()
    voltage: float = float()
    power: float = float()
    total_current: float = float()
    # pylint: enable=C0103


def read():
    ser = serial.Serial(RPICT8_PORT, 38400, timeout=1)
    ser.flush()
    # Re-try timeout set
    now_minute = datetime.now().minute
    while True:
        if ser.in_waiting > 0:
            message = ser.readline().decode("utf-8").rstrip()
            logger.debug(f"[Serial Message] {message}")
            currents = message.split(" ")[1:]
            logger.info(f"[READ CURRENT] {currents}")
            if len(currents) != len(RPICT8_MAPPING):
                logger.error("[CT Sensor] Receive Data Length Incorrect.")
                logger.debug(f"[Data Length] CT:{len(RPICT8_MAPPING)}, Received: {len(currents)}")
                time.sleep(1)
                if datetime.now().minute != now_minute:
                    # Re-try timeout (one minute)
                    logger.warning("[RPICT8] Timeout")
                    exit(1)
                continue
            datas = [CTData(current=float(current) / 240) for idx, current in enumerate(currents) if RPICT8_MAPPING[idx]]
            return datas


def main():
    datas = read()
    for index, data in enumerate(datas):
        upload_data(data.to_dict(), sensor=f"CT_{RPICT8_MAPPING[index]}")


if __name__ == "__main__":
    main()
