import cv2 
import numpy as np




#Test dispaly 
#cv2.imshow('Image', image)        
#cv2.waitKey(0)
#cv2.destroyAllWindows()



#Brightness adjust utils 
def adjust_brightness_contrast(image, contrast=1.0, brightness=0):
    """
    Adjust brightness and contrast using scaling and offset.
    Contrast is a float [0.0, 3.0].
    Brightness is an integer [-100, 100].
    """
    # Apply contrast and brightness adjustment
    new_image = cv2.convertScaleAbs(image, alpha=contrast, beta=brightness)
    return new_image
#Show with brighness and contrast slider 


def on_change(*args):
    alpha = cv2.getTrackbarPos('Contrast', 'Adjustments') / 10 #[0.0, 3.0]
    beta = cv2.getTrackbarPos('Brightness', 'Adjustments') - 50  #[-100, 100].
    updated_image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    cv2.imshow('Adjustments', updated_image)

# Display the image
image = cv2.imread('./test.png')
cv2.namedWindow('Adjustments')
cv2.imshow('Adjustments', image) 

# Add trackbars
cv2.createTrackbar('Contrast', 'Adjustments', 10, 30, on_change)  # Contrast 1.0 to 3.0
cv2.createTrackbar('Brightness', 'Adjustments', 50, 100, on_change)  # Brightness -50 to 50



cv2.imshow('Adjustments', image) 
cv2.waitKey(0)
#Turn off options 
while True:
    key = cv2.waitKey(1) & 0xFF
    # Check for exit (Ctrl + X)
    if key == ord('x'):  # Only check for 'x' key
        
        print("Exiting...")
        break
cv2.destroyAllWindows()