import urllib2
import pygame, os

from xml.dom.minidom import parseString
from datetime import date, datetime, timedelta
from subprocess import call

os.environ['SDL_NOMOUSE'] = '1'
print("Kobo Wifi weather forecast started.")

def index_error(error):
    print(error)
    print("Failed to fetch weather data.")
    print("Double check your location settings by running:")
    print(" cat /mnt/onboard/.apps/koboWeather/location")
    print("If the information is incorrect, re-set your location with:")
    print(" /mnt/onboard/.apps/koboWeather/set_location.sh")
    
def to_hex(color):
    hex_chars = "0123456789ABCDEF"
    return hex_chars[color / 16] + hex_chars[color % 16]
    
def convert_to_raw(surface):
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
    
    
def get_weather_data():
    
    print("Getting weather information . . .")

    try:
        location = open("location", "r")
        lat = location.readline().strip()
        lon = location.readline().strip()
        location.close()
    except IOError:
        print("\nCouldn't open location file.")
        print("Run the 'set_location.sh' script to set your location for the weather script.")
        return 1
    #print(lat, lon)
    #weather_link = 'http://graphical.weather.gov/xml/SOAP_server/ndfdSOAPclientByDay.php?whichClient=NDFDgenByDay&lat={0}&lon={1}&format=24+hourly&numDays=5&Unit=e'.format(lat, lon)
    weather_link='http://free.worldweatheronline.com/feed/weather.ashx?q={0},{1}&format=xml&num_of_days=5&key=525804183f140652120211'.format(lat, lon)
    #print(weather_link)
    weather_xml = urllib2.urlopen(weather_link)
    weather_data = weather_xml.read()
    weather_xml.close()

    dom = parseString(weather_data)
    
    unit_file = open("unit.txt", "r")
    unit = unit_file.read()
    unit_file.close()
    unit = unit.strip().upper()

    h_temps = dom.getElementsByTagName('tempMax%s' % unit)
    l_temps = dom.getElementsByTagName('tempMin%s' % unit)
    highs = []
    lows = []
    for i in h_temps:
        try:
            highs.append(str(i.firstChild.nodeValue))
        except AttributeError as error:
            print("Error getting temperature highs: " + str(error))
                    
    for i in l_temps:
        try:
            lows.append(str(i.firstChild.nodeValue))
        except AttributeError as error:
            print("Error getting temperature lows: " + str(error))

              
    conditions = []
    for con in dom.getElementsByTagName('weatherDesc')[1:]:
        conditions.append(str(con.firstChild.nodeValue))
        
    now = datetime.now()
    day3 = now + timedelta(days=2)
    day4 = now + timedelta(days=3)
    day5 = now + timedelta(days=4)
    days = ["Today", "Tomorrow", day3.strftime("%A"), day4.strftime("%A"), day5.strftime("%A")]

    # images
    # The first image link is for the current weather, which we don't want.
    icons = dom.getElementsByTagName('weatherIconUrl')[1:]
    img_links = []
    for i in icons:
        try:
            link = "icons/" + str(i.firstChild.nodeValue)[72:]
        except AttributeError as error:
            print("Error getting icon links: " + str(error))
        img_links.append(link)
        
        
    #print(img_links)
    #print(highs, lows)
    #print(conditions)
    #print(days)
    
    display(days, highs, lows, conditions, img_links, unit)


def display(days, highs, lows, conditions, img_links, unit):
    
    print("Creating image . . .")
    
    pygame.display.init()
    pygame.font.init()
    pygame.mouse.set_visible(False)

    white = (255, 255, 255)
    black = (0, 0, 0)
    gray = (125, 125, 125)

    display = pygame.display.set_mode((800, 600), pygame.FULLSCREEN)
    screen = pygame.Surface((600, 800))
    screen.fill(white)

    tiny_font = pygame.font.Font("Cabin-Regular.otf", 18)
    small_font = pygame.font.Font("Fabrica.otf", 22)
    font = pygame.font.Font("Forum-Regular.otf", 40)
    comfortaa = pygame.font.Font("Comfortaa-Regular.otf", 60)
    comfortaa_small = pygame.font.Font("Comfortaa-Regular.otf", 35)

    # Dividing lines
    pygame.draw.line(screen, gray, (10, 200), (590, 200))
    pygame.draw.line(screen, gray, (10, 400), (590, 400))
    pygame.draw.line(screen, gray, (200, 410), (200, 790))
    pygame.draw.line(screen, gray, (400, 410), (400, 790))

    # Today
    date = small_font.render(days[0], True, black, white)
    date_rect = date.get_rect()
    date_rect.topleft = 10, 15

    high = small_font.render('high: ', True, black, white)
    high_rect = high.get_rect()
    high_temp = comfortaa.render(highs[0], True, black, white)
    htemp_rect = high_temp.get_rect()
    high_rect.topleft = (50, 100)
    htemp_rect.topleft = high_rect.topright

    low = small_font.render("low: ", True, black, white)
    low_rect = low.get_rect()
    low_rect.topleft = (400, 100)
    low_temp = comfortaa.render(lows[0], True, black, white)
    ltemp_rect = low_temp.get_rect()
    ltemp_rect.topleft = low_rect.topright


    condition = font.render(conditions[0], True, black, white)
    con_rect = condition.get_rect()
    con_rect.centerx = 300
    con_rect.top = 5
    # Make sure words don't overlap
    if con_rect.left < date_rect.right:
        con_rect.left = date_rect.right

    image = pygame.image.load(img_links[0])
    image.set_colorkey((255, 255, 255))
    img_rect = image.get_rect()
    img_rect.center = (300, 125)
    degrees = pygame.image.load("icons/%s.png" % unit)

    screen.blit(condition, con_rect)
    screen.blit(high, high_rect)
    screen.blit(degrees, htemp_rect.topright)
    screen.blit(degrees, ltemp_rect.topright)
    screen.blit(high_temp, htemp_rect)
    screen.blit(low, low_rect)
    screen.blit(low_temp, ltemp_rect)
    screen.blit(image, img_rect)
    screen.blit(date, date_rect)


    # Tomorrow
    date = small_font.render(days[1], True, black, white)
    date_rect = date.get_rect()
    date_rect.topleft = 10, 210

    high = small_font.render('high: ', True, black, white)
    high_rect = high.get_rect()
    high_temp = comfortaa.render(highs[1], True, black, white)
    htemp_rect = high_temp.get_rect()
    high_rect.topleft = (50, 300)
    htemp_rect.topleft = high_rect.topright

    low = small_font.render("low: ", True, black, white)
    low_rect = low.get_rect()
    low_rect.topleft = (400, 300)
    low_temp = comfortaa.render(lows[1], True, black, white)
    ltemp_rect = low_temp.get_rect()
    ltemp_rect.topleft = low_rect.topright


    condition = font.render(conditions[1], True, black, white)
    con_rect = condition.get_rect()
    con_rect.centerx = 300
    con_rect.top = 210
    if con_rect.left < date_rect.right:
        con_rect.left = date_rect.right

    image = pygame.image.load(img_links[1])
    image.set_colorkey((255, 255, 255))
    img_rect = image.get_rect()
    img_rect.center = (300, 325)

    screen.blit(condition, con_rect)
    screen.blit(high, high_rect)
    screen.blit(degrees, htemp_rect.topright)
    screen.blit(degrees, ltemp_rect.topright)
    screen.blit(high_temp, htemp_rect)
    screen.blit(low, low_rect)
    screen.blit(low_temp, ltemp_rect)
    screen.blit(image, img_rect)
    screen.blit(date, date_rect)



    # Day 3
    date = small_font.render(days[2], True, black, white)
    date_rect = date.get_rect()
    date_rect.centerx = 100
    date_rect.top = 410

    high = small_font.render('high: ', True, black, white)
    high_rect = high.get_rect()
    high_temp = comfortaa_small.render(highs[2], True, black, white)
    htemp_rect = high_temp.get_rect()
    high_rect.topright = (100, 630)
    htemp_rect.midleft = high_rect.midright

    low = small_font.render("low:  ", True, black, white)
    low_rect = low.get_rect()
    low_rect.topright = (100, 710)
    low_temp = comfortaa_small.render(lows[2], True, black, white)
    ltemp_rect = low_temp.get_rect()
    ltemp_rect.midleft = low_rect.midright


    condition = tiny_font.render(conditions[2], True, black, white)
    con_rect = condition.get_rect()
    con_rect.centerx = 100
    con_rect.top = 450

    image = pygame.image.load(img_links[2])
    image.set_colorkey((255, 255, 255))
    img_rect = image.get_rect()
    img_rect.center = (100, 540)

    screen.blit(condition, con_rect)
    screen.blit(high, high_rect)
    screen.blit(degrees, htemp_rect.topright)
    screen.blit(degrees, ltemp_rect.topright)
    screen.blit(high_temp, htemp_rect)
    screen.blit(low, low_rect)
    screen.blit(low_temp, ltemp_rect)
    screen.blit(image, img_rect)
    screen.blit(date, date_rect)



    # Day 4
    date = small_font.render(days[3], True, black, white)
    date_rect = date.get_rect()
    date_rect.centerx = 300
    date_rect.top = 410

    high = small_font.render('high: ', True, black, white)
    high_rect = high.get_rect()
    high_temp = comfortaa_small.render(highs[3], True, black, white)
    htemp_rect = high_temp.get_rect()
    high_rect.topright = (300, 630)
    htemp_rect.midleft = high_rect.midright

    low = small_font.render("low:  ", True, black, white)
    low_rect = low.get_rect()
    low_rect.topright = (300, 710)
    low_temp = comfortaa_small.render(lows[3], True, black, white)
    ltemp_rect = low_temp.get_rect()
    ltemp_rect.midleft = low_rect.midright


    condition = tiny_font.render(conditions[3], True, black, white)
    con_rect = condition.get_rect()
    con_rect.centerx = 300
    con_rect.top = 450

    image = pygame.image.load(img_links[3])
    image.set_colorkey((255, 255, 255))
    img_rect = image.get_rect()
    img_rect.center = (300, 540)

    screen.blit(condition, con_rect)
    screen.blit(high, high_rect)
    screen.blit(degrees, htemp_rect.topright)
    screen.blit(degrees, ltemp_rect.topright)
    screen.blit(high_temp, htemp_rect)
    screen.blit(low, low_rect)
    screen.blit(low_temp, ltemp_rect)
    screen.blit(image, img_rect)
    screen.blit(date, date_rect)

    # Day 5
    date = small_font.render(days[4], True, black, white)
    date_rect = date.get_rect()
    date_rect.centerx = 500
    date_rect.top = 410

    high = small_font.render('high: ', True, black, white)
    high_rect = high.get_rect()
    high_temp = comfortaa_small.render(highs[4], True, black, white)
    htemp_rect = high_temp.get_rect()
    high_rect.topright = (500, 630)
    htemp_rect.midleft = high_rect.midright

    low = small_font.render("low:  ", True, black, white)
    low_rect = low.get_rect()
    low_rect.topright = (500, 710)
    low_temp = comfortaa_small.render(lows[4], True, black, white)
    ltemp_rect = low_temp.get_rect()
    ltemp_rect.midleft = low_rect.midright


    condition = tiny_font.render(conditions[4], True, black, white)
    con_rect = condition.get_rect()
    con_rect.centerx = 500
    con_rect.top = 450

    image = pygame.image.load(img_links[4])
    image.set_colorkey((255, 255, 255))
    img_rect = image.get_rect()
    img_rect.center = (500, 540)

    screen.blit(condition, con_rect)
    screen.blit(high, high_rect)
    screen.blit(degrees, htemp_rect.topright)
    screen.blit(degrees, ltemp_rect.topright)
    screen.blit(high_temp, htemp_rect)
    screen.blit(low, low_rect)
    screen.blit(low_temp, ltemp_rect)
    screen.blit(image, img_rect)
    screen.blit(date, date_rect)

    update_time = "Last updated at " + datetime.now().strftime("%l:%M%P")
    last_update = tiny_font.render(update_time, True, gray, white)
    screen.blit(last_update, (5, 770))
    
    # Rotate the display to portrait view.
    graphic = pygame.transform.rotate(screen, 90)
    display.blit(graphic, (0, 0))
    pygame.display.update()
    
    call(["./full_update"])
    #convert_to_raw(screen)
    #call(["/mnt/onboard/.python/display_raw.sh"])
    
    
#try:
get_weather_data()
#except IndexError as error:
    #index_error(error)
