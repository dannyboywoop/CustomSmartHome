

# CustomSmartHome

Repository for code written to create and host custom smart home devices.

## Project structure

Below are some simple explanations as to the purpose of sub-directories within this repo.

```
CustomSmartHome
├── lambda (code hosted as an aws_lambda function)
├── Smart_Devices(code ran on, or used to control smart devices)
│   └── SmartBlind (code to create a smart blind)
│       ├── AutoBlind (Python code ran on the RPi, can control a directly-wired blind or a Bluetooth Arduino blind)
│       └── BluetoothBlind (Code ran on a Arduino Nano 33 IoT to control a blind)
└── TannoHolmes.com (the web server for my personal website, also manages local smart home devices)
```

The full structure of the project, along with its interactions with Amazon Alexa are shown in the diagram below.

[DIAGRAM NOT YET CREATED]

## Setting up your Raspberry Pi

NOTE: The Raspberry Pi I used was the Raspberry Pi 3 Model B+ Revision 1.2. Your success may vary with other RPi devices.

The following instructions provide a relevant summary of those found below:

- https://ubuntu.com/tutorials/how-to-install-ubuntu-on-your-raspberry-pi.
- https://www.itzgeek.com/how-tos/linux/ubuntu-how-tos/netplan-how-to-configure-static-ip-address-in-ubuntu-18-04-using-netplan.html.

### Notes on the OS

The following sections describe two different setup processes. The first, using Ubuntu, is a headless setup (without monitor and keyboard) and the second is a simpler setup, using Raspberry Pi OS.

Ubuntu was used for a headless setup, as it seems to have far fewer issues in connected to WIFI.

Raspberry Pi OS Lite may be used headless, but your mileage may vary if you choose to use WIFI. Following the documentation online, I was unable to get it to work correctly on my Pi.

I would suggest that you use Raspberry Pi OS rather than Ubuntu. This is because I had a far easier time getting the RPi to communicate through BLE when using RPi OS, the Bluez stack that comes with Ubuntu would not work out-of-the-box and I needed to recompile it manually.

### Prepare the SD Card

First download the official Raspberry Pi Imager, for your operating system, from https://downloads.raspberrypi.org/imager/.

Click **CHOOSE OS**, then select "Ubuntu > Ubuntu 20.04 LTS" for headless setup, or "Raspberry Pi OS (Other) > Raspberry Pi OS LITE".

Click **CHOOSE SD CARD**, then select the SD card that will be used for your Raspberry Pi.

### Connecting to WIFI (Optional)

You can choose to connect your Raspberry Pi to the internet via an Ethernet connection, in which case you can skip this section.

#### Ubuntu (headless)

To use WIFI, follow these steps **BEFORE** you boot your Raspberry Pi for the first time.

1. Insert the SD card back into your computer.

2. Edit the `network-config` file to add your WIFI credentials, e.g.

   ```yaml
   version: 2
   renderer: networkd # or NetworkManager if you intend to install that
   ethernets:
     eth0:
       dhcp4: true
       optional: true
   wifis:
     wlan0:
       dhcp4: false
       optional: true
       access-points:
         my_wifi_ssid:
           password: "MY_PASSWORD"
       addresses: [192.168.1.200/24] # desired static IP
       gateway4: 192.168.1.1 # the local ip of your router
       nameservers:
         addresses: [192.168.1.1,8.8.8.8]
   ```
   
3. Put the SD card into the RPi and perform the initial boot.

4. Once the initial boot is complete, restart the RPi with `sudo reboot` (or by disconnecting and reconnecting power).

5. You should now be connected to WIFI. This can be checked using `ip a`, or by trying to SSH into the device.

NOTE: The config info above must be well formed YAML, this can easily be checked with tools such as http://www.yamllint.com/.


#### Raspberry Pi OS

Begin by putting the SD card into the Raspberry Pi and performing the initial boot.

Next, launch the raspi-config command-line tool with `sudo raspi-config`.

Simple ensure that the Localisation Options are set correctly, then use the wizard to setup Network Options.

To allow custom smart home devices to find the RPi, you must set its "Hostname" to `TannoHub` from the Network Options menu.

### Install necessary packages

Before installing any new packages, it is a good idea to update all current packages with the command `sudo apt update` followed by `sudo apt upgrade`.

Install Git with the command `sudo apt install git-all`.

Enter your git details with the following commands:

- `git config --global user.name "John Doe"`
- `git config --global user.email johndoe@example.com`

Install pip with the command `sudo apt install python3-pip`.

Install pexpect with `sudo pip3 install pexpect`.

Install RPi.GPIO with `sudo pip3 install RPi.GPIO`.