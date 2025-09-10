import cv2

camera = cv2.VideoCapture(0)

while True:
    
    _, frame = camera.read()
    print(frame)
    cv2.imshow("frame", frame)
    
    cv2.waitKey(1)