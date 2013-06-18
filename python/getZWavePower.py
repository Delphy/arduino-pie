import httplib
import time

import logging
import sys, os
import openzwave
from openzwave.node import ZWaveNode
from openzwave.value import ZWaveValue
from openzwave.scene import ZWaveScene
from openzwave.controller import ZWaveController
from openzwave.network import ZWaveNetwork
from openzwave.option import ZWaveOption

device="/dev/zwave-aeon-s2"
zwavenode=3
EMONCMS_SERVER = '192.168.0.138'
EMONCMS_APIKEY = 'a474356a3c04c8f162891959dd6edb76' # Must be read and write one!
log="Debug"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('openzwave')

#Define some manager options
options = ZWaveOption(device, \
  config_path="../openzwave/config", \
  user_path=".", cmd_line="")
options.set_log_file("OZW_Log.log")
options.set_append_log_file(False)
options.set_console_output(False)
options.set_save_log_level(log)
#options.set_save_log_level('Info')
options.set_logging(False)
options.lock()

#Create a network object
network = ZWaveNetwork(options, log=None)

time_started = 0
print "------------------------------------------------------------"
print "Waiting for network awaked : "
print "------------------------------------------------------------"
for i in range(0,300):
    if network.state>=network.STATE_AWAKED:

        print(" done")
        break
    else:
        sys.stdout.write(".")
        sys.stdout.flush()
        time_started += 1
        time.sleep(1.0)
if network.state<network.STATE_AWAKED:
    print "."
    print "Network is not awake but continue anyway"

for i in range(0,300):
    if network.state>=network.STATE_READY:
        print " done in %s seconds" % time_started
        break
    else:
        sys.stdout.write(".")
        time_started += 1
        #sys.stdout.write(network.state_str)
        #sys.stdout.write("(")
        #sys.stdout.write(str(network.nodes_count))
        #sys.stdout.write(")")
        #sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(1.0)

if not network.is_ready:
    print "."
    print "Network is not ready but continue anyway"

name_map = {
    1: 'TV',
    2: 'HTPC',
    3: 'Amplifier',
    4: 'ConsolesAndCable',
    5: 'ServerPrinterMonitor',
    6: 'RouterAndSwitches',
}

def show_node_power(nodeid):
    node = network.nodes[nodeid]

    readings = {}

    for val in node.get_sensors():
        if  node.values[val].instance not in  readings:
            readings[node.values[val].instance] = {}
        #if node.values[val].label == "Energy" or node.values[val].label == "Power":
        if node.values[val].label == "Power":
            readings[node.values[val].instance][node.values[val].label] = node.get_sensor_value(val)
        
    print readings

    return readings

def SendValue(value, node = 1, key = 'power'):
    global EMONCMS_APIKEY
    global EMONCMS_SERVER

    if (value < 20000):

        timenow = time.strftime('%s')
        url = ("/emoncms/input/post?time=%s&node=%i&json={%s:%f}&apikey=%s" % (timenow, node, key, value, EMONCMS_APIKEY))
        connection = httplib.HTTPConnection(EMONCMS_SERVER)
        connection.request("GET", url)

data = show_node_power(zwavenode);
print data

for val in data:
    for readings in data[val]:
        SendValue(data[val][readings], zwavenode, name_map[val] + "_" + readings)


network.stop()

