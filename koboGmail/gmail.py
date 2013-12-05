#!/usr/bin/python
#
# koboGmail, Copyright Graham Jones 2013 (grahamjones139@gmail.com)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Based on information from a variety of sources including:
#    gmail access: http://g33k.wordpress.com/2009/02/04/check-gmail-the-python-way/ 
#    Kobo display: http://www.mobileread.com/forums/showthread.php?t=194376
#
import sys
import urllib2
import pygame
import os
import time
import ConfigParser
import feedparser
from subprocess import call

from wireless import *
from battery import *

os.environ['SDL_NOMOUSE'] = '1'   # Not sure what this does

configFname="config.ini"

def to_hex(color):
    ''' convert a colour value into a hexadecimal value 
    Based on Kevin Short's koboWeather app
    '''
    hex_chars = "0123456789ABCDEF"
    return hex_chars[color / 16] + hex_chars[color % 16]
    
def convert_to_raw(surface):
    ''' convert an SDS drawing surface into a raw image format.
    saves the raw data in /tmp/img.raw.
    Based on Kevin Short's koboWeather app
    '''
    print("Converting image . . .")
    raw_img = ""
    for row in range(surface.get_height()):
        for col in range(surface.get_width()):
            color = surface.get_at((col, row))[0]
            raw_img += ('\\x' + to_hex(color)).decode('string_escape')
    f = open("/tmp/img.raw", "wb")
    f.write(raw_img)
    f.close()
    print("Image converted.")
    

def openConfigFile(fname):
    '''Open the configuration file 'fname' and return a ConfigParser object
    that points to the opened file.
    '''
    config = ConfigParser.ConfigParser()
    config.read(fname)
    return(config)

def getConfigSectionMap(config, section):
    '''Returns a dictionary containing the config file data in the section
    specified by the parameter section.   config should be a ConfigParser object
    pointing to a configuration file.'''
    dict1 = {}
    options = config.options(section)
    for option in options:
        try:
            dict1[option] = config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

def getGmailData():
    '''The method to do HTTPBasicAuthentication
    created based on http://docs.python.org/2/howto/urllib2.html'''

    # Read the config file
    config = openConfigFile(configFname)
    print config.sections()
    configData =  getConfigSectionMap(config,config.sections()[0])
    print configData

    # Open connection to gmail using the usernam and password specified
    # in the config file.
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    top_level_url = configData['baseurl']
    username = configData['username']
    password = configData['password']
    password_mgr.add_password(None, top_level_url, username, password)
    handler = urllib2.HTTPBasicAuthHandler(password_mgr)
    opener = urllib2.build_opener(handler)

    # use the opener to fetch a URL
    fullURL = "%s/%s/%s" % (top_level_url,
                            configData['feedurl'],
                            configData['labelfilter'])
    print "getting data using url %s." % fullURL
    try:
        f = opener.open(fullURL)
        feed = f.read()
        atom = feedparser.parse(feed)
        print ""
        print atom.feed.title
        print "You have %s new mails" % len(atom.entries)
    except Exception:
        print "Error accessing gmail"
        atom = None
    print "getGmailData()"

    return atom

def updateDisplay(atom):
    '''Update the kobo display to show the email atom feed atom.'''
    print("Creating Image")

    # Define some colours
    white = (255, 255, 255)
    black = (0, 0, 0)
    gray = (125, 125, 125)

    # Initialise Pygame for drawing to the screen.
    pygame.display.init()
    pygame.font.init()
    pygame.mouse.set_visible(False)
    display = pygame.display.set_mode((800, 600), pygame.FULLSCREEN)
    #display = pygame.display.set_mode((800, 600))
    screen = pygame.Surface((600, 800))
    screen.fill(white)

    font = pygame.font.Font("fonts/Forum-Regular.otf", 40)
    large_font = pygame.font.Font("fonts/Forum-Regular.otf", 100)
    huge_font = pygame.font.Font("fonts/Forum-Regular.otf", 300)

    # Now render the data
    if (atom!=None):
        # Atom title
        txt = font.render(atom.feed.title, True, black, white)
        txt_rect = txt.get_rect()
        txt_rect.topleft = 0,0
        screen.blit(txt, txt_rect)

        str = "You have"
        txt = large_font.render(str, True, black, white)
        txt_rect = txt.get_rect()
        txt_rect.topleft = 0,40
        screen.blit(txt, txt_rect)

        str = "%d" % len(atom.entries)
        txt = huge_font.render(str, True, black, white)
        txt_rect = txt.get_rect()
        txt_rect.topleft = 100,130
        screen.blit(txt, txt_rect)

        str = "new Emails!!!"
        txt = large_font.render(str, True, black, white)
        txt_rect = txt.get_rect()
        txt_rect.topleft = 0,400
        screen.blit(txt, txt_rect)
    else:
        str = "Error Accessing Gmail"
        txt = large_font.render(str, True, black, white)
        txt_rect = txt.get_rect()
        txt_rect.topleft = 0,400
        screen.blit(txt, txt_rect)
        

    # Display Wifi Image
    wifiImg = getWirelessIcon()
    screen.blit(wifiImg,(0,0))

    # Display Battery Image
    batImg = getBatteryIcon()
    screen.blit(batImg,(40,0))

    # Rotate the display to portrait view.
    graphic = pygame.transform.rotate(screen, 90)
    display.blit(graphic, (0, 0))

    # Only do this for testing to keep the window visible on pc screen.
    #while True: # main game loop 
    #    for event in pygame.event.get(): 
    #        if event.type == pygame.QUIT: 
    #            pygame.quit() 
    #            sys.exit() 
    #    pygame.display.update()

    pygame.display.update()
    
    call(["./full_update"])
    #convert_to_raw(screen)
    #call(["/mnt/onboard/.python/display_raw.sh"])

while True:
    atom = getGmailData()
    updateDisplay(atom)
    time.sleep(10)
