#!/usr/bin/python

from Adafruit_CharLCD import Adafruit_CharLCD
from time import sleep, strftime
from datetime import datetime

lcd = Adafruit_CharLCD()

lcd.begin(16, 2)

# availble functions
#   lcd.home()
#   lcd.clear()
#   lcd.setCursor(col, row)
#   lcd.noCursor()
#   lcd.message(*str)
#
#
#


lcd.clear()
count = 0;
while 1:
    lcd.setCursor(0,0)
    lcd.message('Count:')
    count = count + 1
    lcd.setCursor(7,0)
    lcd.message("{0}".format(count))
    lcd.setCursor(0,1)
    lcd.message(datetime.now().strftime('%b %d  %H:%M:%S\n'))
    sleep(0.2)
