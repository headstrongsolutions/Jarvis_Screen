# -*- coding: utf-8 -*-
import pygame, gettime, getip, METWeather, Timecycle, Command_Centre, text_generator as text

# METWeather
knowledge_METWeather = METWeather.METWeather()

# Timecycle for METWeather
metWeatherTimecycle = Timecycle.Timecycle()

# System Commands
commands = Command_Centre.Command_Centre()

pygame.init()
screen = pygame.display.set_mode((656,416))
# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set the background to black
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0, 0, 250))
 
clock = pygame.time.Clock()

weather_icon_data = ""
weather_temperature_data = ""
weather_rain_probability_data = ""
house_temperature_data = ""
weather_later = ""
weather_days = ""

# Define the character icon to weather type lookup
weather_types = {}
weather_types['NA'] = ')'
weather_types['0'] = '1'
weather_types['1'] = 'B'
weather_types['2'] = '4'
weather_types['3'] = 'H'
weather_types['4'] = ')'
weather_types['5'] = 'J'
weather_types['6'] = 'M'
weather_types['7'] = 'N'
weather_types['8'] = 'N'
weather_types['9'] = '7'
weather_types['10'] ='Q'
weather_types['11'] ='Q'
weather_types['12'] ='Q'
weather_types['13'] ='8'
weather_types['14'] ='R'
weather_types['15'] ='R'
weather_types['16'] ='"'
weather_types['17'] ='U'
weather_types['18'] ='U'
weather_types['19'] ='$'
weather_types['20'] ='X'
weather_types['21'] ='X'
weather_types['22'] ='#'
weather_types['23'] ='W'
weather_types['24'] ='W'
weather_types['25'] ='W'
weather_types['26'] ='W'
weather_types['27'] ='W'
weather_types['28'] ='&'
weather_types['29'] ='P'
weather_types['30'] ='O'

# Define Fonts
font_weather_icons = ['fonts/meteocons-webfont.ttf', 'meteoconsregular']
font_standard = ['helveticaneue','texgyreheros']


def get_screen_height():
    x, y = screen.get_size()
    return y

def get_width(this):
    x, y = this.get_size()
    return x

def get_height(this):
    x, y = this.get_size()
    return y

def get_screen_width():
    x, y = screen.get_size()
    return x

def get_weather(weather_icon_data, weather_temperature_data, weather_rain_probability_data, house_temperature_data, weather_later, weather_days):
    # Should we get a new weather result?
    time_check_result = metWeatherTimecycle.time_check()
    weather_now = False
    weather_later = False
    weather_days = False

    if(time_check_result):
        knowledge_METWeather.get_weather_now()
        # Format the now weather to something nice
        weather_now = knowledge_METWeather.format_weather_now()
        weather_later = knowledge_METWeather.format_weather_later()
        weather_days = knowledge_METWeather.format_future_days()

    # Breakout the data to individual rows
    if weather_now:
        weather_icon_data = weather_types[weather_now['W'][1].strip()]
        weather_temperature_data = weather_now['F']
        weather_rain_probability_data = weather_now['Pp']
        house_temperature_data = "temp/hum data"

    return (weather_icon_data, weather_temperature_data, weather_rain_probability_data, house_temperature_data, weather_later, weather_days)

# disable mouse cursor
pygame.mouse.set_visible(0)

while 1:
    screen.fill(BLACK)
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    # Check System Commands
    commands.check_command_and_run()

    # Time and Date display
    current_time = text.create_standard_text(gettime.get_time_now(), font_standard, 105, WHITE) 
    current_date = text.create_standard_text(gettime.get_date_now(), font_standard, 39, WHITE)

    # MET Weather
    weather_later_count =  4
    weather_days_count =  4
    weather_later_icons = {}
    weather_later_temps = {}
    weather_later_timeslots = {}
    weather_days_icons = {}
    weather_days_temps = {}
    weather_days_names = {}

    (weather_icon_data, weather_temperature_data, weather_rain_probability_data, house_temperature_data, weather_later, weather_days) = get_weather(weather_icon_data, weather_temperature_data, weather_rain_probability_data, house_temperature_data, weather_later, weather_days)
    if weather_icon_data != "":
        weather_icon = text.create_weather_text(weather_icon_data, font_weather_icons, 100, WHITE)
        weather_temperature = text.create_standard_text(weather_temperature_data[1].replace(" ", "").lower(), font_standard, 40, WHITE)
        weather_rain_probability = text.create_standard_text("rain: %s" % (weather_rain_probability_data[1]), font_standard, 12, WHITE)

        if len(weather_later) < weather_later_count:
                weather_later_count = len(weather_later)
        if weather_later:
            count = 0
            while (count < weather_later_count):
                for weather_day_key, weather_day_value in weather_days.items():
                    weather_later_icons[count] = text.create_weather_text("%s" % (weather_day_value['W']), font_weather_icons, 34, WHITE)
                    weather_later_temps[count] = text.create_standard_text("%sc" % (weather_day_value['F']), font_standard, 17, WHITE)
                    weather_later_timeslots[count] = text.create_standard_text("%s" % (weather_day_key), font_standard, 16, WHITE)
                    count += 1
            
            future_weather_icon = text.create_weather_text(weather_icons, font_weather_icons, 34, WHITE)
            future_weather_temp = text.create_standard_text(weather_temps, font_standard, 17, WHITE)
            future_weather_timeslot = text.create_standard_text(weather_timeslots, font_standard, 16, WHITE)

        if len(weather_days) < weather_days_count:
                weather_days_count = len(weather_days)
        if weather_days:
            count = 0
            while (count < weather_days_count):
                for weather_day_key, weather_day_value in weather_days.items():
                    weather_days_icons[count] = text.create_weather_text("%s" % (weather_day_value['W']), font_weather_icons, 34, WHITE)
                    weather_days_temps[count] = text.create_standard_text("%sc" % (weather_day_value['F']), font_standard, 17, WHITE)
                    weather_days_names[count] = text.create_standard_text("%s" % (weather_day_key), font_standard, 16, WHITE)
                    count += 1
            

    # House Temperature
    house_temperature = text.create_standard_text("unimplemented", font_standard, 20, WHITE)
    
    # System Infomation
    ip = text.create_standard_text(getip.get_ip_address(), font_standard, 12, WHITE)
    screen_size = text.create_standard_text("X:%spx / Y:%spx" % screen.get_size(), font_standard, 12, WHITE)

    screen.blit(current_time, (0, -17))
    screen.blit(current_date, (0, 100))
    screen.blit(weather_icon, (470, 0))
    screen.blit(weather_temperature, (575, 40))
    screen.blit(weather_rain_probability, (580, 85))
    for i in xrange(weather_later_count):
        screen.blit(weather_later_icons[i], (465 + i * 50, 100))
        screen.blit(weather_later_temps[i], (468 + i * 50, 145))
        screen.blit(weather_later_timeslots[i], (470 + i * 50, 170))
    for i in xrange(weather_days_count):
        screen.blit(weather_days_icons[i], (465 + i * 50, 210))
        screen.blit(weather_days_temps[i], (468 + i * 50, 245))
        screen.blit(weather_days_names[i], (470 + i * 50, 270))
    screen.blit(house_temperature, (465, 300))

    # Would be nice to control the visibility of the sys info form the command module
    screen.blit(screen_size, (0, get_height(screen) - get_height(screen_size)))
    screen.blit(ip, (get_width(screen) - get_width(ip), get_height(screen) - get_height(ip)))

    pygame.display.flip()
