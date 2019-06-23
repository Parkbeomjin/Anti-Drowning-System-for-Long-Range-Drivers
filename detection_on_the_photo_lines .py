import cv2
import numpy as np

img = cv2.imread ("lines.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2. Canny(gray, 75, 150) ## craya
# cv2.HoughLines()
# cv2.HoughLinesP()

lines = cv2.HoughLinesP(edges, 1, np.pi/180, 30, maxLineGap=250) #maxLineGap обводка всего квадрата  250 это на сколько его зарисовать
#print(lines) // ricovka liniy

for line in lines:
    x1, y1, x2, y2 = line[0] # извелакаем значения  x1, y1, x2, y2 и это будет равняться 0
    cv2.line (img, (x1,y1), (x2,y2), (0,255, 0),3) # рисовка линий на оригальной фото
cv2.imshow("Edges", edges)
cv2.imshow("Image",img)
cv2.waitKey(0)
cv2.destroyAllWindows()
