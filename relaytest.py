import RPi.GPIO as GPIO
from time import sleep
relay1 = 5
relay2 = 6
relay3 = 13
relay4 = 19
led1 = 12
led2 = 16
led3 = 20
led4 = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(relay1,GPIO.OUT)
GPIO.setup(relay2, GPIO.OUT)
GPIO.setup(relay3,GPIO.OUT)
GPIO.setup(relay4, GPIO.OUT)
GPIO.setup(led1,GPIO.OUT)
GPIO.setup(led2, GPIO.OUT)
GPIO.setup(led3,GPIO.OUT)
GPIO.setup(led4, GPIO.OUT)

while True:
    GPIO.output(led1,1)
    GPIO.output(led2,1)
    GPIO.output(led3,1)
    GPIO.output(led4,1)
    GPIO.output(relay1,1)
    GPIO.output(relay2,1)
    GPIO.output(relay3,1)
    GPIO.output(relay4,1)
    sleep(1)
    GPIO.output(led1,0)
    GPIO.output(led2,0)
    GPIO.output(led3,0)
    GPIO.output(led4,0)
    GPIO.output(relay1,0)
    GPIO.output(relay2,0)
    GPIO.output(relay3,0)
    GPIO.output(relay4,0)
    sleep(1)
