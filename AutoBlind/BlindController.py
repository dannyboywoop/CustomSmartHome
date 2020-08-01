"""Blind Controller module.

Manages a motor driver to allow control of a connected blind.
"""
from AutoBlind.Controllers.MotorDriverInterface import MotorDriverInterface


class BlindController:
    """Class to calibrate and control blind position."""

    def __init__(self, motor_type=None, max_angle=0, **kwargs):
        """Initialise blind control hardware."""
        if motor_type is None:
            raise Exception("Error: Must provide a motor_type.")
        if not issubclass(motor_type, MotorDriverInterface):
            raise Exception("Error: Not a valid motor_type.")
        self.motor = motor_type(**kwargs)
        self.blind_position_max = max_angle

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

    def _percentage_to_pos(self, percentage):
        return self.blind_position_max * percentage // 100

    def set_percentage(self, start_percentage, end_percentage):
        self.blind_position = self._percentage_to_pos(start_percentage)
        end_pos = self._percentage_to_pos(end_percentage)
        self._go_to_position(end_pos)
