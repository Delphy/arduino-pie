import serial
import httplib
import time

# tty = "ACM0" # For Arduino Uno
tty = "USB0" # For Arduino Nano v3

EMONCMS_SERVER = '192.168.0.138'
EMONCMS_APIKEY = 'ad5d08fb3456418beb0d19d282fa9144' # Must be read and write one!

ser = serial.Serial('/dev/tty' + tty, 9600, timeout=5);
pulsecount = 0
lastPulse = 0
ignoreFastPulse = 0.10 # Ignore extraneous pulses that come faster than this

def SendPulse(power):
	global EMONCMS_APIKEY
	global EMONCMS_SERVER

	if (power < 20000):

		timenow = time.strftime('%s')
		url = ("/emoncms/input/post?time=%s&node=1&json={power:%s}&apikey=%s" % (timenow, power, EMONCMS_APIKEY))
		connection = httplib.HTTPConnection(EMONCMS_SERVER)
		connection.request("GET", url)

while 1:
	try:
		serialInput = ser.readline()

		inputStuff = serialInput.strip().strip('\x00').split();
	        # print "inputStuff: %s" % inputStuff
		if inputStuff and inputStuff[1] and inputStuff[0] == "PulsePower:":
			print "Pulse: %s w" % inputStuff[1]
			SendPulse(float(inputStuff[1]))
				
	except KeyboardInterrupt:
		print "Byebye"
		raise
	except:
		print "Error reading from serial!"
		raise

	# Sleep for 20 milliseconds
	time.sleep(0.02)	
