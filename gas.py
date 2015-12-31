from Adafruit_CharLCD import Adafruit_CharLCD
import RPi.GPIO as GPIO
from time import sleep
gas = 8
relay2=6

GPIO.setmode(GPIO.BCM)
GPIO.setup(6,GPIO.OUT)
GPIO.setup(gas,GPIO.IN)
lcd = Adafruit_CharLCD()

lcd.begin(16, 2)
lcd.clear()


while True:
    if(GPIO.input(gas) == 0):
        lcd.setCursor(13,0)
        lcd.message("GP")
        print "GP"
        GPIO.output(relay2,True)
        sleep(1)
    else:
        lcd.setCursor(13,0)
        lcd.message("NG")
        print "NG"
        GPIO.output(relay2,False)
        sleep(1)
