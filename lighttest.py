#!/usr/bin/python
import smbus
import time
 
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

while True:
    lux = readLight()
    print lux
    print "light Level is " + str(lux) + " lx"
    time.sleep(1)

