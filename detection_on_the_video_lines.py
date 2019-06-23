import cv2
import numpy as np

camera = cv2.VideoCapture("road_car_view.mp4")

while True:
    ret, orig_frame = camera.read()
    if not ret:
        camera = cv2.VideoCapture(0)
        continue

    frame = cv2.GaussianBlur(orig_frame, (5, 5), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # определить диапазон желтого цвета в HSV
    lower_yellow = np.array([18, 94, 140])
    up_yellow = np.array([48, 255, 255])
    lower_white = np.array ([0,160,0])
    up_white = np.array ([255,255,255])

    # Порог HSV изображение, чтобы получить только желтый цвет
    mask = cv2.inRange(hsv, lower_yellow, up_yellow)
    edges = cv2.Canny(mask, 75, 150)

    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, maxLineGap = 50)
    if lines is not None:
         for line in lines:
             x1, y1, x2, y2 = line [0]
             cv2.line(frame, (x1, y1), (x2, y2), (0,255,0),3)

    cv2.imshow("frame", frame)
    #cv2.imshow("Mask",mask)
    cv2.imshow("edges", edges)

    key = cv2.waitKey(25)
    if key == 27:
        break
camera.release()
cv2.destroyAllWindows()