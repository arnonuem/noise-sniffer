# Noise Sniffer
A python script that is running a flask webserver. 
A specific endpoint can be called or polled to trigger a read on a specific pin.
This just returns the value 0 or 1.

# Daemon
Supervisord is used to permanently run the python script in background.
The config file is located at /etc/supervisor/conf.d/noise-sniffer.conf
The configured app is called `noisesniffer`

# Start system service
`sudo supervisorctl start noisesniffer`

# Stop system service
`sudo supervisorctl stop noisesniffer`


# Running the app manually
> python3 noise_sniffer.py

This will fire up a webserver running on port 5000.
Noise level can be fetched/polled with [get] rpi:5000/noise