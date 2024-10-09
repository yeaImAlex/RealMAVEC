import depthai as dai
import cv2
import numpy as np

class Camera:
    def __init__(self, fps=40):
        # Initialize pipeline when the class is instantiated
        self.fps = fps
        self.pipeline = self.create_pipeline()
        self.device, self.videoQueue = self.start_camera()

    # Function to create and configure the pipeline
    def create_pipeline(self):
        pipeline = dai.Pipeline()

        # Create a Color Camera node
        camRgb = pipeline.createColorCamera()
        camRgb.setBoardSocket(dai.CameraBoardSocket.RGB)
        camRgb.setInterleaved(False)
        camRgb.setFps(self.fps)

        # Create an output stream
        xout = pipeline.createXLinkOut()
        xout.setStreamName("video")
        camRgb.video.link(xout.input)

        return pipeline

    # Function to start the camera device
    def start_camera(self):
        device = dai.Device(self.pipeline)
        videoQueue = device.getOutputQueue(name="video", maxSize=1, blocking=False)
        return device, videoQueue

    # Function to show the video feed
    def show_video(self):
        frame = self.videoQueue.get().getCvFrame()
        frame = cv2.resize(frame, [480, 320])
        # cv2.imshow('Camera', frame)
        if cv2.waitKey(1) == ord('q'):
            return None
        return frame

    # Function to calculate the brightness level of a frame
    def get_brightness_level(self, frame):
        # Convert the frame to grayscale if it is in color (BGR)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Calculate the average brightness level
        brightness_level = np.mean(gray_frame)
        return brightness_level

    # Function to clean up and release resources
    def stop_camera(self):
        cv2.destroyAllWindows()

if __name__ == "__main__":
    camera = Camera(fps=35)

    while True:
        frame = camera.show_video()
        if frame is None:
            break
        brightness = camera.get_brightness_level(frame)
        print(f"Average brightness level: {brightness}")

cv2.destroyAllWindows()

