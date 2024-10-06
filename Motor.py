import RPi.GPIO as GPIO
from time import sleep 
GPIO.setmode (GPIO.BCM)
GPIO.setwarnings(False)

class Motor():
    def __init__(self, L_PWM, R_PWM, L_EN, R_EN, L2_PWM, R2_PWM, L2_EN, R2_EN, SteeringPin):
        self.L_PWM = L_PWM
        self.R_PWM = R_PWM
        self.L_EN = L_EN
        self.R_EN = R_EN
        self.L2_PWM = L2_PWM
        self.R2_PWM = R2_PWM
        self.L2_EN = L2_EN
        self.R2_EN = R2_EN
        self.SteeringPin = SteeringPin
        GPIO.setup (self.L_PWM, GPIO.OUT)
        GPIO.setup (self.R_PWM, GPIO.OUT)
        GPIO.setup (self.L_EN, GPIO.OUT)
        GPIO.setup (self.R_EN, GPIO.OUT)
        GPIO.setup (self.L2_PWM, GPIO.OUT)
        GPIO.setup (self.R2_PWM, GPIO.OUT)
        GPIO.setup (self.L2_EN, GPIO.OUT)
        GPIO.setup (self.R2_EN, GPIO.OUT)
        GPIO.setup (self.SteeringPin, GPIO.OUT)

        self.left_motor_pwm = GPIO.PWM(self.L_PWM, 100)
        self.right_motor_pwm = GPIO.PWM(self.R_PWM, 100)
        self.left2_motor_pwm = GPIO.PWM(self.L2_PWM, 100)
        self.right2_motor_pwm = GPIO.PWM(self.R2_PWM, 100)

        self.left_motor_pwm.start(0)
        self.right_motor_pwm.start(0)
        self.left2_motor_pwm.start(0)
        self.right2_motor_pwm.start(0)

        self.steeringPin_pwm = GPIO.PWM(self.SteeringPin, 50)
        self.steeringPin_pwm.start(0)
    
    def stop(self):
        self.left_motor_pwm.ChangeDutyCycle(0)
        self.right_motor_pwm.ChangeDutyCycle(0)
        self.left2_motor_pwm.ChangeDutyCycle(0)
        self.right2_motor_pwm.ChangeDutyCycle(0)
        GPIO.output(self.L_EN, False)
        GPIO.output(self.R_EN, False)
        GPIO.output(self.L2_EN, False)
        GPIO.output(self.R2_EN, False)

    def set_speed(self, speed):
        GPIO.output(self.L_EN, True)
        GPIO.output(self.R_EN, True)
        GPIO.output(self.L2_EN, True)
        GPIO.output(self.R2_EN, True)

        self.left_motor_pwm.ChangeDutyCycle(speed)
        self.right_motor_pwm.ChangeDutyCycle(0)
        self.left2_motor_pwm.ChangeDutyCycle(speed)
        self.right2_motor_pwm.ChangeDutyCycle(0)

    def set_steering(self, angle):
        servo_angle = (angle+1)*90
        duty_cycle = 2.5 + (servo_angle/180) * 10
        self.steeringPin_pwm.ChangeDutyCycle(duty_cycle)

    def move(self, speed, angle):
        self.set_speed(speed)
        self.set_steering(angle)
    
    def cleanup(self):
        self.stop()
        self.left_motor_pwm.stop()
        self.right_motor_pwm.stop()
        self.left2_motor_pwm.stop()
        self.right2_motor_pwm.stop()
        self.steeringPin_pwm.stop()
        GPIO.cleanup()
    
def main():
    
        motor.move(50, 0)
        sleep(2)
        motor.stop()
        sleep(2)
        motor.move(40, 45)
        sleep(2)
        motor.stop()
        sleep(2)
        motor.move(40,155)
        sleep(2)

if __name__ == '__main__':
    motor = Motor(12,16,27,17,21,13,26,19,18)
    main()
