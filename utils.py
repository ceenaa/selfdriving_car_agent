import math
import cv2
import numpy as np


# cv2.namedWindow('trackbar')
# cv2.createTrackbar('l_h', 'trackbar', 0, 255, lambda x: x)
# cv2.createTrackbar('l_s', 'trackbar', 0, 255, lambda x: x)
# cv2.createTrackbar('l_v', 'trackbar', 200, 255, lambda x: x)
# cv2.createTrackbar('u_h', 'trackbar', 255, 179, lambda x: x)
# cv2.createTrackbar('u_s', 'trackbar', 50, 255, lambda x: x)
# cv2.createTrackbar('u_v', 'trackbar', 255, 255, lambda x: x)


# find left line
def left_line(x):
    return 1.4536741214057507 * x + 24


def right_line(x):
    return -1.6447876447876448 * x + 1104.019305019305


# find the steering angle for turning the car
def find_first_left_point(line, mask):
    for x in range(344, 0, -3):
        y = int(line(x))
        if 480 > y > 0 and mask[y][x] > 200:
            return y, x

    return None


def find_first_right_point(line, mask):
    for x in range(344, 639, 3):
        y = int(line(x))
        if 480 > y > 0 and mask[y][x] > 200:
            return y, x
    return None


def find_first_center_point(mask):
    for y in range(479, 0, -3):
        if mask[y][344] == 255:
            return y, 344

    return None


# Perspective Transformation
def bird_eye_view(image):
    tl = (88, 222)
    tr = (416, 224)
    bl = (7, 378)
    br = (475, 379)

    cv2.circle(image, tl, 5, (0, 0, 255), -1)
    cv2.circle(image, tr, 5, (0, 0, 255), -1)
    cv2.circle(image, bl, 5, (0, 0, 255), -1)
    cv2.circle(image, br, 5, (0, 0, 255), -1)

    # apply the perspective transformation

    pts1 = np.float32([tl, tr, bl, br])
    pts2 = np.float32([[0, 0], [640, 0], [0, 480], [640, 480]])

    # Matrix to warp the image for bird's eye view
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    transformed = cv2.warpPerspective(image, matrix, (640, 480))

    return transformed


# Object Detection
def extract_lines(image):
    # Image Thresholding
    hsv_transformed = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # trackbar to find the best values for the mask

    # l_h = cv2.getTrackbarPos('l_h', 'trackbar')
    # l_s = cv2.getTrackbarPos('l_s', 'trackbar')
    # l_v = cv2.getTrackbarPos('l_v', 'trackbar')
    # u_h = cv2.getTrackbarPos('u_h', 'trackbar')
    # u_s = cv2.getTrackbarPos('u_s', 'trackbar')
    # u_v = cv2.getTrackbarPos('u_v', 'trackbar')

    l_h = 0
    l_s = 0
    l_v = 197
    u_h = 179
    u_s = 255
    u_v = 255

    lower = np.array([l_h, l_s, l_v])
    upper = np.array([u_h, u_s, u_v])
    mask = cv2.inRange(hsv_transformed, lower, upper)

    return mask


def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0


# find the steering angle for drive between the lines
def drive_in_lines(left, right, center):
    left_y, left_x = 0, 0
    right_y, right_x = 0, 0
    center_y, center_x = 0, 0

    if left is not None:
        left_y, left_x = left
    if right is not None:
        right_y, right_x = right
    if center is not None:
        center_y, center_x = center

    if left is not None and right is not None:
        if center is not None:

            if center_y == left_y:
                return 90

            if center_y == right_y:
                return -90

            angle_between_left_and_center = (center_x - left_x) / (-center_y + left_y)
            angle_between_left_and_center = math.degrees(math.atan(angle_between_left_and_center))

            angle_between_right_and_center = (right_x - center_x) / (-right_y + center_y)
            angle_between_right_and_center = math.degrees(math.atan(angle_between_right_and_center))

            if abs(angle_between_left_and_center - angle_between_right_and_center) < 20:
                return sign(angle_between_left_and_center) * 90

        angle = (-right_y + left_y) / (right_x - left_x)
        angle = math.degrees(math.atan(angle))

        return angle

    elif right is None and left is not None and center is not None:
        angle = math.degrees(math.atan((center_y - left_y) / (center_x - left_x)))
        return -angle

    elif left is None and right is not None and center is not None:
        angle = math.degrees(math.atan((center_y - right_y) / (center_x - right_x)))
        return -angle

    elif left is None and center is None and right is not None:
        return 90

    elif right is None and center is None and left is not None:
        return -90

    else:
        return 0


def show_adjusting_circles(image, left, right, center):
    if left is not None:
        left_y, left_x = left
        cv2.circle(image, (left_x, left_y), 5, (0, 0, 255), -1)
    if right is not None:
        right_y, right_x = right
        cv2.circle(image, (right_x, right_y), 5, (0, 0, 255), -1)
    if center is not None:
        center_y, center_x = center
        cv2.circle(image, (center_x, center_y), 5, (0, 0, 255), -1)


def distance_to_left_line(center_x, center_y, mask):
    for x in range(center_x, 0, -1):
        if mask[center_y][x] > 200:
            return center_x - x

    return -1


def distance_to_right_line(center_x, center_y, mask):
    for x in range(center_x, 640):
        if mask[center_y][x] > 200:
            return x - center_x
    return -1


def turn_left(mask, left, right, center):
    center_x = 370
    center_y = 470
    if distance_to_left_line(center_x, center_y, mask) > 0:
        return -30, 2

    else:
        return drive_in_lines(left, right, center), 3


def keep_straight(left, right, center, flag):
    return drive_in_lines(left, right, center), flag + 1


def turn_right(mask, left, right, center, frame):
    center_x = 370
    center_y = 470

    if distance_to_right_line(center_x, center_y, mask) > 0:
        return 30, frame

    else:
        return drive_in_lines(left, right, center), 0


def get_over_obstacle(mask, left, right, center, flag, frame):
    if flag < 3:
        return turn_left(mask, left, right, center)
    elif flag < frame:
        return keep_straight(left, right, center, flag)
    else:
        return turn_right(mask, left, right, center, frame)


def cal_speed(car_angle):
    if abs(car_angle) < 10:
        car_speed = 100
    elif abs(car_angle) < 15:
        car_speed = 95
    elif abs(car_angle) < 20:
        car_speed = 90
    elif abs(car_angle) < 25:
        car_speed = 85
    elif abs(car_angle) < 30:
        car_speed = 55
    elif abs(car_angle) < 35:
        car_speed = 20
    elif abs(car_angle) < 40:
        car_speed = 10
    elif abs(car_angle) < 55:
        car_speed = 5
    elif abs(car_angle) < 55:
        car_speed = 3
    elif abs(car_angle) < 70:
        car_speed = 2
    else:
        car_speed = 0

    return car_speed


tt = 0


def drive(car, flag):
    global tt

    image = car.getImage()
    sensor = car.getSensors()

    transformed = bird_eye_view(image)
    mask = extract_lines(transformed)

    # find the left line
    left = find_first_left_point(left_line, mask)
    right = find_first_right_point(right_line, mask)
    center = find_first_center_point(mask)
    show_adjusting_circles(transformed, left, right, center)

    if flag == 0 and (sensor[2] < 1300):
        flag = 1

    if flag == 0:
        tt = 0
        angle = drive_in_lines(left, right, center)

        car.setSensorAngle(5)
        if (sensor[2] < 1499) and car.getSpeed() > 40:
            car_speed = 0
        else:
            car_speed = cal_speed(angle)

    else:

        if tt == 1 or car.getSpeed() > 60:
            frame = 100
            tt = 1
        if tt == 0:
            frame = 45

        angle, flag = get_over_obstacle(mask, left, right, center, flag, frame)
        car_speed = cal_speed(angle)

        if car.getSpeed() > 60:
            car_speed = 0

        if abs(angle) > 30 and car.getSpeed() > 50:
            car_speed = 35
        elif abs(angle) > 20 and car.getSpeed() > 50:
            car_speed = 45

    car.setSteering(angle)
    car.setSpeed(car_speed)

    if image is not None and image.any():
        # Showing the opencv type image
        cv2.imshow('frames', image)
        cv2.imshow('transformed', transformed)
        cv2.imshow('mask', mask)

    return flag
