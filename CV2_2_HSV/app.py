import cv2 
import numpy as np
import matplotlib.pyplot as plt

image = cv2.imread('./test_2.jpg')[:,:,::-1] #bgr to rgb
# Basic plot 
plt.figure(figsize=(10,10))
plt.subplot(1,2,1)
plt.imshow(image)
plt.title("RGB View")
hsv= cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

plt.subplot(1,2,2)
plt.imshow(hsv)
plt.title("HSV View")
plt.tight_layout()
#plt.show()

#Plot of the hist 
plt.figure(figsize=(10,6))
plt.subplot(1,2,1)
for i in range(3):
    plt.hist(image[:,:,i].ravel(),256,[0,256], color = 'r' if i == 0 else 'g' if i == 1 else 'b',histtype='step')
    plt.xlim([0,256])
plt.title("RGB View hist")

plt.subplot(1,2,2) 
for i in range(3):
    plt.hist(hsv[:,:,i].ravel(),256,[0,256], color = 'r' if i == 0 else 'g' if i == 1 else 'b',histtype='step')
    plt.xlim([0,256])
plt.title("HSV View hist")

plt.tight_layout()
#plt.show()
#cv2.namedWindow('HSV View')

plt.figure(figsize=(10,6))
plt.subplot(1,3,1)
plt.imshow(hsv[:,:,0])
plt.title("Hue")
plt.subplot(1,3,2)
plt.imshow(hsv[:,:,1])
plt.title("Saturation") 
plt.subplot(1,3,3)
plt.imshow(hsv[:,:,2])
plt.title("Value")
plt.tight_layout()
plt.show()


# Equalization of value 

equ = cv2.equalizeHist(hsv[:,:,2])
new_hsv = cv2.merge((hsv[:,:,0],hsv[:,:,1],equ))
new_image = cv2.cvtColor(new_hsv, cv2.COLOR_HSV2BGR)
plt.figure(figsize=(10,6))
plt.subplot(1,2,1)
plt.imshow(image)
plt.title("RGB View")
plt.subplot(1,2,2)
plt.imshow(new_image)
plt.title("View equalized View")
plt.tight_layout()
plt.show()


#  Saturation 
equ = cv2.equalizeHist(hsv[:,:,1])
new_hsv = cv2.merge((hsv[:,:,0],equ,hsv[:,:,2]))
new_image = cv2.cvtColor(new_hsv, cv2.COLOR_HSV2BGR)
plt.figure(figsize=(10,6))
plt.subplot(1,2,1)
plt.imshow(image)
plt.title("RGB View")
plt.subplot(1,2,2)
plt.imshow(new_image)
plt.title("Saturation equalized View")
plt.tight_layout()
plt.show()


# Color isolation 
# Define range for the color (e.g., red)
lower_red = np.array([140, 0, 0])
upper_red = np.array([180, 255, 255])

# Create a mask
mask = cv2.inRange(hsv, lower_red, upper_red)
filtered_image = cv2.bitwise_and(image, image, mask=mask)
plt.figure(figsize=(10,6))  
plt.subplot(1,2,1)
plt.imshow(image)
plt.title("RGB View")
plt.subplot(1,2,2)
plt.imshow(filtered_image)
plt.title("Filtered View")
plt.tight_layout()  
plt.show()  