"""ULN2003 Motor Driver controller class.

This module acts as a hardware abstraction layer to allow a ULN2003
stepper motor to be controlled easily and accurately.
"""
from RPi.GPIO import HIGH, LOW, BOARD, OUT, setmode, setup, cleanup, output
from time import sleep
from .MotorDriverInterface import MotorDriverInterface


class ULN2003(MotorDriverInterface):
    """Class used to control a ULN2003 stepper motor/driver."""

    OUTPUT_PINS = [12, 11, 13, 15]
    PIN_STATES = [
        (HIGH, LOW, LOW, LOW),
        (LOW, HIGH, LOW, LOW),
        (LOW, LOW, HIGH, LOW),
        (LOW, LOW, LOW, HIGH)
    ]
    STEPS_PER_ROTATION = 509.4716
    MIN_DELAY = 0.002

    def __init__(self):
        """Initialise GPIO pins."""
        setmode(BOARD)
        setup(ULN2003.OUTPUT_PINS, OUT, initial=LOW)

    def __del__(self):
        """Reset all GPIO pins."""
        cleanup()

    def _perform_step(self,
                      direction=MotorDriverInterface.Direction.CLOCKWISE,
                      delay=MIN_DELAY):
        """Perform 1 full step of the motor.

        Args:
            direction (MotorDriver.Direction): The direction of rotation of the
                motor in this step.
            delay (float): Time in seconds to wait between each update to
                motor controller pin states.
        """
        for state in ULN2003.PIN_STATES[::direction.value]:
            output(ULN2003.OUTPUT_PINS, state)
            sleep(delay)

    def _delay_for_speed(self, speed):
        """Return the delay between signal updates required for a given speed.

        Args:
            speed (float): The desired speed as a percentage of the max speed.
                Must be greater than 0.

        Returns:
            float: Delay between signal updates required for the given speed,
                or the Min_Delay, whichever is larger.
        """
        if speed <= 0:
            raise ArithmeticError
        delay = ULN2003.MIN_DELAY * 100 / speed
        return max(delay, ULN2003.MIN_DELAY)

    def rotate_by_angle(self,
                        angle,
                        direction=MotorDriverInterface.Direction.CLOCKWISE,
                        speed=100):
        """Rotate the motor through a given angle.

        Args:
            angle (float): The angle, in degrees, through which the motor is
                to be rotated.
            direction (MotorDriver.Direction): The direction of rotation of the
                motor. Default is clockwise.
            speed (float): The desired speed as a percentage of the max speed.
                Must be greater than 0. Default is 100.
        """
        if angle < 0:
            angle = abs(angle)
            direction = direction.opposite()
        steps_to_perform = int(round(
                                ULN2003.STEPS_PER_ROTATION * angle / 360))
        delay = self._delay_for_speed(speed)
        for _ in range(steps_to_perform):
            self._perform_step(direction, delay)

        # reset pin states.
        output(ULN2003.OUTPUT_PINS, LOW)
        sleep(ULN2003.MIN_DELAY)
