#!/usr/bin/env python3
# Scratch Robot Arm 
# see http://www.penguintutor.com/robotarm
# Copyright Stewart Watkiss 2015


# scratchrobotarm is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# grobota is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.


import scratch, sys, time, re
import robotarm

''' User settings are in a file config.py
it's a python config file. In case of a corrupt file then it will prevent
the program from running. In which case copying default.py over config.py will
restore the default settings'''
# Load settings
import config

# Name and version of the program 
APP_NAME = 'Scratch Robot Arm'
APP_VERS = '0.0.1'
COPYRIGHT = 'Copyright Stewart Watkiss 2015'

CMD_LEN_TIME = 0.1




## global variables to track 
global ROBOTA
global s        ## Connection to scratch
global light_status # Track separately so we can apply at the same time as other actions
global DEBUG

DEBUG = False


# Although technically these are global variables they are mainly constants
# or instances that we update as required (eg. screen that we blit images to)


SCRATCH_CONNECT_ERRROR_TEXT = 'Unable to connect to Scratch.\nEnsure Scratch is started and remote sensors enabled.\nSee http://www.penguintutor.com/robotarm for more details.\n'


# Connect error messages
# Long error - used in initial connect, short error if later
ROBOT_CONNECT_ERROR_TEXT = (
    'Unable to connect to a robot arm via the usb interface.',
    'Please check that the robot arm is connected',
    'and switched on.',
    'See below for more troubleshooting information',
    '[url=http://www.penguintutor.com/robot-arm]http://www.penguintutor.com/robot-arm[/url]'
    )

# Robot connect short message
ROBOT_CONNECT_SHORT_ERROR = 'Unable to connect to robot arm\n'


# About / help message
ABOUT_TEXT = (
    APP_NAME+' - robot arm controller.',
    COPYRIGHT,
    'This program comes with ABSOLUTELY NO WARRANTY',
    'This is free software, and you are welcome to redistribute',
    'it under certain conditions',
    'See below for more information',
    '[url=http://www.penguintutor.com/robot-arm]http://www.penguintutor.com/robot-arm[/url]'
    )



def main():
    '''Start Gooey Robot Arm graphic application'''
    global DEBUG
    setup()
    # Loop to receive events from Scratch
    while True:
        (cmdtype, cmdstring) = s.receive()
        if DEBUG == True:
            print ("Received cmd ")
            print (cmdstring)
        run_command (cmdstring)



def setup():
    '''Initialise robot and connect to Scratch etc.'''
    
    global ROBOTA, s, light_status
    
    light_status = 0
    
    # Connect to scratch first
    try:
        s = scratch.Scratch()
    except scratch.ScratchError:
        print (SCRATCH_CONNECT_ERRROR_TEXT)
        exit()
    
    # Create instance of ROBOTA (robotarm class)
    # Does not connect
    ROBOTA = robotarm.RobotArm()
    
    
    # Should we auto_connect to robotarm (normally this would be the case, but can be turned off through config
    if (config.auto_connect):
        # check connect returns 1
        # currently this is a text error message - this should be output to the GUI
        if (ROBOTA.connect () !=1) :  
            # Error to console and to scratch
            s.broadcast('RobotArmNotConnected')
            print (ROBOT_CONNECT_ERROR_TEXT)
        else :
            # set to connected
            # Tell Scratch we are connected with a broadcast
            s.broadcast('RobotArmConnected')
            # Flash LED to confirm connection
            if (config.test_on_connect) :
                ROBOTA.flash_light()
    

# converts light status to a command (add this to command this during the action request)
def light_cmd (status) :
    if (status == 1):
        lightcmd = 'light-on'
    else:
        lightcmd = 'light-off'
    return ROBOTA.ROBOT_CMDS[lightcmd]
    

'''Handle commands from scratch'''
def run_command(cmd):
    global ROBOTA
    global light_status
    global CMD_LEN_TIME
    
    if cmd == "RobotArmConnect":
    # change status as appropriate
        # connect to robot arm
        if (ROBOTA.status() == 0) :
            if (ROBOTA.connect() != 1) :
                s.broadcast('RobotArmNotConnected')
                print (ROBOT_CONNECT_SHORT_ERROR)
            else :
                # set to connected
                # Flash LED to confirm connection
                if (config.test_on_connect) :
                    ROBOTA.flash_light()
                s.broadcast('RobotArmConnected')
    
    
    elif cmd == "RobotArmLightOn":
        light_status = 1
        ROBOTA.action(ROBOTA.ROBOT_CMDS['light-on'])
        
    elif cmd == "RobotArmLightOff":
        light_status = 0
        ROBOTA.action(ROBOTA.ROBOT_CMDS['light-off'])
        
    elif cmd == "RobotArmGripOpen":
        ROBOTA.action(add_cmds(ROBOTA.ROBOT_CMDS['grip-open'], light_cmd(light_status)))
        time.sleep(CMD_LEN_TIME)
        # All off except for light status
        ROBOTA.action(light_cmd(light_status))
    
    elif cmd == "RobotArmGripClose":
        ROBOTA.action(add_cmds(ROBOTA.ROBOT_CMDS['grip-close'], light_cmd(light_status)))
        time.sleep(CMD_LEN_TIME)
        # All off except for light status
        ROBOTA.action(light_cmd(light_status))

    elif cmd == "RobotArmWristUp":
        ROBOTA.action(add_cmds(ROBOTA.ROBOT_CMDS['wrist-up'], light_cmd(light_status)))
        time.sleep(CMD_LEN_TIME)
        # All off except for light status
        ROBOTA.action(light_cmd(light_status))
    
    elif cmd == "RobotArmWristDown":
        ROBOTA.action(add_cmds(ROBOTA.ROBOT_CMDS['wrist-down'], light_cmd(light_status)))
        time.sleep(CMD_LEN_TIME)
        # All off except for light status
        ROBOTA.action(light_cmd(light_status))
        
    elif cmd == "RobotArmElbowUp":
        ROBOTA.action(add_cmds(ROBOTA.ROBOT_CMDS['elbow-up'], light_cmd(light_status)))
        time.sleep(CMD_LEN_TIME)
        # All off except for light status
        ROBOTA.action(light_cmd(light_status))
    
    elif cmd == "RobotArmElbowDown":
        ROBOTA.action(add_cmds(ROBOTA.ROBOT_CMDS['elbow-down'], light_cmd(light_status)))
        time.sleep(CMD_LEN_TIME)
        # All off except for light status
        ROBOTA.action(light_cmd(light_status))

    elif cmd == "RobotArmShoulderUp":
        ROBOTA.action(add_cmds(ROBOTA.ROBOT_CMDS['shoulder-up'], light_cmd(light_status)))
        time.sleep(CMD_LEN_TIME)
        # All off except for light status
        ROBOTA.action(light_cmd(light_status))
    
    elif cmd == "RobotArmShoulderDown":
        ROBOTA.action(add_cmds(ROBOTA.ROBOT_CMDS['shoulder-down'], light_cmd(light_status)))
        time.sleep(CMD_LEN_TIME)
        # All off except for light status
        ROBOTA.action(light_cmd(light_status))
        
    elif (cmd == "RobotArmBaseCW" or cmd == "RobotArmBaseClockwise"):
        ROBOTA.action(add_cmds(ROBOTA.ROBOT_CMDS['base-cw'], light_cmd(light_status)))
        time.sleep(CMD_LEN_TIME)
        # All off except for light status
        ROBOTA.action(light_cmd(light_status))
    
    elif (cmd == "RobotArmBaseCCW"  or cmd == "RobotArmBaseCounterClockwise" or cmd == "RobotArmBaseAnticlockwise"):
        ROBOTA.action(add_cmds(ROBOTA.ROBOT_CMDS['base-ccw'], light_cmd(light_status)))
        time.sleep(CMD_LEN_TIME)
        # All off except for light status
        ROBOTA.action(light_cmd(light_status))

    elif cmd == "RobotArmStatus" :
        if (ROBOTA.status() == 1) :
            s.broadcast('RobotArmConnected')
        else :
            s.broadcast('RobotArmNotConnected')

    elif cmd == "RobotArmQuit" :
        sys.exit()
    
    else :
        if (cmd.startswith("RobotArm")) :
                s.broadcast('RobotArmInvalidCommand')


# Merges two commands together (eg. move motor + light on)
def add_cmds (cmd1, cmd2):
    return_cmd = [0,0,0]
    return_cmd[0] = cmd1[0] + cmd2[0]
    return_cmd[1] = cmd1[1] + cmd2[1]
    return_cmd[2] = cmd1[2] + cmd2[2]
    return (return_cmd)


if __name__ == '__main__':
    main()
