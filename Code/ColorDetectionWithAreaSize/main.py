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
    
    contours_area, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    red_area = 0
    if contours_area:
        largest_red = max(contours_area, key=cv2.contourArea)
        red_area = int(cv2.contourArea(largest_red))
        if red_area > 500:
            cv2.drawContours(frame, [largest_red], -1, (0 ,0, 255), 3)
            cv2.putText(frame, f"Red Area: {red_area}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2) 
    
    contours_area, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    green_area = 0
    if contours_area:
        largest_green = max(contours_area, key=cv2.contourArea)
        green_area = int(cv2.contourArea(largest_green))
        if green_area > 500:
            cv2.drawContours(frame, [largest_green], -1, (0 ,0, 255), 3)
            cv2.putText(frame, f"Green Area: {green_area}", (100, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2) 
    
    
    cv2.imshow("Color Detection with Area", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


camera.release()
cv2.destroyAllWindows()