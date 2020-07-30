from .MotorDriverInterface import MotorDriverInterface
from AutoBlind.Utilities.BLEutils import (scan_for_device,
                                          connect_to_device,
                                          send_data_to_char,
                                          disconnect_from_device)


class ArduinoController(MotorDriverInterface):
    def __init__(self, **kwargs):
        self.MAC_ADDRESS = kwargs["mac_address"]
        self.CHARACTERISTIC = kwargs["characteristic"]

    def _get_hex_representation(self, val, nbits=32):
        return"{0:0{1}x}".format((val + (1 << nbits)) % (1 << nbits), nbits//4)

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
        if direction == MotorDriverInterface.Direction.ANTICLOCKWISE:
            angle *= -1
        int_angle = round(angle)
        data_to_send = self._get_hex_representation(int_angle)

        device_found = scan_for_device(self.MAC_ADDRESS)
        if device_found:
            device = connect_to_device(self.MAC_ADDRESS)
            send_data_to_char(device, self.CHARACTERISTIC, data_to_send)
            disconnect_from_device(device)
