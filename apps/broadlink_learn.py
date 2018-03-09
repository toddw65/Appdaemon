#
# broadlink_learn.py
#
#
# batch learn broadlink codes
#
# Logic:
#
#
#
import appdaemon.plugins.hass.hassapi as hass

class BroadlinkGetCodes(hass.Hass):


# Import the csv file containing the list of keys
import appdaemon.appapi as appapi
from queue import Queue
import threading
import time
import os.path
import datetime
import globals
import csv
import tkinter
import tkinter.messagebox as mb
from tkinter import filedialog

root = tkinter.Tk()
root.withdraw()

file_path = filedialog.askopenfilename()


def procCode(keyname):
    mb.showinfo("Process Code", keyname)
    retCode = hass.services.call("switch.broadlink_learn_command_192_168_0_132", None, True)
    while not retCode =='':
        mb.showinfo("Process Code", keyname + ' - ' + retCode)
    return;


#loop_enabled = True
# sleep_time = .065

#while loop_enabled:
#        hass.services.call("switch.broadlink_learn_command_192_168_0_132", "denonavr_volume_up", None, True)
#    else:
#        loop_enabled = False

with open(file_path, 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        # mb.showinfo("Process Code", row)
        procCode(row)
        # print (row)



# Get Data from Automation Trigger
# triggeredEntity = data.get('entity_id')
# metatrackerName = "device_tracker." + data.get('meta_entity')

# Get current & new state
# newState = hass.states.get(triggeredEntity)
# currentState = hass.states.get(metatrackerName)
# Get New data
# newSource = newState.attributes.get('source_type')

# If GPS source, set new coordinates
# if newSource == 'gps':
#    newLatitude = newState.attributes.get('latitude')
#    newLongitude = newState.attributes.get('longitude')
#    newgpsAccuracy = newState.attributes.get('gps_accuracy')
# If not, keep last known coordinates
# else:
#    if newSource is not None:
#        newLatitude = currentState.attributes.get('latitude')
#        newLongitude = currentState.attributes.get('longitude')
#        newgpsAccuracy = currentState.attributes.get('gps_accuracy')

# Get Battery
# if newState.attributes.get('battery') is not None:
#    newBattery = newState.attributes.get('battery')
# elif currentState.attributes.get('battery') is not None:
#    newBattery = currentState.attributes.get('battery')
# else:
#    newBattery = None

# Set new state and icon
# Everything updates 'home'
# if newState.state == 'home':
#    newStatus = 'home'
#    newIcon = 'mdi:home-map-marker'
## only GPS platforms update 'not_home'
# elif newState.state == 'not_home' and newSource == 'gps':
#    newStatus = 'not_home'
#    newIcon = 'mdi:home'
# Otherwise keep old status
# else:
#    newStatus = currentState.state

# Create device_tracker.meta entity
# hass.states.set(metatrackerName, newStatus, {
#    'icon': newIcon,
#    'name': metatrackerName,
#    'source_type': newSource,
#    'battery': newBattery,
#    'gps_accuracy': newgpsAccuracy,
#    'latitude': newLatitude,
#    'longitude': newLongitude,
#    'last_update_source': newState.name
# })
