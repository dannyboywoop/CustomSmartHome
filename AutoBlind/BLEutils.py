from pexpect import EOF, TIMEOUT, run, spawn
from time import sleep


def scan_for_device(mac_address):
    print("Scanning for device")
    run("sudo hciconfig hci0 reset")
    scan = spawn("sudo hcitool lescan", timeout=5)
    try:
        scan.expect("{} (?:(?!\\(unknown\\)).)+$".format(mac_address))
    except EOF:
        print("Something went wrong: {}".format(scan.before))
        return False
    except TIMEOUT:
        print("Device not found!")
        scan.terminate()
        return False
    else:
        print("Device found!")
        scan.terminate()
        return True


def connect_to_device(mac_address):
    gatttool = spawn("sudo gatttool -b {} -I".format(mac_address), timeout=5)
    device_connected = False
    while not device_connected:
        try:
            print("Attempting to connect to {}".format(mac_address))
            sleep(1)
            gatttool.sendline("connect")
            gatttool.expect("Connection successful")
            device_connected = True
        except (EOF, TIMEOUT):
            print("Failed to connect: {}".format(gatttool.before))

    print("Connected!")
    return gatttool


def get_handle(device, characteristic):
    device.sendline("characteristics")
    device.expect("handle: (0x[0-9a-fA-F]{4}), "
                  + "char properties: (0x[0-9a-fA-F]{2}), "
                  + "char value handle: (0x[0-9a-fA-F]{4}), "
                  + "uuid: "+characteristic)
    _, _, handle = device.match.groups()
    return handle.decode()


def send_data_to_handle(device, handle, data):
    device.sendline("char-write-req {} {}".format(handle, data))
    device.timeout = 60
    device.expect("Characteristic value was written successfully")


def send_data_to_char(device, characteristic, data):
    handle = get_handle(device, characteristic)
    print(handle)
    send_data_to_handle(device, handle, data)


def disconnect_from_device(device):
    device.sendline("disconnect")
    device.sendline("quit")
    print("Disconnected!")
