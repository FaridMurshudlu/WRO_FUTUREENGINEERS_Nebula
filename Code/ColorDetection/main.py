import cv2
import numpy as np


camera = cv2.VideoCapture(0)

while True:
    
    ret, frame = camera.read()
    
    if not ret:
        break
    
    frame = cv2.resize(frame, (640, 480))
    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    
    lower_red1 = np.array([10, 120, 20])
    upper_red1 = np.array([])
    
    lower_red2 = np.array([])
    upper_red2 = np.array([])
    
    lower_green = np.array([])
    upper_green = np.array([])
    
    
    mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)
    
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    
    result_red = cv2.bitwise_and(frame, frame, mask=mask_red)
    result_greeen = cv2.bitwise_and(frame, frame, mask=mask_green)
                                    
    cv2.imshow("Original", frame)  
    cv2.imshow("Red Detector", result_red)
    cv2.imshow("Green Detector", result_greeen)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


camera.release()
cv2.destroyAllWindows()