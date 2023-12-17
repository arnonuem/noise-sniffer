import RPi.GPIO as GPIO
import time

from flask import Flask
from flask import jsonify

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


app = Flask(__name__)
@app.route("/")
def home():
	return "<h2>Noise Sniffer</h2><br><p>Use <tt>/noise</tt> to fetch noise level</p>"

@app.route("/noise")
def noiseLevel():
	return jsonify(dataStream)
#	return str(pinValue)
#	return str(GPIO.input(channel))

if __name__ == "__main__":
	app.debug = True
	app.run(host="0.0.0.0")