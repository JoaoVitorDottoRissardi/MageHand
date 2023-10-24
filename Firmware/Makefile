install: install-service install-python

install-service:
	install -v magehand.service $(XDG_CONFIG_HOME)/systemd/user/

install-python:
	install -v -D -t /usr/local/bin/MageHand/ *.py
	cp -r pose /usr/local/bin/MageHand/
	cp -r images /usr/local/bin/MageHand/

config:
	install -v -D -t $(XDG_CONFIG_HOME)/MageHand MageHandParameters.json

# rsync
remote:
	rsync -av * magehand@raspberrypi:/home/magehand/MageHand/Firmware

remote-all:
	rsync -av ../* magehand@raspberrypi:/home/magehand/MageHand
