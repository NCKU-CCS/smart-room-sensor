# smart room - sensor

Smart Room Sensors

+ [Thermo Sensor](./thermo_sensor.py)
    + DHT11, DHT22 Thermo Data
+ [Smart Meter](./meter.py)
    + Smart Meter Data
+ [1 CT Sensor - Arduino - Save Local](./read_arduino_one.py)
    + Read one CT Sensor Data
    + Save to local CSV file
+ [6 CT Sensor - Arduino - Save DB](./read_arduino.py)
    + CT Sensor Data
    + Save to Remote database
+ [CT Sensor - RPICT8](./read_RPICT8.py)
    + CT Sensor Data from RPICT8
## Getting Started

### Prerequisites

- python 3.7

### Config

Update `.env` setting file
```sh
cp env.sample .env
# update .env file
```

### General Packages

Installing General Packages
```sh
pip3 install requests python-dotenv loguru
```

# Services

## [Smart Meter](./meter.py)
Read data from Smart Meter via modbus.

### Packages
```sh
# minimalmodbus for modbus communication
pip3 install minimalmodbus
```

### env example
Set Modbus USB Port.

```sh
MODBUS_PORT=/dev/ttyUSB0
```

How to know PORT name from Pi:
```sh
ls /dev/tty*
```


### Running
```sh
python3 meter.py
```

## [Thermo Sensor](./thermo_sensor.py)
Read data from DHT Sensor.

### Packages
Customize `Adafruit_DHT` package: make DHT11 data accuracy to one decimal place.


### env example
+ PIN: PIN Number
+ DHT_TYPE: DHT Sensor Type
    + DHT11: DHT11
    + DHT22: AM2302 or DHT22

```sh
DHT_PIN=27
DHT_TYPE=AM2302
```

### Running
```sh
python3 thermo_sensor.py
```


## [1 CT Sensor - Arduino - Save Local](./read_arduino_one.py)

RPi read meter data from CT sensor via Arduino and save to local CSV file.

### Packages
```sh
pip3 install pyserial
```

### env example
Set Arduino USB Port.

```sh
ARDUINO_PORT=/dev/ttyUSB0
```

How to know PORT name from Pi:
```sh
ls /dev/tty*
```

### Running
```sh
python3 read_arduino_one.py
```


## [6 CT Sensor - Arduino - Save DB](./read_arduino.py)
Read data from CT sensor from Arduino via serial signal.

*CT Sensor* --Aanlog Signal-> *Arduino* --Serial Signal--> *Raspberry pi* --HTTP-> *Data Center*

### Packages
```sh
pip3 install pyserial
```

### env example
Set Arduino USB Port.

```sh
ARDUINO_PORT=/dev/ttyUSB0
```

How to know PORT name from Pi:
```sh
ls /dev/tty*
```


### Running
```sh
python3 read_arduino.py
```

## [CT Sensor - RPICT8](./read_RPICT8.py)
Read data from CT sensor via [RPICT8](http://lechacal.com/wiki/index.php/RPICT8) with serial signal.

Docs: [Notion](https://www.notion.so/netdb/61b89b8fcd374ef1996bd712f8778a6e)

*CT Sensor* --Aanlog Signal-> *RPICT8* --Serial Signal--> *Raspberry pi* --HTTP-> *Data Center*

### Packages
```sh
pip3 install pyserial
```

### env example
Set RPICT8_PORT USB Port.

```sh
RPICT8_PORT=/dev/ttyUSB0
```

How to know PORT name from Pi:
```sh
ls /dev/tty*
```


### Running
```sh
python3 read_RPICT8.py
```

## Save Data

[save_data.py](./save_data.py)

+ `upload_data` : upload data to data center via HTTP POST request.
    Note: `upload_data` will REBOOT Pi when internet error
