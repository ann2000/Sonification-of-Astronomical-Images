'''
import cv2

img1=cv2.imread('xray1.jpeg')
img2=cv2.imread('optical.jpg')
img3=cv2.imread('IR.jpg')


ret, thresh4 = cv2.threshold(img2, 90, 255, cv2.THRESH_TOZERO)
thresh4=cv2.cvtColor(thresh4,cv2.COLOR_BGR2GRAY)
im1= cv2.bitwise_not(img1, img1, mask=thresh4)

ret, thresh4 = cv2.threshold(img3, 150, 255, cv2.THRESH_TOZERO)
thresh4=cv2.cvtColor(thresh4,cv2.COLOR_BGR2GRAY)
im2= cv2.bitwise_not(im1, im1, mask=thresh4)



cv2.imshow('IMAGE',im2)
cv2.waitKey(0)


merged = cv2.merge([img1, img2, img3])
cv2.imshow("Merged", merged)
'''

import numpy as np
from PIL import Image

src1 = np.array(Image.open('xray1.jpeg'))
src2 = np.array(Image.open('optical.jpg').resize(src1.shape[1::-1], Image.BILINEAR))
src3 = np.array(Image.open('IR.jpg').resize(src1.shape[1::-1], Image.BILINEAR))
print(src1.dtype)
# uint8

dst = src1 * 0.5 + src2 * 0.5 + src3 * 0.2

print(dst.dtype)
# float64

Image.fromarray(dst.astype(np.uint8)).save('numpy_image_alpha_blend.jpg')