from flask import Flask, render_template
#import Adafruit_BMP.BMP085 as BMP085
import time
import datetime
import sys
import math
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
relay3=13
relay4=19
led1 = 12
led2 = 16
led3 = 20
led4 = 21
gas = 8
GPIO.setmode(GPIO.BCM)
GPIO.setup(5,GPIO.OUT)
GPIO.setup(6,GPIO.OUT)
GPIO.setup(pir,GPIO.IN)
GPIO.setup(gas,GPIO.IN)
GPIO.setup(5,GPIO.OUT)
GPIO.setup(relay1,GPIO.OUT)
GPIO.setup(relay2,GPIO.OUT)
GPIO.setup(relay3,GPIO.OUT)
GPIO.setup(relay4,GPIO.OUT)
GPIO.setup(led1,GPIO.OUT)
GPIO.setup(led2,GPIO.OUT)
GPIO.setup(led3,GPIO.OUT)
GPIO.setup(led4,GPIO.OUT)
############################################################################################

#upto this


app = Flask(__name__)

@app.route('/SENS.csv',methods=['GET','POST'])
def textf():
	error = None
	myfile = open("SENS.txt ","r")
	strg = myfile.read()
	myfile.close()
	#response = make_response(csv)
	#response.header["Content-Disposition"]= "attachment;filename=sens.csv"
	return strg
	#return strg

@app.route("/r4on",methods=['GET','POST'])
def hello4():
	GPIO.output(relay4,GPIO.HIGH)
	GPIO.output(led4,True)
	return "relay 4 turned on"


@app.route("/r4off",methods=['GET','POST'])
def hello5():
	GPIO.output(relay4,GPIO.LOW)
	GPIO.output(led4,False)	
	return "relay 4 turned off"

@app.route("/r3on",methods=['GET','POST'])
def hello6():
	GPIO.output(relay3,GPIO.HIGH)
	GPIO.output(led3,True)
	return "relay 3 turned on"
@app.route("/r3off",methods=['GET','POST'])
def hello7():
	GPIO.output(relay3,GPIO.LOW)
	GPIO.output(led3,False)	
	return "relay 3 turned off"

@app.route("/r2on",methods=['GET','POST'])
def hello21():
	GPIO.output(relay2,GPIO.HIGH)
	GPIO.output(led2,True)
	return "relay 2 turned on"

@app.route("/r2off",methods=['GET','POST'])
def hello22():
	GPIO.output(relay2,GPIO.LOW)
	GPIO.output(led2,False)	
	return "relay 2 turned off"

@app.route("/r1on",methods=['GET','POST'])
def hello2():
	GPIO.output(relay1,GPIO.HIGH)
	GPIO.output(led1,True)
	return "relay 1 turned on"
@app.route("/r1off",methods=['GET','POST'])
def hello3():
	GPIO.output(relay1,GPIO.LOW)
	GPIO.output(led1,False)	
	return "relay 1 turned off"

@app.route("/")
def hello():
    degC,degf=read_temp()
    degC = round(degC,1)
    #print degC
    lcd.setCursor(10,1)
    lcd.message("T:"+str(degC))
    lux = readLight()
    lux = round(lux,2)
    #print "light Level is " + str(lux) + " lx"
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
    #time.sleep(2)
    if(GPIO.input(pir) == 1):
        lcd.setCursor(10,0)
        lcd.message("TD")
        pstring = 'Present'
        print "TD"
        GPIO.output(relay1,True)
        #sleep(1)
    else:
        lcd.setCursor(10,0)
        lcd.message("NT")
        print "NT"
        pstring = 'No'
        GPIO.output(relay1,False)
        #sleep(1)
    if(GPIO.input(gas) == 0):
        lcd.setCursor(13,0)
        lcd.message("GP")
        print "GP"
        gstring = 'Yes'
        GPIO.output(relay2,True)
        #sleep(1)
    else:
        lcd.setCursor(13,0)
        lcd.message("NG")
        gstring = 'No'
        print "NG"
        GPIO.output(relay2,False)
        #sleep(1)
    #########################################################################
    now = datetime.datetime.now()
    timeString = now.strftime("%d-%m-%Y %H:%M")
    #text_file = open("SENS.txt","a")
    #text_file.write(timeString + str(tempr) + str(pressure) + str(altitude) + str(countvalue) + str(distance) + '\n\r\r\n')
    #text_file.write("\r")
    #text_file.close()
    #csvfile = open("SENS.csv","a")
    #csvfile.write(timeString + ',' + str(tempr) + ',' + str(pressure) + ',' + str(altitude) + ',' + str(countvalue) + ',' + str(distance) + '\r\n\r\n')
    #csvfile.close()
    #lcd.set_cursor(0,0)
    #lcd.message(tempr)
    
    #lcd.message(" ")
    #lcd.message(str(pressure))
    #lcd.message(str(pressure))
    #lcd.set_cursor(0,1)
    #lcd.message("Cnt:")
    #lcd.message(str(countvalue))
    #lcd.message(" ")
    #lcd.message("D:")
    #lcd.message(str(distance))
    #lcd.message("cm")
    #lcd.message("     ")
    templateData = {
	'title' : 'HELLO!',
	'time' : timeString,
	'temp' :degC,
	'pirsens' :pstring,
	'lgt' : lux,
	'humid' : humidity,
	'lpg' : gstring #this is ultrasonic sensor value
	}
    return render_template('main2.html',**templateData)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
    
