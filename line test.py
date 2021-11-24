import numpy as np
import cv2

testImg = np.zeros((500,500), np.uint8)
testImg = cv2.line(testImg, (0,0), (100,100), (255,255,255), 5)
cv2.imshow("testImg", testImg)
cv2.waitKey(1)
