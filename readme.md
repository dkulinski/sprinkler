## Sprinkler controller app

## Install
Create a new Raspbian image on an SD card

1. After the image installation is complete open the boot partition
1. On the boot partition add an empty file called ssh
1. Open the config.txt and add this to the bottom of the file:
  `enable_uart=1`
1. Open the cmdline.txt file and remove the following string, make sure the rest of the line doesn't change:
  `console=serial0,115200`

Once the above is completed place the SD card into the Raspberry Pi and power it on

Once booted, run the following steps:

1. `sudo systemctl enable sshd`
1. `sudo systemctl start sshd`
1. `sudo usermod -a -G tty pi`
1. `sudo shutdown -r now`
1. Wait for the pi to reboot and log in again
1. `sudo apt update`
1. `sudo apt install -y git nginx python3-venv gunicorn`
1. `mkdir ~/dev`
1. `cd ~/dev`
1. `git clone https://github.com/dkulinski/sprinkler.git`
1. `cd sprinkler`
1. `python3 -mvenv venv`
1. `. venv/bin/activate`
1. `pip install -r requirements.txt`
1. `sudo cp sprinkler /etc/nginx/sites-available/`
1. `sudo ln -s /etc/nginx/sites-available/sprinkler /etc/nginx/sites-enabled/sprinkler`
1. `sudo rm /etc/nginx/sites-enabled/default`
1. `sudo cp sprinkler.service /etc/systemd/system/`
1. `sudo systemctl daemon-reload`
1. `sudo systemctl enable sprinkler`
1. `sudo systemctl start sprinkler`
1. `sudo systemctl enable nginx`
1. `sudo systemctl start nginx`

At this point you should be able to browse to:
http://raspberrypi.local/

If that doesn't work then you should be able to reach it via IP address of the pi.
