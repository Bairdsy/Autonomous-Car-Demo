#Electronics Setup & Install
## Raspberry Pi OS Install 
1. In a web browser, navigate to the URL http://downloads.raspberrypi.org/raspbian/images/raspbian-2018-11-15/ and download the zip file 2018-11-13-raspbian-stretch.zip
2. Download and install the latest version of Balena Etcher for your desktop operating system from https://www.balena.io/etcher/
3. Run Balena Etcher
  ![Etcher Screenshot](../Images/Balena.png?raw=true)
4. Click on “Select Image” and select the Raspbian Stretch zip file you downloaded.
5. Insert your microSD card into the slot on your computer (or a USB microSD reader if you don’t have a slot)
6. Click on “Flash!” 
  ![Flashing](../Images/Flashing.png?raw=true)
7. Wait for Balena Etcher to finish “Flashing” and “Verifying”.  Close any windows that pop up during this process giving warnings about drives that need formatting.
8. Remove the microSD card from your computer and insert it into the slot on the Raspberry Pi Zero W
  ![Raspberry Pi](../Images/RPi.png?raw=true)

## Explorer Phat
1.  The explorer Phat plugs into the top of the Raspberry Pi board as pictured
  ![Explorer](../Images/explorerphat.png?raw=true)
2. Connect each of the 2 motors to the Motor 1 + and - and Motor 2 + and - connectors on the board
3. Connect the IR distance sensor to the Ground, Analog and 5V connectors

## Video Streaming Service
### Update & Install Tools
```
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install build-essential imagemagick libv4l-dev libjpeg-dev cmake -y```
```

### Clone Repo in /tmp
```
cd /tmp
git clone https://github.com/jacksonliam/mjpg-streamer.git
cd mjpg-streamer/mjpg-streamer-experimental
```

### Make
```
make
sudo make install
```

### Run
```
/usr/local/bin/mjpg_streamer -i "input_uvc.so -r 1280x720 -d /dev/video0 -f 30" -o "output_http.so -p 8080 -w /usr/local/share/mjpg-streamer/www"
```

## Python Libraries
```
pip3 install scikit-learn
pip3 install scikit-image
sudo apt-get install python-opencv
sudo apt-get install python3-opencv
git clone http://github.com/pimoroni/explorer-hat
cd explorer-hat/library
sudo python setup.py install
```
