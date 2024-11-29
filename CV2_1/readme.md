
# CV2: What is an Image?, Lets adjust the Brightness and Contrast of an image
Blog post on [DEV.to](https://dev.to/jarvissan22/cv2-what-is-an-image-lets-adjust-the-brightness-and-contrast-of-an-image-35po)
日本語版  [qiita.com](https://qiita.com/JarvisSan22/items/c86b28071dbc0343287a)

In the context of CV2 in Python, when you read an image, it is stored as a 2D or 3D array of Y and X coordinates with uint8 values indicating the color and brightness of the image. The term `uint8` refers to an 8-bit unsigned integer data type that ranges from 0 to 255. This, combined with 3 channels for Red, Green, and Blue (RGB), forms a color image.

## Why This Structure Matters
If you start altering parts of the image like a normal array (e.g., dividing it by 3), you may lose this format. For instance, pixel values may fall outside the range of 0 to 255, causing the image to become unusable. Understanding this structure is crucial for manipulating images correctly.

## Viewing an Image in CV2

In the CV2 Python library, you can easily view an image using the following code snippet:

```python
#pip install opencv-python # if not already installed 
import cv2

# Load an image
image = cv2.imread('./test.png')

# Display the image in a window
cv2.imshow('Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

![Image first test image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/fk6rs7mt6v4rq6katzlk.png)


The code above will open a popup window displaying the image on your computer. Feel free to add a url to your own image to test.  You can then zoom in to observe the pixel-level RGB values of the image. This basic functionality is a great starting point for exploring image processing.

![Image test image for zoom](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/sxdz75xe4890nws78to5.png)



## Brightness and Contrast
### What Are Brightness and Contrast?

- Brightness refers to the overall lightness or darkness of an image, determined by the pixel intensity.
- Contrast refers to the difference in intensity between pixels compared to a reference value (e.g., the mean pixel intensity). It essentially measures how "sharp" or "distinct" the variations in the image are.

Mathematically, brightness and contrast can be adjusted using the formula:

`new_image=contrast×image+brightness`


### Applying Brightness and Contrast in CV2

The `cv2.convertScaleAbs()` function in OpenCV automates this process. It applies the formula above while ensuring that pixel values remain within the range of 0 to 255.

Here’s how it works:

- alpha (contrast): A scaling factor, typically between 0.0 and 3.0.
- beta (brightness): An offset value, typically between -100 and 100


Example Usage: 
`new_image = cv2.convertScaleAbs(image, alpha=contrast, beta=brightness)
`
This allows us to easily modify brightness and contrast without manually clipping pixel values.
```
image = cv2.imread('./test.png')
cv2.namedWindow('Adjustments')
contrast=0.8
brightness=89
image=cv2.convertScaleAbs(image, alpha=contrast, beta=brightness)
cv2.imshow('Adjustments', image) 
cv2.waitKey(0)
cv2.destroyAllWindows()

```
![Image test image for brightens and contract change](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/j2ifff8gehfs1gug27e1.png)

## Creating Interactive Adjustments with Callbacks 

While a one-time adjustment is useful, most of the time, we want to tweak brightness and contrast interactively. OpenCV allows us to achieve this using trackbar.

Trackbars can be created with cv2.createTrackbar(), which lets us adjust values dynamically. The general syntax is:
`cv2.createTrackbar(trackbarname, winname, value, count, onChange_function)`

- trackbarname: The name of the trackbar.
- winname: The name of the OpenCV window where the trackbar will be displayed.
- value: The initial position of the trackbar.
- count: The maximum value of the trackbar.
- onChange_function: A callback function that is called whenever the trackbar value changes.

These trackbar then can be called in the onChange_function with;
`cv2.getTrackbarPos(trackbarname, winname)`
・trackbarname: The name of the trackbar
・ winname: The name of the OpenCV window where the trackbar will be displayed.

To adjust both brightness and contrast, we will need two trackbars.


```

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
# Exit on pressing 'x'
while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord('x'):  # Press 'x' to exit
        print("Exiting...")
        break
cv2.destroyAllWindows()
```

![Image test finnl app image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/cmaqzgjatoh9fv0fzw4e.png)


Adjusting the contrast and brightness sliders triggers the `on_change` function, which reads the values from the trackbars using `cv2.getTrackbarPos()`. These values are then applied to the image using the `cv2.convertScaleAbs` function, and the updated image is displayed in real-time.

To make the app more user-friendly, I added a simple snippet at the end to allow users to exit by pressing the `x` key. This addresses a common issue with OpenCV, where closing the window doesn’t always stop the code from running. By implementing this, the app ensures a clean exit without lingering processes.

