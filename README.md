# robot-arm
# GUI application for a USB robot arm


## Introduction

G-Robot Arm is a GUI application to control the cebekit Robot Arm. This is designed for use with the Raspberry Pi running Linux, but should work with any Linux computer. 

The robot arm used for testing is the Maplin robot arm, but I believe it should also work with the Cebek ModelC-6985 available from CPC Farnell. The robot arm is also available through other retailers, often called an Education Robot Arm or similar, although they sometimes come with a handheld remote control rather than the USB interface. The robot arm needs the USB interface which can be purchased separately if it was not already included.

The usb robot arm comes with Windows software only. This software has been written to allow the robot arm to be controlled from other computers, in particular Linux based computers such as the Raspberry Pi educational computer. This software is provided free of charge under the GPL version 3 license which allows you to view and edit the source code and redistribute as along as you make any changes available as open source software through the same license.

The application is similar to the remote control software supplied for Windows, but only handling the realtime functionality. This application is written using a similar layout and key bindings to the Windows software, but does not currently have the record and playback functionality.

This page provides some of the information for developers wanting to understand the software. If you just want to set the software up and run it then see the install instructions further down or at http://www.penguintutor.com/robotarm

The code is well documented within the source code, but this explains some of the high-level information and reasons for why some of the things are delivered as they are.

## Install

The instructions are provided for Linux only. The application has not been tested on other operating systems and is unlikely to be until much later in the development. The program uses Python which is currently available in two main versions: version 2.* and version 3.* (referred to as Python 2 and Python 3). 

Python 3 is the preferred distribution, however on some Linux distrutions, the install for Python 3 can be harder, so instructions for python 2 are included.


### Install for the Raspberry Pi

The Raspberry Pi is the easiest platform to install this on as it includes Python 3 Pygame as default. Instructions are therefore provided for Python 3 only. There is however an additional step that is required to provide permissions to access the device.


First download pyusb using:

wget https://github.com/walac/pyusb/tarball/master -O walac-pyusb.tar.gz


unzip and cd to the directory 
(actual directory name depends upon the latest version of pyusb) 

tar -xvzf walac-pyusb.tar.gz
cd walac-pyusb-*

sudo python3 setup.py install

Download the source code
git clone https://github.com/penguintutor/robot-arm.git


Copy the Udev USB rule using
sudo cp robot-arm/src/10-robotarm.rules /etc/udev/rules.d/

You can now launch the app by changing to the src directory and running grobota.py


## Install for other Linux distributions

The pre-requisites for the application are: pygame, libusb and pyusb, but these then also have their own dependancies (particularly pygame for Python 3).

These instructions are for Debian (or Ubuntu) based distributions the commands may be different for other distributions.

The first two can be installed using the instructions below (this does not setup pygame for Python 3 though only Python 2):

sudo apt-get install python-pygame libusb-1.0-0


pyusb can be installed manually.

First download using:

wget https://github.com/walac/pyusb/tarball/master -O walac-pyusb.tar.gz


unzip and cd to the directory 
(actual file and directory names depend upon the latest version of pyusb) 

tar -xvzf walac-pyusb.tar.gz
cd walac-pyusb-*

sudo python setup.py install
(and / or for Python 3)
sudo python3 setup.py install


###Python 3 pygame (optional)

Whilst pygame will work on Python 3 it is not necessarily available through the distributions repositories. These instructions explain how to install it manually.
This uses the current development version as at the time of writing the official release is 1.9.1 which will not work with Python 3.

Install the pre-requisites using:
sudo apt-get install python3-dev mercurial libsdl1.2-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsmpeg-dev libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev libfreetype6-dev libjpeg-dev 

Download pygame using:

hg clone https://bitbucket.org/pygame/pygame

cd pygame

python3 setup.py build
sudo python3 setup.py install


###Installing GRobotArm

Download the source code
git clone https://github.com/penguintutor/robot-arm.git

You can now launch the app by changing to the src directory and running grobota.py

If you get an error regarding permissions then you may also need to add the udev rule

sudo cp robot-arm/src/10-robotarm.rules /etc/udev/rules.d/

You can now launch the app by changing to the src directory and running grobota.py

###Adding a start menu button

If installing on a Raspberry Pi then the following will add the robotarm software to the LXDE start menu. This will only work on a Raspberry Pi using the default pi username.

/opt/robotarm/src/startmenu/setupmenu.sh

(or if running an older version of Raspbian prior to September 2015 use setupmenu-old.sh instead).

###Installing ARobotArm

The ARobotArm software adds support for the AstroPi buttons connected through a Raspberry Pi Sense Hat.

The following additional steps are required:

cd /boot/overlays
sudo wget https://github.com/raspberrypilearning/astro-pi-flight-case/raw/master/dtb/astropi-keys.dtbo --no-check-certificate


sudo nano /boot/config.txt
Go to the bottom of the file and enter the two lines below:

dtoverlay=rpi-sense
dtoverlay=astropi-keys
Press Ctrl + O then Enter to save, followed by Ctrl + X to quit.

Now reboot the Astro Pi.

These are based on instructions from https://www.raspberrypi.org/learning/astro-pi-flight-case/worksheet2/ 

The command arobota.py can now be run and the arm controlled using the buttons on the Astro Pi.

Programming style
=================

This has been written using Pygame. This is the first application I've written in Pygame and whilst Pygame and the programming method have provided flexibilty to create a friendly looking application, it did add some challenges in that certain functionality that is normally included by toolkits needed to be handled by my code. 

I originally avoided using object oriented programming for the GUI application influenced by Al Sweigart's book Making Games with Python & Pygame (see acknowledgments). This does make it easier to follow for new programmers that may struggle to grasp the object oriented concepts (it took me some time to grasp the paradigm when I first started OO programming). The downside is that to make it easier to follow I have had to create more global variables than I would normally like to. Many of these are variables that don't change "much". Technically they are not constants as they are updated, especially during the setup stage, but when treated as though they are constants by other functions then it is safe to treat them as though they were constants. I have created them using CAPITAL letters which convention states is normally only used for true constants. This is cheating, but hopefully cheating for the right reason. 

Whilst the idea of avoiding object oriented programming is a good idea when teaching programming, for a larger application this can make the code more complex. I have therefore refactored some of the code to use some object orientation and may looking at further rectoring to improve the code..


Window layout
=============

The window layout is designed for a fixed screen size of 800 x 600 pixels.
Some of the placement is created dynamically during the startup to allow the different blocks to be positioned and spaced differently, but that would need significant additional code to handle dynamic resizing of the screen. Whilst some of the code is written so as to make changing this to dynamic window sizing easier, it is not planned to change it to a dyanmic window size at this time.


Button lists (dictionaries)
===========================

The buttons are contained in a dictionary of dictionaries. 
This allows us to iterate over the buttons when drawing them and for checking for key press / mouse click. 

The key 'type' is used to determine how the buttons are handled (eg. are they 'movement' buttons)


Button images
=============

Each button has 3 images -normal -pressed and -hover
-pressed is a lighter version of -normal
-hover is the same as -normal (possible change in future) - or hover may be done using different colour for the text


Buttons can have an 'icon' applied which should be the same size as the button using transparency to see the button underneath.

Buttons can also have text applied - 'text' = centered vertically OR 'text1' = line 1, 'text2' = line 2 


Key presses
===========

Most sofware uses either the get_pressed function OR the event.type KEYUP/KEYDOWN for detecting key presses. Due to the behaviour of the different buttons this application uses both. This is so that normal application buttons and the Light button can use traditional button / key press techniques, but the movement buttons instead perform an action whilst a key is in the pressed state. This could have been done by tracking the state of each key, but is easier using the different techniques for each of the different button types.  

The code checks for the value of type. If it is 'movement' in then we use get_pressed . For the other buttons the event handling is written separately for each button in the loop code.


Message popup
=============

Window in centre of screen with OK button
It can have links to urls - which are encoded using BB-code eg.
[url=http://website.com]linkname[/url] or [url]http://website.com[/url]
only one link per line - and link is applied to the entire line

This should be used with just the url on that line eg. 

Line 1: See below for more information
Line 2: [url=http://www.penguintutor.com]www.penguintutor.com[/url]



Todo / Future development
=========================

At the moment only real-time operation of the robot arm is included. In future I hope to add record and playback functionality. Space has been left at the right hand side of the screen so that this can be included in the one window.

Hover doesn't do anything yet (perhaps add tooltips).


Acknowledgements
================

Although this program is my own work acknowledgements go to the following people whose resources I have used to assist in the creating of this program. 

Al Sweigart for the great books on Invent with Python http://inventwithpython.com/ which has been a great help with learning Pygame and influential in some of the techniques used.

Peter Lavelle whose MagPi article (issue 14) http://www.themagpi.com/en/issue/14 helped with the initial setup of the robot arm and usb modules and Jamie Scott whose WikiHow article http://www.wikihow.com/Use-a-USB-Robotic-Arm-with-a-Raspberry-Pi-%28Maplin%29 provided 
the instructions required to communicate with the robot arm.
