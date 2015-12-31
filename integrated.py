from Adafruit_CharLCD import Adafruit_CharLCD
import Adafruit_DHT
import smbus
import time
import RPi.GPIO as GPIO
from time import sleep

#############################################################################
import os
import glob
os.system('modprobe w1-gpio') # this is specific to ds18b20
os.system('modprobe w1-therm')# this is specific to ds18b20
base_dir = '/sys/bus/w1/devices/' #address of base d

device_folder = glob.glob(base_dir + '28*')[0] # to the base address, 28 and * means wild card is attached
# because actual sensor address starts from 28
device_file = device_folder + '/w1_slave'
def read_temp_raw():
    f = open(device_file, 'r') # read the device file with an attribute of 'r' means Read ONLY
    lines = f.readlines()#lines read the status
    f.close()   # close the file
    return lines

def read_temp():
    lines = read_temp_raw()                 # this is actual process of reading temperature from sensor, and processing it, 
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f
###########################################################################

sensor = Adafruit_DHT.DHT22
pin = 22
lcd = Adafruit_CharLCD()
lcd.begin(16, 2)
lcd.clear()
 
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
######################################################################################
pir = 27
relay1 = 5
relay2=6
gas = 8
GPIO.setmode(GPIO.BCM)
GPIO.setup(5,GPIO.OUT)
GPIO.setup(6,GPIO.OUT)
GPIO.setup(pir,GPIO.IN)
GPIO.setup(gas,GPIO.IN)

############################################################################################

while True:
    degC,degf=read_temp()
    degC = round(degC,1)
    print degC
    lcd.setCursor(10,1)
    lcd.message("T:"+str(degC))
    lux = readLight()
    lux = round(lux,2)
    print "light Level is " + str(lux) + " lx"
    lcd.setCursor(0,1)
    lux = round(lux,1)
    lcd.message("L:"+str(lux))
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity is not None and temperature is not None:
        humidity = round(humidity,2)
        print "humidity is " + str(humidity)
        lcd.setCursor(0,0)
        lcd.message("H:" + str(humidity))
    else:
        print 'Failed to get reading. Try again!'
    time.sleep(2)
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
    
    
