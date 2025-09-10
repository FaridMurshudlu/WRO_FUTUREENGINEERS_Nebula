import cv2 as cv
import numpy as np
from math import atan

# ========================== SIGNAL DETECTION ==========================
def signal_detection(image, signal_size, weight, object_size, focal_distance, px, l):
    img = image.copy()
    blurred = cv.medianBlur(img, 15)
    hsv = cv.cvtColor(blurred, cv.COLOR_BGR2HSV)
    height, width = img.shape[:2]

    # --- Green mask ---
    lower_limit = np.array([25, 150, 40])
    upper_limit = np.array([85, 230, 255])
    mask1 = cv.inRange(hsv, lower_limit, upper_limit)
    kernel = np.ones((11, 11), np.uint8)
    mask1 = cv.dilate(mask1, kernel, iterations=2)
    mask1 = cv.erode(mask1, kernel, iterations=2)

    # --- Red mask ---
    lower_limit = np.array([97, 170, 70])
    upper_limit = np.array([180, 255, 255])
    mask2 = cv.inRange(hsv, lower_limit, upper_limit)
    mask2 = cv.dilate(mask2, kernel, iterations=2)
    mask2 = cv.erode(mask2, kernel, iterations=2)

    # --- Detect GREEN contours ---
    contours1, _ = cv.findContours(mask1, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)[-2:]
    for cnt in contours1:
        if cv.contourArea(cnt) > height * width * 0.012:
            (cx, cy), radius = cv.minEnclosingCircle(cnt)
            x, y, w, h = cv.boundingRect(cnt)
            cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv.putText(img, "Green", (x, y), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            dis, latx = d_l(x + w // 2, h, signal_size, focal_distance, l)
            try:
                angle = 100 - (180/np.pi*(atan(dis/abs(latx))))
            except ZeroDivisionError:
                angle = 30

            angle = max(angle, 40)  # Prevent too sharp turns

            if dis < 60:
                return img, [1, int(cx < (width // 2 - object_size // 2)), angle, dis, latx]

    # --- Detect RED contours ---
    contours2, _ = cv.findContours(mask2, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)[-2:]
    for cnt in contours2:
        if cv.contourArea(cnt) > height * width * 0.012:
            (cx, cy), radius = cv.minEnclosingCircle(cnt)
            x, y, w, h = cv.boundingRect(cnt)
            cv.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv.putText(img, "Red", (x, y), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            dis, latx = d_l(x + w // 2, h, signal_size, focal_distance, l)
            try:
                angle = 100 - (180/np.pi*(atan(dis/abs(latx))))
            except ZeroDivisionError:
                angle = 30

            angle = max(angle, 40)

            if dis < 60:
                return img, [0, int(cx > (width // 2 + object_size // 2)), angle, dis, latx]

    return img, [2, 0, 0]


# ========================== HELPER FUNCTIONS ==========================
def d_l(sx, sy, object_size, f, window_size):
    y = sy * 0.0264583333  # pixel → cm
    distance_from_object = int((f * object_size) / y)
    x = ((window_size // 2) - sx) * 0.0264583333
    rx = int(((x * distance_from_object) / f))
    return distance_from_object, rx


def get_real_coords(x1, x2, y1, y2, l, b):
    m = (y2 - y1) / (x2 - x1)
    coords = [
        int((m*x1 - y1 + 0) / m),
        int(y1 - m*(x1 - 0)),
        int((m*x1 - y1 + b) / m),
        int(y1 - m*(x1 - l))
    ]
    # Clamp to image bounds
    for i in range(len(coords)):
        if i % 2 == 0:
            coords[i] = 0 if coords[i] < 0 or coords[i] > l else coords[i]
        else:
            coords[i] = 0 if coords[i] < 0 or coords[i] > b else coords[i]

    rx1 = ry1 = rx2 = ry2 = 0
    if coords[0] != 0: rx1, ry1 = coords[0], 1
    if coords[1] != 0:
        if ry1 == 0: rx1, ry1 = 1, coords[1]
        else: rx2, ry2 = 1, coords[1]
    if coords[2] != 0:
        if rx1 == 0: rx1, ry1 = coords[2], b
        else: rx2, ry2 = coords[2], b
    if coords[3] != 0:
        if ry1 == 0: rx1, ry1 = l, coords[3]
        else: rx2, ry2 = l, coords[3]
    return rx1, ry1, rx2, ry2


def find_lines(line_details):
    rho, theta = line_details[0]
    a, b = np.cos(theta), np.sin(theta)
    x0, y0 = a*rho, b*rho
    return int(x0 + 1000*-b), int(x0 - 1000*-b), int(y0 + 1000*a), int(y0 - 1000*a)


def warpImg(img, points, w, h, inv=False):
    pts1 = np.float32(points)
    pts2 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
    matrix = cv.getPerspectiveTransform(pts2, pts1) if inv else cv.getPerspectiveTransform(pts1, pts2)
    return cv.warpPerspective(img, matrix, (w, h))


# ========================== WALL DETECTION ==========================
def wall_detection(image, l, b, threshold):
    points = np.float32([(13, 73), (l - 13, 73), (0, 118), (l, 118)])
    img = warpImg(image, points, l, b)
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    # Green/Yellow mask
    lower_limit = np.array([25, 150, 40])
    upper_limit = np.array([85, 230, 255])
    mask1 = cv.inRange(hsv, lower_limit, upper_limit)

    # Red mask
    lower_limit = np.array([97, 170, 70])
    upper_limit = np.array([180, 255, 255])
    mask2 = cv.inRange(hsv, lower_limit, upper_limit)

    mask = cv.bitwise_or(mask1, mask2)  # combine both
    edges = cv.Canny(mask, 100, 200)
    lines = cv.HoughLines(edges, 1, np.pi/180, 50)

    right_wall = left_wall = front_wall = 0
    line_slopes = []

    if lines is not None:
        for line in lines:
            try:
                x1, x2, y1, y2 = find_lines(line)
                angle = 180/np.pi*atan(1/((y2 - y1) / (x2 - x1)))
                if round(angle) not in line_slopes:
                    cv.line(img, (x1, y1), (x2, y2), (0, 255, 255), 2)
                    line_slopes.append(round(angle))
                    if angle > 45 or angle < -45:
                        front_wall = angle
                    elif angle > 0:
                        right_wall = angle
                    else:
                        left_wall = angle
            except ZeroDivisionError:
                pass

    if left_wall != 0 and abs(left_wall) > threshold:
        return img, "R", abs(left_wall)
    if right_wall != 0 and abs(right_wall) > threshold:
        return img, "L", abs(right_wall)
    if front_wall != 0:
        return img, "F", abs(front_wall)

    return img, "N", 0
