import pexpect
import time
import os


MAC_ADDRESS = "24:62:AB:BA:0C:66"


def scan_for_device(mac_address):
    print("Scanning for device")
    os.system("sudo hciconfig hci0 reset")
    scan = pexpect.spawn("sudo hcitool lescan", timeout=5)
    try:
        scan.expect("{} (?:(?!\\(unknown\\)).)+$".format(mac_address))
    except pexpect.EOF:
        print("Something went wrong: {}".format(scan.before))
        return False
    except pexpect.TIMEOUT:
        print("Device not found!")
        scan.terminate()
        return False
    else:
        print("Device found!")
        scan.terminate()
        return True


def connect_to_device(mac_address):
    gatttool = pexpect.spawn("sudo gatttool -b {} -I".format(mac_address),
                             timeout=5)
    device_connected = False
    while not device_connected:
        try:
            time.sleep(1)
            print("Attempting to connect to {}".format(mac_address))
            gatttool.sendline("connect")
            gatttool.expect("Connection successful")
            device_connected = True
        except (pexpect.EOF, pexpect.TIMEOUT):
            print("Failed to connect: {}".format(gatttool.before))

    print("Connected!")
    return gatttool


def disconnect_from_device(device):
    device.sendline("disconnect")
    device.sendline("quit")
    print("Disconnected!")


if __name__ == "__main__":
    device_found = scan_for_device(MAC_ADDRESS)
    if device_found:
        device = connect_to_device(MAC_ADDRESS)
        disconnect_from_device(device)
    print("Done!")
