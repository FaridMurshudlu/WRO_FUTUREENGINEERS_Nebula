import cv2
import numpy as np

def nothing(x):
    pass

camera = cv2.VideoCapture(0)

cv2.namedWindow("HSV")
cv2.createTrackbar("LH", "HSV", 0, 179, nothing)
cv2.createTrackbar("UH", "HSV", 255, 255, nothing)

cv2.createTrackbar("LS", "HSV", 0, 255, nothing)
cv2.createTrackbar("US", "HSV", 255, 255, nothing)

cv2.createTrackbar("LV", "HSV", 0, 255, nothing)
cv2.createTrackbar("UV", "HSV", 255, 255, nothing)

while True:
    _, frame = camera.read()
    hsv_format = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    
    lh = cv2.getTrackbarPos("LH", "HSV")
    uh = cv2.getTrackbarPos("UH", "HSV")
    ls = cv2.getTrackbarPos("LS", "HSV")
    us = cv2.getTrackbarPos("US", "HSV")  
    lv = cv2.getTrackbarPos("LV", "HSV")
    uv = cv2.getTrackbarPos("UV", "HSV") 
    
    lower = np.array([lh, ls, lv])
    upper = np.array([uh, us, uv])
    
    mask = cv2.inRange(hsv_format, lower, upper)
    result = cv2.bitwise_and(frame, frame, mask=mask)
    
    cv2.imshow("Original", frame)
    cv2.imshow("Mask", mask)
    cv2.imshow("Result", result)
    
    cv2.waitKey(1)