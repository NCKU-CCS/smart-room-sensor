#!/usr/bin/env python3
from dataclasses import dataclass
import time
from datetime import datetime, timedelta
import csv

from loguru import logger
import serial

from config import ARDUINO_PORT, CSVFILE


@dataclass
class CTData:
    # pylint: disable=C0103
    created: datetime.isoformat
    current: float
    # pylint: enable=C0103


def read():
    ser = serial.Serial(ARDUINO_PORT, 9600, timeout=1)
    ser.flush()
    # Re-try timeout set
    time_start = datetime.utcnow()
    while True:
        if ser.in_waiting > 0:
            current = float(ser.readline().decode("utf-8").rstrip())
            logger.info(f"[READ CURRENT] {current}")
            if datetime.utcnow() - time_start >= timedelta(seconds=10):
                # Re-try timeout (10 seconds)
                logger.warning("[Meter] Timeout")
                return None
            return CTData(datetime.utcnow().isoformat(), current)


def save_csv(filename: str, data: CTData) -> None:
    try:
        with open("output.csv", "a", newline="") as csvfile:
            fieldnames = data.__dict__.keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(data.__dict__)
        logger.info("[CSV Data Saved]")
    except Exception as err:
        logger.error(f"[CSV Failed] {err}")
        logger.error(f"[CSV Data] {data}")


def main():
    while True:
        data: CTData = read()
        if data:
            save_csv(CSVFILE, data)
        time.sleep(1)


if __name__ == "__main__":
    main()
