from Adafruit_CharLCD import Adafruit_CharLCD
import RPi.GPIO as GPIO
from time import sleep
pir = 27
relay1 = 5
GPIO.setmode(GPIO.BCM)
GPIO.setup(5,GPIO.OUT)
GPIO.setup(pir,GPIO.IN)

lcd = Adafruit_CharLCD()

lcd.begin(16, 2)
lcd.clear()
while True:
    if(GPIO.input(pir) == 1):
        lcd.setCursor(10,0)
        lcd.message("TD")
        print "TD"
        GPIO.output(relay1,True)
        sleep(1)
    else:
        lcd.setCursor(10,0)
        lcd.message("NT")
        print "NT"
        GPIO.output(relay1,False)
        sleep(1)
    
