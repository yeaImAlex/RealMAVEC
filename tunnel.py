import RPi.GPIO as GPIO
from time import sleep, time
from test import Motor
from KeyboardM import Keyboard1
from CameraT import Camera

leftTrigPin = 23
leftEchoPin = 24
motorR = 0

Kp = 20
Ki = 0
Kd = 0.005

integral = 0
lastError = 0
dt = 0.1

target_distance = 10
u = 20

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(leftTrigPin, GPIO.OUT)
GPIO.setup(leftEchoPin, GPIO.IN)
GPIO.output(leftTrigPin, False)


def get_distance(trigPin, echoPin):
    GPIO.output(trigPin, GPIO.LOW)
    sleep(0.000002)
    GPIO.output(trigPin, GPIO.HIGH)
    sleep(0.000015)
    GPIO.output(trigPin, GPIO.LOW)

    start_time = time()
    stop_time = time()

    while GPIO.input(echoPin) == 0:
        start_time = time()
    while GPIO.input(echoPin) == 1:
        stop_time = time()

    time_elapsed = stop_time - start_time
    distance = (time_elapsed * 34300) / 2
    return distance


def pid_control(distance_difference):
    global integral, lastError, dt

    P = Kp * distance_difference
    integral += distance_difference * dt
    I = Ki * integral
    derivative = (distance_difference - lastError) / dt
    D = Kd * derivative

    output = P + I + D
    lastError = distance_difference

    return output


def adjust_motor_speed(motor, pid_output):
    pid_output = max(min(pid_output, 100), -100)

    mapped_output = pid_output / 100

    motor.move(u, mapped_output)


motor = Motor(12, 16, 27, 17, 21, 13, 26, 19, 18)
keyboard = Keyboard1()
camera = Camera()

if __name__ == '__main__':
    try:
        while True:
            frame = camera.show_video()  # Capture the video frame
            if frame is None:
                break  # Exit if frame is None

            # Get brightness level using the captured frame
            brightness = camera.get_brightness_level(frame)
            print(f"Average brightness level: {brightness}")

            if brightness < 35:
                left_distance = get_distance(leftTrigPin, leftEchoPin)

                # Clamp distance values
                if left_distance < 7.5:
                    left_distance = 7.5
                elif 11 < left_distance <= 90:
                    left_distance = 11
                elif left_distance > 100:
                    left_distance = 6.5
                elif 10 <= left_distance <= 10.5:
                    left_distance = 10

                distance_difference = target_distance - left_distance

                print(
                    f"Distance Difference: {distance_difference}")



                pid_output = pid_control(distance_difference)
                if not (15 <= left_distance <= 90):
                    adjust_motor_speed(motor, pid_output)

                sleep(dt)
            else:
                motor.stop()


    except KeyboardInterrupt:
       motor.cleanup()
    

