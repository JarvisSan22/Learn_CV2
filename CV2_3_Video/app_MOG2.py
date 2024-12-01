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

rec = cv2.VideoWriter('./output_mog2_no_shadow.mp4',cv2.VideoWriter_fourcc(*'mp4v'),fps,(frame_width,frame_height),True)

# Create the background subtractor object
fgbg = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=16, detectShadows=True)

def process_frame(frame):
    frame= cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)[:,:,2]

    frame = cv2.GaussianBlur(frame, (5, 5), 1)
    return frame
while(cap.isOpened()):
    ret, frame = cap.read()
    
    if ret == True:
        #frame = process_frame(frame)
        # Apply background subtraction
        fgmask = fgbg.apply(frame)

        #cut shadows 
        fgmask[fgmask != 255] =0
        cv2.imshow('frame', fgmask)

        rec.write(fgmask)
        # Press "q" to quit option 
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
    # Release resources
cap.release()
cv2.destroyAllWindows()
rec.release()