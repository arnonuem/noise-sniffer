# What is this?
A python script that is listening to a GPIO pin of a RPI.
Attached is a simple microphone which just returns a 1 if there is no noise and a 0 if there is a noise.

The data is collected in a sort of sliding window of like 30 entries. It sort of looks like `111111111111001111110000111111111...`

This data is directly published to an MQTT broker (https://nanomq.io) to the topic `sensor/noise` using paho-mqtt.

# Installation
Clone the repo. Have Python 3 installed as well as the Paho MQTT dependency.
```
sudo pip3 install paho-mqtt
```

# Post installation
Supervisord is used to permanently run the python script in background.
Create a config file which is located at `/etc/supervisor/conf.d/noise-sniffer.conf`.

Add the following content:
```
[program:noisesniffer]
command = /usr/bin/python3 /home/someuser/noise-sniffer/noise_sniffer.py
directory = /home/someuser/noise-sniffer
user = someuser
environment=HOME="/home/someuser", USER="someuser"
```

# Start system service
`sudo supervisorctl start noisesniffer`

# Stop system service
`sudo supervisorctl stop noisesniffer`

# Running the app manually
> python3 noise_sniffer.py

# Deprecation
The `noise_sniffer_flask.py` is deprecated and not longer used.
