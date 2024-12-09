# [CV2] Motion Detection and Tracking in OpenCV: Frame Delta, MOG2, and Optical Flow Explained

In the previous blog posts, we explored basic image processing techniques in OpenCV.

- [CV2: What is an Image?, Lets adjust the Brightness and Contrast of an image](https://dev.to/jarvissan22/cv2-what-is-an-image-lets-adjust-the-brightness-and-contrast-of-an-image-35po)

- [ [CV2] HSV vs RGB: Understanding and Leveraging HSV for Image Processing](https://dev.to/jarvissan22/cv2-hsv-vs-rgb-understanding-and-leveraging-hsv-for-image-processing-49ac)

 While OpenCV is excellent for image manipulation, it also excels at processing video frames. By using cap = cv2.VideoCapture(video_file), we can analyze video streams frame by frame.

In this post, I will demonstrate motion detection and tracking techniques using a sample video of Shibuya Crossing, extracted from a public live stream. If you'd like to follow along with the same video, you can download it here: [[Video Download Link]](https://drive.google.com/file/d/1RPd4s_TicjVZ0hRyH24YBDtys_zNZ8Gk/view?usp=sharing).



## Setting Up and Displaying the Video
First, let's load the video and retrieve its metadata. These properties—frame size, frame count, and frames per second (FPS)—are critical for accurate processing and saving of video data.
```python
import cv2 

video_file = "./shibuy_test_20240705_063826.avi"
cap = cv2.VideoCapture(video_file)

# Test frame properties
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

print(f"Total Frames: {frame_count}, Width: {frame_width}, Height: {frame_height}, FPS: {fps}")
```

Its typical practice to set the video as a `cap` variable, there we can then get the meta data of the video with `cv2.CAP_PROP_*`. this is useful to get the frame size, total frame count and fps of the video. 

## Displaying the Video

To display the video, we use a while loop to read frames sequentially and show them with cv2.imshow. Always include a quit option for smooth termination.

```python
while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        cv2.imshow('Video Playback', frame)
        # Press "q" to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()

```

{% youtube https://www.youtube.com/watch?v=SrGE54LJEDY  %}

## Motion Detection

### Method 1 : Frame Delta 

Motion detection can be as simple as comparing consecutive frames. Using `cv2.absdiff(frame_1, frame_2)`, we compute the absolute difference between two frames.

```python
frame_1 = cap.read()[1]
cap.set(cv2.CAP_PROP_POS_FRAMES, 5)  # Skip to the 5th frame
frame_2 = cap.read()[1]

delta_frame = cv2.absdiff(frame_1, frame_2)
cv2.imshow('Delta Frame', delta_frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

![Image DeltaTest ](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/1enqfyyw8qxpl0fr7sfl.png)



To apply this method to the entire video:

```python
prev_frame = cap.read()[1]
while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        delta_frame = cv2.absdiff(prev_frame, frame)
        cv2.imshow('Delta Frame', delta_frame)
        prev_frame = frame
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
```


### Saving the video 

This above code displayed the video but it closed after the code was finished. To save this video we can use `cv2.VideoWriter()`. This is quite simple all we need to do is set the recorder variable then write each frame to it in the loop, then close it when done.

```python 
rec = cv2.VideoWriter('./output_delta.mp4',cv2.VideoWriter_fourcc(*'mp4v'),fps,(frame_width,frame_height),True)


#Video test 1
prev_frame=cap.read()[1]
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        delta_frame = cv2.absdiff(prev_frame,frame)
        cv2.imshow('Delta Frame', delta_frame)
        prev_frame=frame
        rec.write(delta_frame)
        # Press "q" to quit option
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break


cap.release()
cv2.destroyAllWindows()
rec.release()


```

{% youtube https://www.youtube.com/watch?v=WxYwRp9AcD0  %}


Note is good process to just use the fps,frame_width,frame_height, from the cap values to not lead to any issues with the size of the final video. 
Another option is change the output format. Its currently set to mp4 by the `cv2.VideoWriter_fourcc(*'mp4v')` but over formats like `mov` and `avi` can be used too.Finnaly is worth noting the `True` at the end, thats a default setting `is_color` i.e is a 3 channal image. If for example you have a 1 channal gray image this should be set to `False` for else it wont save properly and you get a "1kb" file of nothing at the end (Trust me this happens a lot). 

## Method 2: Background Subtraction
Another option is use cv2.createBackgroundSubtractorMOG2, we can separate moving objects from the static background. This a allows a indication of motion in a video and can separate the motion into objects and shadows.

```python
fgbg = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=16, detectShadows=True)

while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        fgmask = fgbg.apply(frame)
        cv2.imshow('Background Subtraction', fgmask)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
```

{% youtube https://www.youtube.com/watch?v=4RBn2IWbsOM %}

`cv2.createBackgroundSubtractorMOG2(history = 500,varThreshold = 16,	detectShadows = true)`


- history: The number of frames used to build the background model. The default value is 500.
- ・varThreshold: The threshold on the squared Mahalanobis distance between the pixel and the model to decide whether a pixel is well described by the background model. The default value is 16.
- ・detectShadows: A Boolean indicating whether to detect shadows. If set to True, the algorithm detects and marks shadows, which are typically shown in gray in the output mask. The default value is True.


Now using this method, the motion is much brighter with enter bodies being highlighted, we can even see some differences in people who are walking across the crossing. Like someone holding an umbrella. But there is a lot more noise in this version with some background artifacts from frame to frame. 

As Shadows are detected in fgbg object, a separate value is set to them than the object which is solid white. we can do this by a simple array boolean change to set all non 255 values to zero

```python
fgmask[fgmask != 255] = 0
```
There is also still a lot of noize in the version . One way to reduce this is use the value channel from a hsv image then apply a slight blur to cut out those artifacts 

```python
def process_frame(frame):
    frame= cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)[:,:,2]


    frame = cv2.GaussianBlur(frame, (5, 5), 1)
    return frame
```

This reduced the pixel artifact but does not solve them entirely but its good enough for now. 

{% youtube https://www.youtube.com/watch?v=MpCgIG1yrk0 %}

### Method 3   Motion Tracking with cv2.calcOpticalFlowPyrLK

In previous sections, we explored motion detection based on changes in pixel values between frames. However, detecting motion alone doesn't provide insights into how individual objects move. OpenCV's `cv2.calcOpticalFlowPyrLK` is a powerful tool for tracking specific points across video frames. This function uses the [Lucas-Kanade method](https://en.wikipedia.org/wiki/Lucas%E2%80%93Kanade_method) for optical flow estimation, making it highly effective for tracking dynamic objects in scenes such as the bustling traffic at Shibuya crossing.

```python
import cv2
import numpy as np

# Parameters for Shi-Tomasi corner detection
feature_params = dict(maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7)

# Parameters for Lucas-Kanade optical flow
lk_params = dict(winSize=(15, 15), maxLevel=2, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

# Video capture and output setup
cap = cv2.VideoCapture("shibuya_traffic.mp4")
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
rec = cv2.VideoWriter("output_tracking.mp4", fourcc, 30.0, (int(cap.get(3)), int(cap.get(4))))

# Read the first frame and initialize tracking points
ret, old_frame = cap.read()
old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
p0 = cv2.goodFeaturesToTrack(old_gray, mask=None, **feature_params)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the current frame to grayscale
    frame_gray = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY)

    # Calculate optical flow
    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

    # Select points successfully tracked
    good_new = p1[st == 1]
    good_old = p0[st == 1]

    # Draw the tracked points
    for i, (new, old) in enumerate(zip(good_new, good_old)):
        a, b = map(int, new.ravel())
        c, d = map(int, old.ravel())
        cv2.circle(frame, (a, b), 5, (0, 0, 255), -1)
        cv2.line(frame, (a, b), (c, d), (0, 255, 0), 2)

    # Update the previous frame and points
    old_gray = frame_gray.copy()
    p0 = good_new.reshape(-1, 1, 2)

    # Write and display the frame
    rec.write(frame)
    cv2.imshow("Tracked Motion", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
rec.release()
cv2.destroyAllWindows()

```

{% youtube https://www.youtube.com/watch?v=uIElCwj5hTM  %}

#### Setting Key Points for Tracking

Before tracking can begin, initial key points must be identified. This is done using the `cv2.goodFeaturesToTrack` function:

```python
p0 = cv2.goodFeaturesToTrack(old_gray, mask=None, **feature_params)
```

Parameters for feature_params:

- maxCorners: The maximum number of corners (keypoints) to detect. Increasing this value allows more points to be tracked but increases computational cost.
- qualityLevel: The minimum accepted quality of detected corners (0 to 1). Lower values detect weaker corners but may reduce tracking reliability.
- minDistance: Minimum Euclidean distance between detected points. Smaller values allow detection of closer points, increasing density.
- blockSize: Size of the neighborhood considered for corner detection. Smaller values detect finer details but are more sensitive to noise.

#### Lucas-Kanade Optical Flow Parameters
```python
lk_params = dict(winSize=(15, 15), maxLevel=2, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
```

- `winSize`: Defines the size of the search window for each pyramid level. Smaller windows increase precision but may miss large-scale motion.
- `maxLevel`: Sets the number of pyramid levels used for optical flow estimation. Higher levels improve tracking over larger displacements but require more computation.
- `criteria`: Determines the stopping condition for the iterative search algorithm:
   - EPS: Stops when the search achieves a small enough change.
   - COUNT: Stops after a fixed number of iterations.

In a complex scene like Shibuya crossing, adjusting parameters can enhance tracking results. Increasing the number of corners and reducing the search window size can improve motion precision:

```python
# Optimized parameters
feature_params = dict(maxCorners=500, qualityLevel=0.3, minDistance=7, blockSize=7)
lk_params = dict(winSize=(7, 7), maxLevel=5, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

```
{% youtube https://www.youtube.com/watch?v=bOrTlF64ZfE  %}

## Conclusion

In this article, we explored three powerful motion detection and tracking methods in OpenCV: Frame Delta, Background Subtraction, and Optical Flow using cv2.calcOpticalFlowPyrLK. Each method has its strengths and ideal use cases, from detecting general motion to tracking precise movements of specific objects.

The Frame Delta method provides a straightforward approach for comparing consecutive frames, while Background Subtraction offers a robust way to separate dynamic foreground objects from a static background. Finally, the Optical Flow method enables detailed tracking of motion by following individual points frame-by-frame.

By understanding and implementing these techniques, you can analyze and visualize motion effectively, even in complex scenes like the bustling Shibuya crossing.

## Homework
try combining the Frame Delta and Background Subtraction methods with the Optical Flow approach. Here’s your challenge:

> Objective:
> Enhance motion detection by blending the strengths of the Frame Delta and MOG2 methods to preprocess the frames before applying Optical Flow for tracking.

Message me or leave a comment with your code and output video link. I'd love to see how you combine these methods and the insights you gain from the process!
