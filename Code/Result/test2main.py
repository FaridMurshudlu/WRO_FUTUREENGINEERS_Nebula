import cv2 as cv 
from test2main import signal_detection

camera = cv.VideoCapture(1)
while True:
    _, frame = camera.read()
    image = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
    image, _, _ = signal_detection(image, 7, 2, 7, 27, 640, 160)
    cv.imshow("Frame", image)
    cv.waitKey(1)