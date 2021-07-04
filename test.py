import cv2
import numpy as np



img = cv2.imread('test.jpg')

r = []
g = []
b = []

for data in img:
    print(data.shape)
    break
