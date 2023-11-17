install: install-service install-python config set-var

install-service:
	mkdir -p /home/magehand/.config/systemd/user/
	install -v magehand.service /home/magehand/.config/systemd/user/

install-python:
	install -v -d -m 0755 -o magehand -g users /usr/local/bin/Magehand
	install -v -D -t /usr/local/bin/MageHand/ *.py
	install -v -D -t /usr/local/bin/MageHand/ run.sh
	cp -r pose /usr/local/bin/MageHand/
	cp -r images /usr/local/bin/MageHand/

config:
	install -v -d /home/magehand/.config/MageHand
	install -v -D -t /home/magehand/.config/MageHand MageHandParameters.json
	touch /home/magehand/.config/MageHand/current_state.txt

set-var:
	install -v -d -m 0755 -o magehand -g users /var/lib/MageHand

# rsync
remote:
	rsync -av * magehand@raspberrypi:/home/magehand/MageHand/Firmware

remote-all:
	rsync -av ../* magehand@raspberrypi:/home/magehand/MageHand

run:
	GPIOZERO_PIN_FACTORY=pigpio DISPLAY=:0.0 python MageHand.py
