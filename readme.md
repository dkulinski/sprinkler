## Sprinkler controller app

## Install
Create a new Raspbian image on an SD card

Once installed, run the following steps:

1. `sudo apt update`
1. `sudo apt install -y git nginx python3-venv`
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

