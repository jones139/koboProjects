#!/usr/bin/python


batteryDir = "/sys/devices/platform/pmic_battery.1/power_supply/mc13892_bat"
statusFile = "status"
capacityFile = "capacity"

def getBatteryStatus():
    f = open("%s/%s" % (batteryDir,statusFile))
    statusStr = f.read()
    print statusStr
    return statusStr.strip()

def getBatteryCapacity():
    f = open("%s/%s" % (batteryDir,capacityFile))
    capacityStr = f.read()
    print capacityStr
    return int(capacityStr)


status= getBatteryStatus()
cap = getBatteryCapacity()

print "status=%s, capacity=%d%%\n" % (status,cap)
