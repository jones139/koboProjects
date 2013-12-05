#!/usr/bin/python

import pygame
import random

TEST = False
iconDir = "./images"
iconFnameBase = "gpm-battery-"

batteryDir = "/sys/devices/platform/pmic_battery.1/power_supply/mc13892_bat"
statusFile = "status"
capacityFile = "capacity"

def getBatteryStatus():
    if (TEST):
        statusStrs = ["charging","discharging"]
        status = random.randint(0,1)
        statusStr = statusStrs[status]
    else:
        try:
            f = open("%s/%s" % (batteryDir,statusFile))
            statusStr = f.read()
            print statusStr
        except Exception:
            statusStr = "no battery"
    return statusStr.strip()

def getBatteryCapacity():
    if (TEST):
        cap = random.randint(0,100)
    else:
        try:
            f = open("%s/%s" % (batteryDir,capacityFile))
            capacityStr = f.read()
            cap = int(capacityStr)
        except Exception:
            cap = -1
    print cap
    return cap

def getBatteryIcon():
    """Gets the curent battery charge and quality using getBatteryCapacity()
    and returns a pygame surface containing the icon representing the
    current battery state.   Uses images in the ./images directory to get
    the icon image.
    """
    cap = getBatteryCapacity()
    status = getBatteryStatus()
    print cap,status
    if (cap<0):
        cap = -1
    elif (cap <10):
        cap = 0
    elif (cap <30):
        cap =  20
    elif (cap<50):
        cap = 40
    elif (cap<70):
        cap = 60
    elif (cap<90):
        cap = 80
    else:
        cap = 100

    print status
    if status=="Charging":
        chargeStr = "-charging"
    elif status=="no battery":
        chargeStr = "-nobattery"
    else:
        chargeStr = ""

    if (cap<0):
        fname = "%s/%s-nobattery.png" % (iconDir,iconFnameBase)
        print "no battery"
    else:
        fname = "%s/%s%03d%s.png" % (iconDir,iconFnameBase,cap,chargeStr)
    print fname
    iconImg = pygame.image.load(fname)
    return iconImg




#status= getBatteryStatus()
#cap = getBatteryCapacity()
#print "status=%s, capacity=%d%%\n" % (status,cap)

icon = getBatteryIcon()
