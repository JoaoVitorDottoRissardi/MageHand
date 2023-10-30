install: install-service install-python

install-service:
	install -v magehand.service $(XDG_CONFIG_HOME)/systemd/user/

install-python:
	install -v -d -m 0755 -o magehand -g users /usr/local/bin/Magehand
	install -v -D -t /usr/local/bin/MageHand/ *.py
	cp -r pose /usr/local/bin/MageHand/
	cp -r images /usr/local/bin/MageHand/

config:
	install -v -d $(XDG_CONFIG_HOME)/MageHand
	install -v -D -t $(XDG_CONFIG_HOME)/MageHand MageHandParameters.json
	touch $(XDG_CONFIG_HOME)/MageHand/current_state.txt

set-var:
	install -v -d -m 0755 -o magehand -g users /var/lib/MageHand

# rsync
remote:
	rsync -av * magehand@raspberrypi:/home/magehand/MageHand/Firmware

remote-all:
	rsync -av ../* magehand@raspberrypi:/home/magehand/MageHand

run:
	GPIOZERO_PIN_FACTORY=pigpio DISPLAY=:0.0 python MageHand.py
	