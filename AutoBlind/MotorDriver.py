"""MotorDriver controller class.

This module acts acts as a hardware abstraction layer to allow a ULN2003
stepper motor to be controlled easily and accurately.
"""
from RPi.GPIO import HIGH, LOW, BOARD, OUT, setmode, setup, cleanup, output
from time import sleep
from enum import Enum


class MotorDriver:
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

    class Direction(Enum):
        """Enum type for rotation directions of motor."""

        CLOCKWISE = 1
        ANTICLOCKWISE = -1

        def opposite(self):
            """Return the opposite Direction enum."""
            opposite_value = self.value * -1
            return MotorDriver.Direction(opposite_value)

    def __init__(self):
        """Initialise GPIO pins."""
        setmode(BOARD)
        setup(MotorDriver.OUTPUT_PINS, OUT, initial=LOW)

    def __del__(self):
        """Reset all GPIO pins."""
        cleanup()

    def perform_step(self, direction=Direction.CLOCKWISE, delay=MIN_DELAY):
        """Perform 1 full step of the motor.

        Args:
            direction (MotorDriver.Direction): The direction of rotation of the
                motor in this step.
            delay (float): Time in seconds to wait between each update to
                motor controller pin states.
        """
        for state in MotorDriver.PIN_STATES[::direction.value]:
            output(MotorDriver.OUTPUT_PINS, state)
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
        delay = MotorDriver.MIN_DELAY * 100 / speed
        return max(delay, MotorDriver.MIN_DELAY)

    def rotate_by_angle(self, angle, direction=Direction.CLOCKWISE, speed=100):
        """Rotate the motor through a given angle.

        Args:
            angle (float): The angle, in degrees, through which the motor is
                to be rotated.
            direction (MotorDriver.Direction): The direction of rotation of the
                motor.
            speed (float): The desired speed as a percentage of the max speed.
                Must be greater than 0.
        """
        if angle < 0:
            angle = abs(angle)
            direction = direction.opposite()
        steps_to_perform = int(round(
                                MotorDriver.STEPS_PER_ROTATION * angle / 360))
        delay = self._delay_for_speed(speed)
        print(delay)
        for _ in range(steps_to_perform):
            self.perform_step(direction, delay)
