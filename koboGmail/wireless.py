#!/usr/bin/python


netDir = "/proc/net"
wirelessFile = "wireless"


def getWirelessQuality():
    f = open("%s/%s" % (netDir,wirelessFile))
    fileLines = f.readlines()
    print fileLines
    #statusStr = f.read()
    #print statusStr
    #statusStr = f.read()
    #print statusStr
    parts = fileLines[2].split()
    qual = float(parts[2])
    print qual
    return qual




qual = getWirelessQuality()

print "quality=%s%%\n" % (qual)
