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

1. Create environment in the local repo directory without forgetting to add --system-site-packages option to access to picamera2: `cd <repo>; python3 -m venv .venv --system-site-packages`

1. activate environment : `source .venv/bin/activate`

1. install requirements : `pip install -r requirements.txt`

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

