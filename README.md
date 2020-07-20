# CustomSmartHome
Repository for code written to create and host custom smart home devices.

## Setting up your Raspberry Pi

NOTE: The Raspberry Pi I used was the Raspberry Pi 3 Model B+ Revision 1.2. Your success may vary with other RP devices.

The following instructions provide a relevant summary of those found below:

- https://ubuntu.com/tutorials/how-to-install-ubuntu-on-your-raspberry-pi.
- https://www.itzgeek.com/how-tos/linux/ubuntu-how-tos/netplan-how-to-configure-static-ip-address-in-ubuntu-18-04-using-netplan.html.

### Prepare the SD Card

First download the official Raspberry Pi Imager, for your operating system, from https://downloads.raspberrypi.org/imager/.

Click **CHOOSE OS**, then select Ubuntu > Ubuntu 20.04 LTS.

Click **CHOOSE SD CARD**, then select the SD card that will be used for your Raspberry Pi.

### Connecting to WIFI (Optional)

You can choose to connect your Raspberry Pi to the internet via an Ethernet connection, in which case you can skip this section.

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
   
3. Put the SD card into the RP and perform the initial boot.

4. Once the initial boot is complete, restart the RP with `sudo reboot`.

5. You should now be connected to WIFI. This can be checked using `ip a`

NOTE: The config info above must be well formed YAML, this can easily be checked with tools such as http://www.yamllint.com/.

### Install necessary packages

Install Git with the command `sudo apt install git-all`.

Enter your git details with the following commands:

- `git config --global user.name "John Doe"`
- `git config --global user.email johndoe@example.com`

Install pip with the command `sudo apt install python3-pip`
