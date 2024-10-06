import laneDetection as ld
import Motor as motorM
import Camera as C
import BoomGateDetection as bgd  
from keyboardM import Keyboard1
import cv2

motor = motorM.Motor(12, 16, 27, 17, 21, 13, 26, 19, 18)
kM = Keyboard1()

if __name__ == '__main__':
    try:
        pipeline = C.create_pipeline(fps=30)
        device, videoQueue = C.start_camera(pipeline)

        intialTrackBarVals = [98, 133, 0, 240]
        ld.utils.initializeTrackbars(intialTrackBarVals)

        while True:
            frame = C.show_video(videoQueue)
            if frame is None:
                break

            # Detect the boom gate
            processed_frame, boom_gate_detected = bgd.detect_red_gate(frame)

            if boom_gate_detected:
                motor.stop()
            else:
                curve = ld.getLaneCurve(frame, display=1)

                if -0.05 <= curve <= 0.05:
                    motor.move(30, 90)  
                else:
                    delay = 0.58
                    curve *= delay
                    motor.move(30, curve)  


            cv2.imshow('Boom Gate Detection', processed_frame)


            if kM.getKey('q'):
                break

    finally:
        motor.cleanup()
        cv2.destroyAllWindows()
