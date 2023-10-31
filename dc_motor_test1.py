import RPi.GPIO as GPIO
import time

In1 = 17 # GPIO17
In2 = 27 # GPIO 27
en = 22  # GPIO 22 Enable
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(In1,GPIO.OUT)
GPIO.setup(In2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)

p = GPIO.PWM(en, 50) # GPIO 17 for PWM with 50Hz
p.start(25) # Initialization
try:
    while(True):
        print('motor running forward')
        GPIO.output(In1,GPIO.HIGH)
        GPIO.output(In2,GPIO.LOW)
except KeyboardInterrupt:   # Ctrl C
    p.stop()
    GPIO.cleanup()  
    