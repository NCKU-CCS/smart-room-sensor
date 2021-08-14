#!/usr/bin/env python3
from dataclasses import dataclass
import time
from datetime import datetime

from loguru import logger
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

from config import SPI_PORT, SPI_DEVICE, SIGNAL_CHANNEL


@dataclass
class CTData:
    # pylint: disable=C0103
    current: float = float()
    voltage: float = float()
    power: float = float()
    total_consumption: float = float()
    # pylint: enable=C0103


def read():
    mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
    # Re-try timeout set
    now_minute = datetime.now().minute
    while True:
        if datetime.now().minute != now_minute:
            # Re-try timeout (one minute)
            logger.warning("[MCP3008] Timeout")
            exit(1)
        try:
            value = mcp.read_adc(SIGNAL_CHANNEL)
            logger.debug(value)
            return value
        except Exception as err:
            logger.error(err)


def main():
    datas = read()


if __name__ == "__main__":
    main()
