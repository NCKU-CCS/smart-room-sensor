import os

from dotenv import load_dotenv


load_dotenv()

# Thermo Sensor
DHT_PIN = int(os.getenv("DHT_PIN", "27"))
# DHT_TYPE (1)DHT11: DHT11; (2)DHT22: AM2302
DHT_TYPE = os.getenv("DHT_TYPE", "AM2302")

# Smart Meter
MODBUS_PORT = os.getenv("MODBUS_PORT", "/dev/ttyUSB0")

# CT Sensor
ARDUINO_PORT = os.getenv("ARDUINO_PORT", "/dev/ttyACM0")
CT_MAPPING = ["WWW", "VLDB_E", "VLDB_W", "LAB_E", "LAB_W", "KDD"]

# RPICT8
RPICT8_PORT = os.getenv("RPICT8_PORT", "/dev/ttyAMA0")
RPICT8_MAPPING = ["602_N", "602_S"]
RPICT8_MAPPING.extend([""] * (8 - len(RPICT8_MAPPING)))

# MCP3008
SPI_PORT = 0
SPI_DEVICE = 0
SIGNAL_CHANNEL = 0
CSVFILE = "CSVFILE"

# Upload
SENSOR = os.getenv("SENSOR", "")
ENDPOINT = os.getenv("ENDPOINT", "http://10.8.2.101:5000/")
TOKEN = os.getenv("TOKEN", "")
RETRY_TIME = int(os.getenv("RETRY_TIME", 11))
TIMEOUT = int(os.getenv("TIMEOUT", 5))

# Log only
GATEWAY = os.getenv("GATEWAY", "")
