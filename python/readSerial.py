import serial
import httplib
import time

tty = "ACM0" # For Arduino Uno
#tty = "USB0" # For Arduino Nano v3

ser = serial.Serial('/dev/tty' + tty, 9600, timeout=5);

import statsd

statsd.Connection.set_defaults(host='prodigy.local')
kwh_counter = statsd.Counter('Meters.Electricity.kWh')
powerusage = statsd.Gauge('Meters.Electricity')

EMONCMS_SERVER = '192.168.2.108'
EMONCMS_APIKEY = '771eb72212b26c140c998cea2e4ece07'

def SendPulse(value, node = 1, key = 'power'):
    global EMONCMS_APIKEY
    global EMONCMS_SERVER

    if (value < 20000):

        timenow = time.strftime('%s')
        url = ("/emoncms/input/post.json?time=%s&node=%i&json={%s:%d}&apikey=%s" % (timenow, node, key, value, EMONCMS_APIKEY))
        connection = httplib.HTTPConnection(EMONCMS_SERVER)
        connection.request("GET", url)


while 1:
    try:
        serialInput = ser.readline()
        inputStuff = serialInput.strip().strip('\x00').split();
        if inputStuff and inputStuff[1] and inputStuff[0] == "PulsePower:":
            value = float(inputStuff[1])
            #SendPulse(value)
            powerusage.send('Watts', value)
            print "Pulse: %s " % (value)
        if inputStuff and inputStuff[1] and inputStuff[0] == "kWh:":
            print "kWh: 1"
            kwh_counter += 1;
				
    except KeyboardInterrupt:
        print "Byebye"
        raise
    except:
        print "Error reading from serial!"
        raise

    # Sleep for 20 milliseconds
    time.sleep(0.02)	
