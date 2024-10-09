import test as motorM
from time import sleep
from KeyboardM import Keyboard1  # Import your keyboard module

# Initialize the motor with GPIO pin numbers
motor = motorM.Motor(12, 16, 27, 17, 21, 13, 26, 19, 18)

# Initialize the keyboard
keyboard = Keyboard1()

try:
    while True:
        # Use your keyboard module to detect key presses
        if keyboard.getKey('w'):  # If 'w' is pressed
            motor.move(20, 0)
            sleep(1)
            motor.move(20, -0.29)
            sleep(4.5)
            motor.move(20, 0)
            sleep(1.5)
            motor.move(20, 0.44)
            sleep(4)
            motor.move(20, 0)
            sleep(1)

        elif keyboard.getKey('r'):  # If 'r' is pressed
            motor.move(20, 0)
            sleep(2)
            motor.move(20, -0.4)
            sleep(2)
            motor.move(20, 0)
            sleep(2)
            motor.move(20, 0.2)
            sleep(4)
            motor.move(20, 0)
            sleep(1)
            motor.move(20, 0.2)
            sleep(4)
            motor.move(20, -0.4)
            sleep(2)
            motor.move(20, 0)
            sleep(2)
            motor.stop()

        elif keyboard.getKey('q'):  # If 'q' is pressed
            motor.stop()
            break  # Exit the loop

finally:
    motor.stop()  # Ensure the motor stops when exiting
