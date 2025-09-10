import cv2 as cv
import numpy as np
import io
import time
import utlis

lap_number = 0
rotation = 1

# Certain constants
Px = 0.0264583333  # Pixel to cm conversion
Focal_distance = 3  # Approx
Signal_size = 10  # in cm
Weight = 5
Object_size = int(100 * 0.3)
speed = 100
motor_power = 0.5

l = 160
b = 120

camera = cv.VideoCapture(1)
order = 0
time.sleep(0.1)

while True:
    _, frame = camera.read()
    image = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
    if frame is not None:    
        start = time.time()
        if lap_number != 3:            
            if order == 0:
                # ------------- Detects the signals and determines the direction to turn ----------------
                Signal_img, Signal_data = utlis.signal_detection(image, Signal_size, Weight, Object_size, Focal_distance, Px, l)
                cv.imshow("Signal Image", Signal_img)
                # pwm_2.ChangeDutyCycle(speed)
                # Processes the signal detection data
                data = Signal_data
                print(data)
                if data[0] == 1:
                    if data[1] == 0:
                        if data[4] < 15:
                            print("LEFT")
                            # rotation = utlis.left_angle(pwm_1, pwm_2, IN2, IN1, IN3, IN4, rotation, data[2], motor_power, speed)
                        
                    else:
                        if data[4] < 15:
                            print("left")
                            # rotation = utlis.left_angle(pwm_1, pwm_2, IN2, IN1, IN3, IN4, rotation, data[2], motor_power, speed)
                        else:
                            print("Centered")
                            # rotation = utlis.centered(pwm_1, IN2, IN1, rotation, motor_power, speed)
        
                elif data[0] == 0:
                    if data[1] == 0:
                        if data[4] < 15:
                            print("RIGHT")
                            # rotation = utlis.right_angle(pwm_1, pwm_2, IN2, IN1, IN3, IN4, rotation, data[2], motor_power, speed)
                    else:
                        if data[4] < 15:
                            print("RIGHT")
                            # rotation = utlis.right_angle(pwm_1, pwm_2, IN2, IN1, IN3, IN4, rotation, data[2], motor_power, speed)
                        else:
                            print("Centered")
                            # rotation = utlis.centered(pwm_1, IN2, IN1, rotation, motor_power, speed)
                else:
                    pass
                    # rotation = utlis.centered(pwm_1, IN2, IN1, rotation, motor_power, speed)
                order += 1
                
            elif order == 1:
                #-------------- Detects the lanes and determines the angle to turn -------------
                Wall_img, Wall_data, Wall_angle = utlis.wall_detection(image, l, b, 6)
                cv.imshow("Lane Image", image)
                # Processes the lane detection data
                data = Wall_data
                angle = Wall_angle
                angle += 10
                print(data, angle)
                if data == "R":
                    print("LEFT")
                    # rotation = utlis.right_angle(pwm_1, pwm_2, IN2, IN1, IN3, IN4, rotation, angle, motor_power, speed)
                        
                elif data == "L":
                    print("RIGHT")
                    # rotation = utlis.left_angle(pwm_1, pwm_2, IN2, IN1, IN3, IN4, rotation, angle, motor_power, speed)
                    
                elif data == "F":
                    print("Wall")
                    # rotation = utlis.left_angle(pwm_1, pwm_2, IN2, IN1, IN3, IN4, rotation, angle, motor_power, speed)
                        
                elif data == "N":
                    print("Nothing")
                    # rotation = utlis.centered(pwm_1, IN2, IN1, rotation, motor_power, speed)
                order -= 1 

            # --------------- All the processing is over ------------------
            # end = time.time()
            # print("FPS :", 1/(end - start))
            cv.waitKey(1)
        else:
            break
