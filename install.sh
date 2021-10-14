#!/bin/bash
echo -e "INSTALLING...\n"

# ProCam Project Folder
echo "ProCam Project Folder..."
mkdir $HOME/ProCam
cp -R `pwd`/* $HOME/ProCam
rm $HOME/ProCam/install.sh
echo -e "Finished\n"

# ProCam Service Configuration
echo "ProCam Service Configuration..."
ServiceFolder="/lib/systemd/system"
ServiceContent="
[Unit]\n
Description=ProCam Service\n
After=multi-user.target\n\n

[Service]\n
User=pi\n
Group=sudo\n
Type=simple\n
ExecStart=/usr/bin/python3 /home/pi/ProCam/webapp.py\n
Restart=on-abort\n\n

[Install]\n
WantedBy=multi-user.target"
echo -e $ServiceContent > ProCam.service
sudo cp  `pwd`/ProCam.service $ServiceFolder/ProCam.service
rm `pwd`/ProCam.service
echo -e "Finished\n"

# Start Service ProCam
echo  "Start Service ProCam..."
sudo chmod 644 $ServiceFolder/ProCam.service
chmod +x /home/pi/ProCam/webapp.py
sudo systemctl daemon-reload
sudo systemctl enable ProCam.service
sudo systemctl start ProCam.service
echo -e "Finished\n"

echo -e "INSTALLED\n\n\n"
sudo systemctl status ProCam.service