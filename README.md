# PiWifiCam
A simple livestream application designed for the Raspberry Pi.  
This is an educational application with the focus on keeping the code simple and understandable.  
The application is basically the video streaming part of [STS-PiLot](https://github.com/mark-orion/STS-PiLot) without the robotics remote control components.

## Features
* Responsive (portrait and landscape mode) interface for use on desktops, laptops, tablets and phones.
* Tested on Raspberry Pi 3 and Raspberry Pi Zero W.
* Frontend requires only HTML, Javascript and CSS - no proprietary plugins needed.
* Data and video connection is automatically reestablished after connection loss.
* Threaded (fast, low latency) capture interface.
* Alternative non-threaded (slower, low CPU usage) video capture for lower spec. computers like the Raspberry Pi Zero.
* Use camera_cv.py for standard webcams.

## Requirements
* Raspberry Pi
* Computer / Tablet / Phone with web browser that supports MJPEG
* Tested with the following browsers:  
Linux and Windows: Firefox, Chrome and Opera.  
Android (5.1 on Fairphone 2): Lightning, IceCat Mobile, Chromium.  
CAVEAT: MS Edge and Internet Explorer do not support MJPEG natively.  
Apple Safari and iOS browsers have limited or broken MJPEG support.  
Please use one of the tested browsers instead.

## Install Dependencies (Picamera, Flask, Gevent, Simplejson)
sudo apt-get install python-picamera python-flask python-gevent python-simplejson  
For generic webcam support (camera_cv.py) add: sudo apt-get install python-opencv python-pil

## Install PiWifiCam
Clone or download the application into a directory of your choice:
git clone https://github.com/mark-orion/PiWifiCam.git  
You can update the already cloned application from within its directory:  
git remote update  
git pull

## Running the program (as normal user, no "sudo" required)  
cd PiWifiCam  
python app.py  

## Start the program automatically while booting
cd PiWifiCam  
chmod +x autostart.sh  
open /etc/rc.local with your preferred editor and add the following line BEFORE the last line reading "exit 0":  
/home/pi/PiWifiCam/autostart.sh  
You may have to change the path if your code lives at another location.  
Restart the Raspberry Pi and test if program starts at boot:  

## Using PiWifiCam
The web interface runs on port 5000 of the Raspberry Pi. You can access it via http://ip_goes_here:5000 or at http://hostname.local:5000 if you have Avahi / mDNS running on your Pi and the client. Hostname is the hostname of your Pi that can be changed with raspi-config (advanced settings).  
http://ip_goes_here:5000/?video=300 Opens the slower, non-threaded interface. This interface will grab a single video frame at the given interval in milliseconds (300 in the example).

## Web API / URLs

### /heartbeat  
Returns JSON object with video status and framerate.

### /video_feed
No frills, bells and whistles MJPEG video feed from the camera.

### /single_frame.jpg
Non threaded (low CPU) single frame JPEG output.

### /
The root serves the web interface itself.

### /?video=[msecs]
Use non-threaded video with [msecs] delay between frames.

## Files
* app.py - the main application.
* config.py - application wide global variables.
* camera_pi.py - camera module for RPi camera module.
* camera_cv.py - camera module for generic (web)cams.
* autostart.sh - script to start the program via /etc/rc.local.
* static - this folder contains HTML, CSS and javascript files for the web interface.

Enjoy! Mark Dammer, Forres, Scotland 2017
