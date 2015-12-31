import os
import glob
import time
from Adafruit_CharLCD import Adafruit_CharLCD
from time import sleep, strftime
lcd = Adafruit_CharLCD()

lcd.begin(16, 2)

os.system('modprobe w1-gpio') # this is specific to ds18b20
os.system('modprobe w1-therm')# this is specific to ds18b20
base_dir = '/sys/bus/w1/devices/' #address of base directory
#in linux, every device connected to system is considered as a single FILE
# and its address is shown above

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
lcd.clear()

while True:
    degC,degf=read_temp()
    print degC
    lcd.setCursor(5,1)
    lcd.message("T:"+str(degC))
    time.sleep(1)

