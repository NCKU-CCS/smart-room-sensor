import time
from datetime import datetime
from typing import Tuple, List

from loguru import logger
import minimalmodbus

from save_data import upload_data
from modbus import OBSERVE_REGS_MAP
from config import MODBUS_PORT

EXECUTION_MINUTE = ''

def get_float_data(com: minimalmodbus.Instrument, reg: str) -> Tuple[bool, float]:
    """send get float data command

    Args:
        com (minimalmodbus.Instrument): instrument object
        reg (str): register in hex

    Returns:
        Tuple[bool, float]: success/failure and value
    """
    try:
        regs = com.read_float(int(reg, 0))
        return True, regs
    except Exception as err:
        logger.debug(f"[Failed to Read Float] address: {reg}. Error: {err}")
        return False, 0

def check_retry_timeout():
    # Check Re-try Timeout (one minute)
    if datetime.now().minute != EXECUTION_MINUTE:
        logger.warning("[Meter] Timeout")
        exit(1)

def scan(com, map_table, loop, timebreak=1):
    while True:
        # GET Data
        datas: List[float] = []
        for reg in map_table.keys():
            while True:
                check_retry_timeout()
                success, value = get_float_data(com, reg)
                if success:
                    datas.append(value)
                    break
                else:
                    time.sleep(1)
                    continue

        map_data = dict()
        # Log ata
        logger.info(datetime.utcnow())
        for data, regs in zip(datas, map_table.values()):
            logger.info(f"{regs['name']}:\t {round(data, 3)} {regs['unit'] if 'unit' in regs else ''}")
            map_data[regs["field_name"]] = round(data, 3)
        logger.info("-" * 40)
        # Return Data
        if not loop:
            return map_data
        time.sleep(timebreak)


def main():
    # Re-try timeout set
    global EXECUTION_MINUTE
    EXECUTION_MINUTE = datetime.now().minute
    while True:
        check_retry_timeout()
        try:
            instrument = minimalmodbus.Instrument(MODBUS_PORT, 1, close_port_after_each_call=True)
            instrument.serial.baudrate = 9600
            break
        except Exception as err:
            logger.debug(f"[Failed to Create Connection] Error: {err}")
            time.sleep(1)
            continue
    # Loop Monitor
    # scan(instrument, OBSERVE_REGS_MAP, loop=True)
    data = scan(instrument, OBSERVE_REGS_MAP, loop=False)
    upload_data(data)


if __name__ == "__main__":
    main()
