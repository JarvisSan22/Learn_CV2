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

""" Frame test 
frame_1=cap.read()[1] # read first frame 
cap.get(5)
frame_2=cap.read()[1] #read the 5 frame with get function  

# Calculate frame delta 
delta_frame = cv2.absdiff(frame_1,frame_2)
cv2.imshow('Delta Frame', delta_frame)
cv2.waitKey(0)
#Turn off options 
while True:
    key = cv2.waitKey(1) & 0xFF
    # Check for exit (Ctrl + X)
    if key == ord('x'):  # Only check for 'x' key
        
        print("Exiting...")
        break
cv2.destroyAllWindows()

""" 

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
