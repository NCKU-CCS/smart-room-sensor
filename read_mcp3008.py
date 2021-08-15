#!/usr/bin/env python3
import csv
from dataclasses import dataclass
import time
from datetime import datetime

from loguru import logger
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

from config import SPI_PORT, SPI_DEVICE, SIGNAL_CHANNEL, CSVFILE


@dataclass
class CTData:
    # pylint: disable=C0103
    created: datetime.isoformat
    current: float
    # pylint: enable=C0103


def read() -> CTData:
    mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
    # Re-try timeout set
    now_minute = datetime.now().minute
    while True:
        if datetime.now().minute != now_minute:
            # Re-try timeout (one minute)
            logger.warning("[MCP3008] Timeout")
            exit(1)
        try:
            current = mcp.read_adc(SIGNAL_CHANNEL)
            logger.debug(current)
            return CTData(datetime.utcnow().isoformat(), current)
        except Exception as err:
            logger.error(err)


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


def main() -> None:
    data: CTData = read()
    save_csv(CSVFILE, data)


if __name__ == "__main__":
    main()
