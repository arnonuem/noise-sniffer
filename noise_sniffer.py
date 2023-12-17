#
# Using MQTT
#

import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt

# GPIO STUFF
print(GPIO.RPI_INFO)

#GPIO SETUP
channel = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

pinValue = 0
dataStream = []

def onPinChange(channel):
	pinValue = GPIO.input(channel)
	if pinValue:
		dataStream.append(pinValue)
		if len(dataStream) > 30:
			dataStream.pop(0)
#		print("Noise detected! " + str(pinValue))
	else:
		dataStream.append(pinValue)
		if len(dataStream) > 30:
			dataStream.pop(0)
#		print("Noise detected!" + str(pinValue))

# inform when pin goes HIGH or LOW
GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)

# assign callback function to be called when pin state changes
GPIO.add_event_callback(channel, onPinChange)


# MQTT STUFF

#def on_publish(client, userdata, mid):
#    print("message sent")


mqttClient = mqtt.Client("noise_sensor")
#mqttClient.on_publish = on_publish
mqttClient.connect('192.168.178.2', 1883)
# start a new thread
mqttClient.loop_start()

# Why use msg.encode('utf-8') here
# MQTT is a binary based protocol where the control elements are binary bytes and not text strings.
# Topic names, Client ID, Usernames and Passwords are encoded as stream of bytes using UTF-8.
# QOS: 
#   0 = message is delivered once at maximum (no checks)
#   1 = message is delivered once at minimum (using check where receiver has to acknowledge)
#   2 = message is delivered exactly once (highest quality more checks)
while True:
    info = mqttClient.publish(
        topic='sensor/noise',
        payload=''.join(map(str, dataStream)).encode('utf-8'),
        qos=0, 
    )
    # Because published() is not synchronous,
    # it returns false while he is not aware of delivery that's why calling wait_for_publish() is mandatory.
    info.wait_for_publish()
    print(info.is_published())
    time.sleep(1)
    