import time
import cv2  # Import OpenCV for cv2.waitKey()

class EventDetector:
    def __init__(self):
        self._last_time = 0  # Private variable to store last trigger time

    def add_event_detect(self, obj_d, stnum, callback, bouncetime=5):
        """
        Checks if the detected object matches the station number,
        and triggers the callback function if conditions are met.
        The detection parameters are passed directly into this function.
        """
        # Get current time in seconds
        current_time = time.time()

        # Check if obj_d matches the station number
        if obj_d == stnum:
            # If enough time has passed since the last trigger (debouncing)
            if current_time - self._last_time >= bouncetime:
                callback()  # Trigger the callback function
                self._last_time = current_time  # Update the last triggered time
                #print(f"last_time updated to: {self._last_time}")

# Example callback function
def station_matched():
    print("Station matched! Callback function triggered.")

# Main entry point
if __name__ == "__main__":
    # Initialize the event detector
    event_detector = EventDetector()

    # Prompt user to press 'q' to exit
    print("Press 'q' to exit the program")

    # Main loop
    while True:
        # Example of how to dynamically pass parameters to add_event_detect
        obj_d = 5  # Example detected object number
        stnum = 5  # Example station number to check against
        bouncetime = 2  # Debounce time in seconds

        # Call the add_event_detect method with dynamic parameters
        event_detector.add_event_detect(obj_d, stnum, callback=station_matched, bouncetime=bouncetime)

        # Check if 'q' key is pressed to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Exiting...")
            break

        # Sleep briefly to avoid tight looping
        time.sleep(0.1)
