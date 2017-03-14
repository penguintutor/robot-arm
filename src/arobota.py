#!/usr/bin/env python3
# Sense Hat Robot Arm 
# see http://www.penguintutor.com/grobot
# arobota.py 
# Copyright Stewart Watkiss 2017


# arobota is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# arobota is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.

import robotarm, pygame, time
from sense_hat import SenseHat
from pygame.locals import *


def status_led (status) :
    if (status == 1): 
        status_color = (0,255,0)
    else :
        status_color = (255,0,0)
        
    sense.set_pixel(7, 0, status_color)



pygame.init()
pygame.display.set_mode((640, 480))

sense = SenseHat()
sense.clear()

sense.set_rotation(270)

# currentmode used to determine which motors we are controlling
# 0 = menu / error (no motors)
# 1 = base + shoulder
# 2 = shoulder + elbow
# 3 = elbow + wrist
# 4 = wrist + gripper
# 5 = gripper + light
currentmode = 0;

#instruction to send to the arm
current_action = [0,0,0]

status_led (0)

sense.show_message("Robot Arm")


status_led (0)
ROBOTA = robotarm.RobotArm()
ROBOTA.connect()
status_led (ROBOTA.status())
ROBOTA.flash_light()


# buttons 1 = pressed, 0 = not pressed
buttons_pressed = {"up" : 0, "down" : 0, "left" : 0, "right" : 0}

# Array for each of the 4 direction buttons with the appropriate commands based on mode
cmds = {"up" : ['none', 'shoulder-up', 'elbow-up', 'wrist-up', 'grip-open', 'light-on'],
    "down" : ['none', 'shoulder-down', 'elbow-down', 'wrist-down', 'grip-close', 'light-on'],
    "left" : ['none', 'base-ccw', 'shoulder-down', 'elbow-down', 'wrist-down', 'grip-close'],
    "right" : ['none', 'base-cw', 'shoulder-up', 'elbow-up', 'wrist-up', 'grip-open']
    }

def move_up(event):
    global currentmode
    if event.action=='pressed':
        currentmode += 1
    print(event)

def move_down(event):
    global currentmode
    if event.action=='pressed':
        currentmode -= 1
    print(event)
    
sense.stick.direction_up = move_up
sense.stick.direction_down = move_down

running = True

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:  # Use KEYUP when released
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_u:
                buttons_pressed["up"] = 1 
            elif event.key == K_d:
                buttons_pressed["down"] = 1
            elif event.key == K_l:
                buttons_pressed["left"] = 1
            elif event.key == K_r:
                buttons_pressed["right"] = 1
            elif event.key == K_a:
                currentmode -= 1
            elif event.key == K_b:
                currentmode += 1
        if event.type == KEYUP:  # Use KEYUP when released
            if event.key == K_u:
                buttons_pressed["up"] = 0
            elif event.key == K_d:
                buttons_pressed["down"] = 0
            elif event.key == K_l:
                buttons_pressed["left"] = 0
            elif event.key == K_r:
                buttons_pressed["right"] = 0
            
            
    if (currentmode < 0) :
        currentmode = 0
    elif (currentmode > 5) :
        currentmode = 5
        
    # In mode 0 have different actions
    if (currentmode != 0):
        
        prev_action = current_action
        current_action = [0,0,0]
        
        for this_key in buttons_pressed.keys() :
            if (buttons_pressed[this_key] == 1):
                temp_action = ROBOTA.ROBOT_CMDS[cmds[this_key][currentmode]]
                current_action[0] += temp_action[0]
                current_action[1] += temp_action[1]
                current_action[2] += temp_action[2]
            
        # check to see if changed
        if (prev_action[0] != current_action[0] or prev_action[1] != current_action[1] or prev_action[2] != current_action[2]):
            # send instruction
            ROBOTA.action(current_action)
            # update previous action
            prev_action = current_action
    # Mode 0 - up = connect / reconnect  
    else :
        if (buttons_pressed['up'] == 1 && ROBOTA.status() == 0):
            ROBOTA.connect()
            ROBOTA.flash_light()
        
    sense.show_letter(str(currentmode))
    status_led (ROBOTA.status())
    
    time.sleep(0.2)#
    

