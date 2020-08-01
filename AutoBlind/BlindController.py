"""Blind Controller module.

Manages a motor driver to allow calibration and control of a connected blind.
"""
from RPi.GPIO import (IN, PUD_UP, FALLING, setup, cleanup, setwarnings,
                      wait_for_edge, add_event_detect, event_detected)
from time import sleep
from AutoBlind.Controllers.MotorDriverInterface import MotorDriverInterface


class BlindController:
    """Class to calibrate and control blind position."""

    BUTTON_PIN = 7

    def __init__(self, motor_type=None, **kwargs):
        """Initialise blind control hardware."""
        if motor_type is None:
            raise Exception("Error: Must provide a motor_type.")
        if not issubclass(motor_type, MotorDriverInterface):
            raise Exception("Error: Not a valid motor_type.")
        self.motor = motor_type(**kwargs)
        setup(BlindController.BUTTON_PIN, IN, pull_up_down=PUD_UP)
        self.calibrate()

    def __del__(self):
        """Reset all GPIO pins."""
        setwarnings(False)
        cleanup()

    def calibrate(self):
        """Calibrate blind controller.

        Promts the user to press the button to begin calibration.
        The blinds are then lowered by rotating the motor in 5 degree
        increments, until the button is pressed again.
        The "fully-closed" position is then recorded and the blinds return
        to the open state.
        """
        # Promt user for to start calibration process.
        print("---Blind Calibration---")
        print("To start:")
        print("1) Ensure the blind is at its highest position.")
        print("2) Click the button.")

        # When the button is clicked, wait one second then begin calibration.
        wait_for_edge(BlindController.BUTTON_PIN, FALLING)
        sleep(1)

        # Display instructions to the user.
        print("The blind will now move in small increments.")
        print("Press the button when the blind is stationary" +
              "and in its fully closed position.")

        # Rotate the blinds until the button is clicked again.
        max_position_set = False
        self.blind_position = 0
        self.blind_position_max = None
        add_event_detect(BlindController.BUTTON_PIN, FALLING)
        while not max_position_set:
            # Rotate the motor in 5 degree increments at 50% speed.
            self.motor.rotate_by_angle(5, speed=50)
            self.blind_position += 5
            max_position_set = event_detected(BlindController.BUTTON_PIN)

        # Record the max position of the blind.
        self.blind_position_max = self.blind_position

        # Return the blinds to the open position.
        print("Calibration complete! Resetting blind position...")
        self.go_to_home()

    def _go_to_position(self, position):
        """Move the blinds to a given angular position.

        Args:
            position (float): The angle in degrees, clockwise from the
                0 position, to move the blinds to. This is clipped to the
                range [0, blind_position_max].
        """
        position = max(0, min(position, self.blind_position_max))
        self.motor.rotate_by_angle(position-self.blind_position)
        self.blind_position = position

    def go_to_home(self):
        """Move the blind to the "fully-open" position."""
        self._go_to_position(0)

    def go_to_max(self):
        """Move the blind to the "fully-closed" position."""
        self._go_to_position(self.blind_position_max)
