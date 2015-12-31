from Adafruit_CharLCD import Adafruit_CharLCD
import Adafruit_DHT
import time

sensor = Adafruit_DHT.DHT22

pin = 22

lcd = Adafruit_CharLCD()

lcd.begin(16, 2)
lcd.clear()
while True:
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity is not None and temperature is not None:
        print "humidity is " + str(humidity)
        lcd.setCursor(0,0)
        lcd.message("Humidity: " + str(humidity))
    else:
        print 'Failed to get reading. Try again!'
    time.sleep(2)
