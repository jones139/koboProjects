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
import urllib2
import pygame
import os

from subprocess import call

os.environ['SDL_NOMOUSE'] = '1'   # Not sure what this does

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
    
def getGmailData():
    print "getGmailData()"

def updateDisplay():
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
    screen = pygame.Surface((600, 800))
    screen.fill(white)

    tiny_font = pygame.font.Font("fonts/Cabin-Regular.otf", 18)
    small_font = pygame.font.Font("fonts/Fabrica.otf", 22)
    font = pygame.font.Font("fonts/Forum-Regular.otf", 40)
    comfortaa = pygame.font.Font("fonts/Comfortaa-Regular.otf", 60)
    comfortaa_small = pygame.font.Font("fonts/Comfortaa-Regular.otf", 35)

    # Dividing lines
    pygame.draw.line(screen, gray, (10, 200), (590, 200))
    pygame.draw.line(screen, gray, (10, 400), (590, 400))
    pygame.draw.line(screen, gray, (200, 410), (200, 790))
    pygame.draw.line(screen, gray, (400, 410), (400, 790))


    date = small_font.render("Hello World", True, black, white)
    date_rect = date.get_rect()
    date_rect.topleft = 10,15
    screen.blit(date, date_rect)


    # Rotate the display to portrait view.
    graphic = pygame.transform.rotate(screen, 90)
    display.blit(graphic, (0, 0))
    pygame.display.update()
    
    #call(["./full_update"])
    convert_to_raw(screen)
    call(["/mnt/onboard/.python/display_raw.sh"])



updateDisplay()
