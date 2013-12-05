#!/usr/bin/python

import random
import pygame
TEST = False
netDir = "/proc/net"
wirelessFile = "wireless"

iconDir = "./images"
iconFnameBase = "nm-signal-"

def getWirelessQuality():
    """Returns the system derived wireless link quality.
    If the global variable TEST is set to true, returns a random number for
    testing.
    """
    if (TEST):
        qual = random.randint(0,100)
    else:
        f = open("%s/%s" % (netDir,wirelessFile))
        fileLines = f.readlines()
        print fileLines
        if (len(fileLines)>=3):
            parts = fileLines[2].split()
            qual = float(parts[2])
        else:
            qual = -1
    print qual
    return qual

def getWirelessIcon():
    """Gets the curent wireless link quality using getWirelessQuality()
    and returns a pygame surface containing the icon representing the
    current image quality.   Uses images in the ./images directory to get
    the icon image.
    """
    q = getWirelessQuality()
    print q
    if (q < 0):
        qual = -1
    elif (q < 1):
        qual = 0
    elif (q < 2):
        qual =  25
    elif (q < 3):
        qual = 50
    else:
        qual = 100
    if (qual<0):
        fname = "%s/%snolink.png" % (iconDir,iconFnameBase)
        print "no Wireless"
    else:
        fname = "%s/%s%d.png" % (iconDir,iconFnameBase,qual)
    print fname
    iconImg = pygame.image.load(fname)
    return iconImg

    


qualImg = getWirelessIcon()
print qualImg

