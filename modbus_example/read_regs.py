import time

# pip3 install minimalmodbus
import minimalmodbus


def main():
    instrument = minimalmodbus.Instrument("/dev/tty.usbserial-AR0JUJ6U", 1)
    instrument.serial.baudrate = 9600
    registers = ["0x0000", "0x0002"]
    while True:
        for register in registers:
            data = instrument.read_register(int(register, 0))
            print(f"[{register}] {data}")
        time.sleep(1)


if __name__ == "__main__":
    main()
