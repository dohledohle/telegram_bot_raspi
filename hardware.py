from rpi_lcd import LCD
from gpiozero import Button

lcd = LCD()
button = Button(17, bounce_time=0.2)
help(LCD)
