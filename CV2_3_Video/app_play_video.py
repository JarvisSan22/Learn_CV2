import cv2 


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


while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        cv2.imshow('frame', frame)
        # Press "q" to quit option 
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()