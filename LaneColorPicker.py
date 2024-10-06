import cv2
import numpy as np
import Camera as C



pipeline = C.create_pipeline(fps=30)
device, videoQueue = C.start_camera(pipeline)

# Function that does nothing, just for trackbar
def empty(a):
    pass

# Create a window for HSV trackbars
cv2.namedWindow("HSV")
cv2.resizeWindow("HSV", 640, 240)

# Create trackbars for adjusting HUE, Saturation, and Value ranges
cv2.createTrackbar("HUE Min", "HSV", 0, 179, empty)
cv2.createTrackbar("HUE Max", "HSV", 179, 179, empty)
cv2.createTrackbar("SAT Min", "HSV", 0, 255, empty)
cv2.createTrackbar("SAT Max", "HSV", 255, 255, empty)
cv2.createTrackbar("VAL Min", "HSV", 0, 255, empty)
cv2.createTrackbar("VAL Max", "HSV", 255, 255, empty)

while True:
    frame = C.show_video(videoQueue)
    # Convert the image to HSV
    imgHsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Get current positions of the HSV trackbars
    h_min = cv2.getTrackbarPos("HUE Min", "HSV")
    h_max = cv2.getTrackbarPos("HUE Max", "HSV")
    s_min = cv2.getTrackbarPos("SAT Min", "HSV")
    s_max = cv2.getTrackbarPos("SAT Max", "HSV")
    v_min = cv2.getTrackbarPos("VAL Min", "HSV")
    v_max = cv2.getTrackbarPos("VAL Max", "HSV")

    # Print current HSV values (for debugging purposes)
    print(f"HUE Min: {h_min}, HUE Max: {h_max}, SAT Min: {s_min}, SAT Max: {s_max}, VALUE Min: {v_min}, VALUE Max: {v_max}")

    # Define the lower and upper ranges for the mask
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])

    # Create a mask that filters out colors outside the defined range
    mask = cv2.inRange(imgHsv, lower, upper)
    result = cv2.bitwise_and(frame, frame, mask=mask)

    # Stack the original image, mask, and result for side-by-side comparison
    mask_bgr = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    hStack = np.hstack([frame, mask_bgr, result])

    # Display the stacked images
    cv2.imshow('Horizontal Stacking', hStack)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources and close all windows
cv2.destroyAllWindows()
