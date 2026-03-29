import cv2 as cv
import cv2.aruco as aruco

aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
img = aruco.generateImageMarker(aruco_dict, 23, 400)
cv.imwrite("marker23.png", img)
