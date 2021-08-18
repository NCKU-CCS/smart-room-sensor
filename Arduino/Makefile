PKG=sct013
CORE=arduino:avr
BOARD=arduino:avr:uno
PORT=/dev/ttyACM0

.PHONY: all clean version init

install:
	sudo sh -c 'curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | BINDIR=/usr/bin sh'

board-list:
	arduino-cli board list

core-install:
	arduino-cli core install $(CORE)

core-list:
	arduino-cli core list

dev: install core-install

add-package:
	arduino-cli lib install EmonLib

code-compile:
	arduino-cli compile --fqbn $(BOARD) $(PKG)

code-upload:
	arduino-cli upload -t -p $(PORT) --fqbn $(BOARD) $(PKG)

update: code-compile code-upload
