#!/usr/bin/python
import smbus
import time
from Adafruit_CharLCD import Adafruit_CharLCD
from time import sleep, strftime

lcd = Adafruit_CharLCD()

lcd.begin(16, 2)

# Define some constants from the datasheet
 
DEVICE     = 0x23 # Default device I2C address
 
POWER_DOWN = 0x00 # No active state
POWER_ON   = 0x01 # Power on
RESET      = 0x07 # Reset data register value
# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_HIGH_RES_MODE_1 = 0x20

 
bus = smbus.SMBus(1)  # Rev 2 Pi uses 1
 
def convertToNumber(data):
  # Simple function to convert 2 bytes of data
  # into a decimal number
  return ((data[1] + (256 * data[0])) / 1.2)
 
def readLight(addr=DEVICE):
  data = bus.read_i2c_block_data(addr,ONE_TIME_HIGH_RES_MODE_1)
  return convertToNumber(data)
lcd.clear()
while True:
    lux = readLight()
    lux=round(lux,2)
    print lux
    print "light Level is " + str(lux) + " lx"
    lcd.setCursor(3,1)
    lux=round(lux,1)
    lcd.message("L:" +str(lux))
    time.sleep(1)

