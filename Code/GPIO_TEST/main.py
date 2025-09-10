import RPI.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.OUT)    # if red block comes      
GPIO.setup(27,  GPIO.OUT)   # if greeen block comes


try:
    while True:
        # if red block comes:
        GPIO.output(17, GPIO.HIGH)
        GPIO.output(27, GPIO.LOW)
        
        # if green block comes:
        GPIO.output(17, GPIO.LOW)
        GPIO.output(27, GPIO.HIGH)
        
except KeyboardInterrupt:
    print("Problem with GPIO pins")
finally:
    GPIO.cleanup()
        