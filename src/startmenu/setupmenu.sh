#!/bin/bash
# Adds start menu for neopixel-gui
# This assumes it is being installed for the pi user
# If not then the configuration files need to be updated as well as the file locations
mkdir -p /home/pi/.config/menus
cp /opt/robotarm/src/startmenu/lxde-robots-applications.menu /home/pi/.config/menus/
mkdir -p /home/pi/.local/share/desktop-directories
cp robot_menu.directory ~/.local/share/desktop-directories/
mkdir -p /home/pi/.local/share/pixmaps
cp /opt/robotarm/src/startmenu/robots.png /home/pi/.local/share/pixmaps/
cp /opt/robotarm/src/startmenu/robotarmicon.png /home/pi/.local/share/pixmaps/
mkdir -p /home/pi/.local/share/applications/
cp /opt/robotarm/src/startmenu/robotarm.desktop /home/pi/.local/share/applications/
lxpanelctl restart