# home-iot
repository for home iot projects

## systemd service details

sudo systemctl daemon-reload

sudo systemctl start bme_pubsub.service 

sudo systemctl stop bme_pubsub.service 

sudo journalctl -u bme_pubsub.service

/lib/systemd/system/bme_pubsub.service


## TODO:
~~- move to more stable bme library:https://github.com/pimoroni/bme280-python~~

~~- fix systemd service to use virtualenv and working bme280 library~~

~~- calulate temperature offset for more accurate temperature readings:~~

~~https://www.raspberrypi.org/forums/viewtopic.php?t=185244 OR https://github.com/pimoroni/bme280-python/blob/master/examples/compensated-temperature.py
