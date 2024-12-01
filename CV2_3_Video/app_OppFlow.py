import cv2 
import numpy as np
video_file="./shibuy_test_20240705_063826.avi"
## Basic Video Display 
cap = cv2.VideoCapture(video_file)

# Test frame properties
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

print(f"Total Frames: {frame_count}")
print(f"Frame Dimensions: {frame_width}x{frame_height}")
print(f"FPS: {fps}")

rec = cv2.VideoWriter('./output_OpticalFlow_2.mp4',cv2.VideoWriter_fourcc(*'mp4v'),fps,(frame_width,frame_height),True)


# Flow prams need to be defined 
# Parameters for Shi-Tomasi corner detection
feature_params = dict(maxCorners=500, qualityLevel=0.3, minDistance=7, blockSize=7)
# Parameters for Lucas-Kanade optical flow
lk_params = dict(winSize=(7, 7), maxLevel=5, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))


# Read the first frame and convert to grayscale
ret, old_frame = cap.read()
old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
# Detect initial keypoints to track
p0 = cv2.goodFeaturesToTrack(old_gray, mask=None, **feature_params)

while True:
    ret,frame = cap.read()
    if ret == True:
        # Convert the current frame to grayscale
        frame_gray = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY)
        # Calculate optical flow
        p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

        # Select points that are successfully tracked
        good_new = p1[st == 1]
        good_old = p0[st == 1]

        # Draw the tracked points
        for i, (new, old) in enumerate(zip(good_new, good_old)):
            a, b = new.ravel()
            c, d = old.ravel()
            #Turn point to int for adding to unit8 image 
            a=int(a)
            b=int(b)
            c=int(c)
            d=int(d)
            cv2.circle(frame, (a, b), 5, (0, 0, 255), -1)
            cv2.circle(frame, (c, d), 5, (0, 255, 0), -1)
            cv2.line(frame, (a, b), (c, d), (0, 255, 0), 1)
        # Update the previous frame and keypoints
        old_gray = frame_gray.copy()
        p0 = good_new.reshape(-1, 1, 2)

        cv2.imshow('frame', frame)
        rec.write(frame)
        # Press "q" to quit option
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
    # Convert to grayscale

cap.release()
cv2.destroyAllWindows()
rec.release()
   