import laneDetection as ld
import test as motorM
from CameraT import Camera
from KeyboardM import Keyboard1
import cv2
from intterupt import EventDetector
import BoomGateDetection as BGD

# Initialize the motor and keyboard
motor = motorM.Motor(12, 16, 27, 17, 21, 13, 26, 19, 18)  # Motor GPIO pin setup
kM = Keyboard1()  # Initialize the keyboard input handler
C = Camera()  # Initialize the camera
ED = EventDetector()

if __name__ == '__main__':
    print('Camera start')
    obj_d =0
    try:
        intialTrackBarVals = [84, 182, 0, 303]
        ld.utils.initializeTrackbars(intialTrackBarVals)

        while True:
            frame = C.show_video()  # Get the camera frame
            if frame is None:
                print('Frame not shown')
                break

            # Lane detection logic
            curve = ld.getLaneCurve(frame, display=1)
            print(curve)


            if -0.02 <= curve <= 0.02:
                motor.move(15, 0)
            else:
                delay = 1
                curve *= delay
                motor.move(15, curve)

            ED.add_event_detect(obj_d, 1, callback=BGD.detect_red_gate() , bouncetime=5)
            
            if kM.getKey('q'):
                break
            
        
    finally:
        motor.cleanup()
        cv2.destroyAllWindows()
