"""Motor Driver interface.

This module provides a simple interface for motor driver controller classes.
"""
from enum import Enum


class MotorDriverMeta(type):
    """A motor driver metaclass.

    It that will be used for motor driver class creation.
    """

    def __instancecheck__(cls, instance):
        """Check if 'instance' is an instance of the MotorDriverInterface.

        Returns:
            bool: True if 'instance' is an instance of MotorDriverInterface,
                False otherwise.
        """
        return cls.__subclasscheck__(type(instance))

    def __subclasscheck__(cls, subclass):
        """Check if 'subclass' is a subclass of the MotorDriverInterface.

        Returns:
            bool: True if 'subclass' is a subclass of MotorDriverInterface,
                False otherwise.
        """
        return (hasattr(subclass, 'rotate_by_angle')
                and callable(subclass.rotate_by_angle))


class MotorDriverInterface(metaclass=MotorDriverMeta):
    """Interface for motor driver controller classes."""

    class Direction(Enum):
        """Enum type for rotation directions of motor."""

        CLOCKWISE = 1
        ANTICLOCKWISE = -1

        def opposite(self):
            """Return the opposite Direction enum."""
            opposite_value = self.value * -1
            return MotorDriverInterface.Direction(opposite_value)

    def rotate_by_angle(self, angle, direction=Direction.CLOCKWISE, speed=100):
        """Rotate the motor through a given angle.

        Args:
            angle (float): The angle, in degrees, through which the motor is
                to be rotated.
            direction (MotorDriver.Direction): The direction of rotation of the
                motor. Default is clockwise.
            speed (float): The desired speed as a percentage of the max speed.
                Must be greater than 0. Default is 100.
        """
        pass
