import cv2
import numpy as np
from Camera import Camera  # Import the Camera class from your camera module

# Function to detect the red boom gate
def detect_red_gate(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the range for detecting red color in HSV
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    # Create masks for red color detection
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = mask1 | mask2

    # Define the Region of Interest (ROI)
    height, width, _ = frame.shape
    roi = mask[height // 3: height, width // 3: 2 * width // 3]

    # Find contours within the ROI
    contours, _ = cv2.findContours(roi, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)

        # Only process contours with sufficient area
        if area > 200:
            # Approximate the contour shape
            epsilon = 0.05 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            # Check if the contour has at least 4 sides (a rectangle-like shape)
            if len(approx) >= 4:
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = w / float(h)

                # Check if the aspect ratio matches that of a boom gate (wide rectangle)
                if aspect_ratio > 3:
                    cv2.rectangle(frame, (x + width // 3, y + height // 3), 
                                  (x + width // 3 + w, y + height // 3 + h), (0, 255, 0), 2)
                    cv2.putText(frame, "Boom Gate Detected", (x + width // 3, y + height // 3 - 10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Show the mask (for debugging purposes)
    cv2.imshow('mask', roi)
    return frame, len(contours) > 0


if __name__ == "__main__":
    # Initialize the Oak-D camera using the Camera class
    C = Camera()  # Use your Camera class from camera_module

    while True:
        # Get the video feed from the Oak-D camera
        frame = C.show_video()
        if frame is None:
            break

        # Perform boom gate detection on the frame
        processed_frame, red_detected = detect_red_gate(frame)

        # Display the result
        cv2.imshow('Boom Gate Detection', processed_frame)

        # Exit the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Stop the Oak-D camera and clean up
    camera.stop_camera()
    cv2.destroyAllWindows()
