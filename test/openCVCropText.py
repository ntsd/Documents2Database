import cv2
import numpy as np

# reading the input image in grayscale image
image = cv2.imread('3.png',cv2.IMREAD_GRAYSCALE)
# image /= 255
if image is None:
    print('Can not find/read the image data')
# Defining ver and hor kernel
N = 5
kernel = np.zeros((N,N), dtype=np.uint8)
kernel[2,:] = 1
dilated_image = cv2.dilate(image, kernel, iterations=2)

kernel = np.zeros((N,N), dtype=np.uint8)
kernel[:,2] = 1
dilated_image = cv2.dilate(dilated_image, kernel, iterations=2)
image *= 255

# finding contours in the dilated image
contours,a = cv2.findContours(dilated_image,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# finding bounding rectangle using contours data points
rect = cv2.boundingRect(contours[0])
pt1 = (rect[0],rect[1])
pt2 = (rect[0]+rect[2],rect[1]+rect[3])
cv2.rectangle(image,pt1,pt2,(100,100,100),thickness=2)

# extracting the rectangle
text = image[rect[1]:rect[1]+rect[3],rect[0]:rect[0]+rect[2]]

cv2.subplot(1,2,1), cv2.imshow(image,'gray')
cv2.subplot(1,2,2), cv2.imshow(text,'gray')

cv2.show()