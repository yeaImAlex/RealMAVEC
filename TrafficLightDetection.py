import cv2
import numpy as np

# A function for trackbar (needed as OpenCV requires this function to be present)
def nothing(x):
    pass

class TrafficDetection:
    def __init__(self, camera_index=0):
        # Initialize webcam
        self.cap = cv2.VideoCapture(camera_index)
        if not self.cap.isOpened():
            print("Error: Could not open webcam.")

        # Initialize trackbars for color range adjustments
        self.initializeTrackbars()

    # Initialize trackbars for HSV values of red and green colors
    def initializeTrackbars(self):
        cv2.namedWindow("RedTrackbars")
        cv2.resizeWindow("RedTrackbars", 400, 300)
        cv2.namedWindow("GreenTrackbars")
        cv2.resizeWindow("GreenTrackbars", 400, 300)

        # Create trackbars for Red HSV values
        cv2.createTrackbar("Red Lower H", "RedTrackbars", 0, 179, nothing)
        cv2.createTrackbar("Red Lower S", "RedTrackbars", 120, 255, nothing)
        cv2.createTrackbar("Red Lower V", "RedTrackbars", 70, 255, nothing)
        cv2.createTrackbar("Red Upper H", "RedTrackbars", 10, 179, nothing)
        cv2.createTrackbar("Red Upper S", "RedTrackbars", 255, 255, nothing)
        cv2.createTrackbar("Red Upper V", "RedTrackbars", 255, 255, nothing)

        # Create trackbars for Green HSV values
        cv2.createTrackbar("Green Lower H", "GreenTrackbars", 36, 179, nothing)
        cv2.createTrackbar("Green Lower S", "GreenTrackbars", 100, 255, nothing)
        cv2.createTrackbar("Green Lower V", "GreenTrackbars", 100, 255, nothing)
        cv2.createTrackbar("Green Upper H", "GreenTrackbars", 86, 179, nothing)
        cv2.createTrackbar("Green Upper S", "GreenTrackbars", 255, 255, nothing)
        cv2.createTrackbar("Green Upper V", "GreenTrackbars", 255, 255, nothing)

    # Function to read the current values from trackbars
    def get_trackbar_values(self):
        # Get Red HSV range values
        red_lower_h = cv2.getTrackbarPos("Red Lower H", "RedTrackbars")
        red_lower_s = cv2.getTrackbarPos("Red Lower S", "RedTrackbars")
        red_lower_v = cv2.getTrackbarPos("Red Lower V", "RedTrackbars")
        red_upper_h = cv2.getTrackbarPos("Red Upper H", "RedTrackbars")
        red_upper_s = cv2.getTrackbarPos("Red Upper S", "RedTrackbars")
        red_upper_v = cv2.getTrackbarPos("Red Upper V", "RedTrackbars")

        # Get Green HSV range values
        green_lower_h = cv2.getTrackbarPos("Green Lower H", "GreenTrackbars")
        green_lower_s = cv2.getTrackbarPos("Green Lower S", "GreenTrackbars")
        green_lower_v = cv2.getTrackbarPos("Green Lower V", "GreenTrackbars")
        green_upper_h = cv2.getTrackbarPos("Green Upper H", "GreenTrackbars")
        green_upper_s = cv2.getTrackbarPos("Green Upper S", "GreenTrackbars")
        green_upper_v = cv2.getTrackbarPos("Green Upper V", "GreenTrackbars")

        # Return the HSV ranges
        red_lower = np.array([red_lower_h, red_lower_s, red_lower_v])
        red_upper = np.array([red_upper_h, red_upper_s, red_upper_v])
        green_lower = np.array([green_lower_h, green_lower_s, green_lower_v])
        green_upper = np.array([green_upper_h, green_upper_s, green_upper_v])

        return (red_lower, red_upper), (green_lower, green_upper)

    # Traffic light detection
    def detect_traffic_light(self):
        # Read frame from the webcam
        ret, frame = self.cap.read()

        if not ret:
            print("Error: Failed to capture frame from webcam.")
            return "No Frame"

        # Convert to HSV for color detection
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Get the current HSV ranges from the trackbars
        (red_lower, red_upper), (green_lower, green_upper) = self.get_trackbar_values()

        # Create masks for red and green based on the HSV ranges from trackbars
        mask_red = cv2.inRange(hsv_frame, red_lower, red_upper)
        mask_green = cv2.inRange(hsv_frame, green_lower, green_upper)

        # Show the frame and the masks for debugging
        cv2.imshow("Webcam Feed", frame)
        cv2.imshow("Red Mask", mask_red)
        cv2.imshow("Green Mask", mask_green)

        # Detect red or green color
        if np.any(mask_red):
            return "Red Light"
        elif np.any(mask_green):
            return "Green Light"
        else:
            return "No Traffic Light Detected"

    def cleanup(self):
        # Release the webcam and close windows
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    traffic_detector = TrafficDetection()

    while True:
        light_status = traffic_detector.detect_traffic_light()
        print(f"Traffic Light Status: {light_status}")

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Cleanup resources
    traffic_detector.cleanup()
