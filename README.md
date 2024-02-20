# Piloting a seven-segment board with gestures

## Installation quick guide on raspberry pi 4 (4 Go)

### Prerequisite

When creating the raspberry image with Raspberry Imager
* Choose Bookworm 64 bits to have cv2 and all the good things right
* If you want to test the display with alfazeta java 8 app, Choose OS / Other /  Pi OS Lite (32-bit) prefere Bullsey over  to have jdk 8 and test the board. And for this, user name should be `pi`. But you wont be able to launch the project which need more modern stuff for cv2 etc.
* In Settings make sure ssh is enabled, choose your regional settings, choose your wifi

### Kind remember

* To activate VNC, ssh to your raspi and launch `sudo raspi-config` > 3. Interface Option > 2 VNC, Yes, Enter


### Installation of the application on the Raspi

1. Activate Serial com: `sudo raspi-config` > 3. Interfaces > Serial > No to console on serial / yes to serial interface > save > reboot

1. Clone this repo or your own fork if you plan to adapt it (cf section _To code remotely_)

1. Check that picamera2 is installed with `sudo apt install -y python3-picamera2`

1. Create environment in the local repo directory, without forgetting to add `--system-site-packages` option to access to picamera2: `cd <repo>; python3 -m venv .venv --system-site-packages`

1. activate environment : `source .venv/bin/activate`

1. install requirements : `pip install -r requirements.txt`

1. launch calling `bash start.sh`! Stop with ctrl-C.

1. Don't forget to call `bash stop.sh` if you want to set dark mode before moving the physical display

### Starting it when booting rapsi (and set dark mode when shutting down)

In repository folder 
1. Adapt `sevendots.service` and `start.sh` to your path

1. `sudo cp ./sevendots.service /etc/systemd/system/`

1. `sudo systemctl enable sevendots.service`

### To code remotely and push things back to github

1. If you have not yet configured ssh connection with public keys, add the public key to accept connections from vscode from your main computer. For this, execute on your main computer:
`ssh-copy-id -i ~/.ssh/<keyfile>.pub name@server.local`
1. Use vscode live share
1. add (manualy) the private key to push on github, with chmod 600

1. set git name and email

```
git config --global user.name "Your Name"
git config --global user.email "email@domain.tld"
```


## Testing serial
```python
import serial
ser = serial.Serial(port='/dev/serial0', baudrate=57600)
# should answer True
ser.isOpen()
# should print Serial<id=0x........, open=True>(port='/dev/serial0', baudrate=57600, bytesize=8, parity='N', stopbits=1, timeout=None, xonxoff=False, rtscts=False, dsrdtr=False)
print(ser)
# should answer 32 and print "-" everywhere
ser.write(bytes([0x80, 0x83, 0x00]+[0b1]*28+[0x8F]))
# print all segments once on first line than "0123456789ABCDEF -?':" on the other lines
ser.write(b'\x80\x83\x00\x01\x02\x04\x08\x10\x20\x40\x7e\x30\x6d\x79\x33\x5b\x5f\x70\x7f\x7b\x77\x1f\x4e\x3d\x4f\x47\x00\x01\x64\x02\x09\x8F')
```

# Troubleshooting
If when instantiating ser, you have `FileNotFoundError: [Errno 2] No such file or directory: '/dev/serial0'`, be sure to have activated Serial in raspi-config (No to console on serial / yes to serial interface, cf 1.)

You can also try to access to the serial port with stty, for example:
```bash
stty -F /dev/serial0 speed 57600 cs8 -cstopb -parenb -echo
echo -en '\x80\x83\x00\x01\x02\x04\x08\x10\x20\x40\x7e\x30\x6d\x79\x33\x5b\x5f\x70\x7f\x7b\x77\x1f\x4e\x3d\x4f\x47\x00\x01\x64\x02\x09\x8F' > /dev/serial0
```