#!/usr/bin/env python3
# Gooey Robot Arm 
# see http://www.penguintutor.com/grobot
# grobota.py 
# Copyright Stewart Watkiss 2013 - 2015


# grobota is free software: you can redistribute it and/or modify
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


import pygame, sys, time, re, webbrowser
from pygame.locals import *
import robotarm

''' User settings are in a file config.py
it's a python config file. In case of a corrupt file then it will prevent
the program from running. In which case copying default.py over config.py will
restore the default settings'''
# Load settings
import config

# Name and version of the program 
APP_NAME = 'Gooey Robot Arm'
APP_VERS = '0.0.1'
COPYRIGHT = 'Copyright Stewart Watkiss 2015'



## global variables to track 
global light_status

# status fields (used for leds and toggling - 0, 1 (neg for errors if applicable)
# light 0 = led off, light 1 = led on
# negative number (eg. -1) means an error has occurred (connection lost / unable to connect)              
light_status = 0

# Although technically these are global variables they are mainly constants
# or instances that we update as required (eg. screen that we blit images to)

FPS = 30 # frames per second setting

# window dimension
WINDOW_WIDTH = 800 # size of window's width in pixels
WINDOW_HEIGHT = 600 # size of windows' height in pixels

# colour settings
BGCOLOUR = (31, 97, 164)
BUTTON_TXT_COLOR = (255, 255, 255) #White
TITLE_TXT_COLOR = (255, 255, 255) #White
# LED colour is a dictionary based on status number
# 0 is neutral (grey), 1 = good (green), -1 = bad (red)
LED_COLOUR = {0:(128,128,128),1:(0,255,0),-1:(255,0,0)}
MSG_BGCOLOUR = (41, 107, 174)
MSG_BORDERCOLOUR = (255, 255, 255)

# robotImg is 500 x 350
IMAGE_LOC = (50, 50)
TITLE_LOC_Y = 30


# each button 50 x 50
# position of first button
MV_BUTTON_START_X = 100
MV_BUTTON_START_Y = 450
MV_BUTTON_SIZE_X = 50
MV_BUTTON_SIZE_Y = 50

MV_BUTTON_PADDING_X = 8
MV_BUTTON_PADDING_Y = 6

MSG_WINDOW_SIZE_X = 500
MSG_WINDOW_SIZE_Y = 300


# size of status LED radius in pixels 
LED_SIZE = 10

# Font details
NORMAL_FONT_STYLE = None
TITLE_FONT_STYLE = None
SUBTITLE_FONT_STYLE = None
BUTTON_FONT_STYLE = None
NORMAL_FONT_SIZE = 22
TITLE_FONT_SIZE = 40
SUBTITLE_FONT_SIZE = 32
BUTTON_FONT_SIZE = 22

TEXT_SPACING = 20


# Connect error messages
CONNECT_ERROR_TEXT = (
	'Unable to connect to a robot arm via the usb interface.',
	'Please check that the robot arm is connected',
	'and switched on.',
	'See below for more troubleshooting information',
	'[url=http://www.penguintutor.com/robot-arm]http://www.penguintutor.com/robot-arm[/url]'
	)

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

## test with both of the formats below
#'[url=http://www.penguintutor.com/robot-arm]http://www.penguintutor.com/robot-arm[/url]'
#'[url]http://www.penguintutor.com/robot-arm[/url]'

''' BUTTONS - initially this contains the movement buttons - other buttons added during the setup stage '''
# dictionary of dictionary
# variable name in caps as though this is a constant, although some are initialised during setup in main (eg. positions and additional buttons) 
# col and row are the position of the button relative to the start of the 
# movement buttons (only for movement buttons)
# key presses are hardcoded below, although these could be moved to a configuration instead if required
# LED on/off button will be located within the same grid, but is handled differently as it retains status so is not included in the BUTTONS variable
# Buttons consists of a base image ('image') followed by -normal, -pressed, -hover
# Can also have icon - or text - or both 

BUTTONS = {
	0: 
		{
		'type':'movement',		# Type of button - movement means these move the robot, other types are light and generic (generic used for any standard button)
		'action':'grip-open',	# What we do - in ROBOT_CMDS
		'motor':'grip',			# Which motor it applies to - only exists on buttons related to motors so if key exists we know this is a motor movement key (not LED or other function)
		'label':'Grip open',	# User friendly - tooltip
		'char':'W',				# Key press (not case sensitive)
		'text1':'W',				# Text to print on button (can fit 2 lines) - in this case same as char - but not for other buttons
		'icon':'bl-open',		# Image to overlay on top of image (if defined)
		'col':0,				# Column in button grid
		'row':0					# Row in button grid
								# Also have startx, starty, endx, endy (button co-ords) which are added during setup()
		},
	1:
		{
		'type':'movement',
		'action':'grip-close',
		'motor':'grip',
		'label':'Grip close',
		'char':'S',
		'text1':'S',
		'icon':'bl-close',
		'col':0,
		'row':1
		},
	2:
		{
		'type':'movement',
		'action':'wrist-up',
		'motor':'wrist',
		'label':'Wrist up',
		'char':'E',
		'text1':'E',
		'icon':'bl-cwup',
		'col':1,
		'row':0
		},
	3:
		{
		'type':'movement',
		'action':'wrist-down',
		'motor':'wrist',
		'label':'Wrist down',
		'char':'D',
		'text1':'D',
		'icon':'bl-ccwdown',
		'col':1,
		'row':1
		},
	4:
		{
		'type':'movement',
		'action':'elbow-up',
		'motor':'elbow',
		'label':'Elbow up',
		'char':'R',
		'text1':'R',                                      
		'icon':'bl-cwup',
		'col':2,
		'row':0
		},
	5:
		{
		'type':'movement',
		'action':'elbow-down',
		'motor':'elbow',
		'label':'Elbow down',
		'char':'F',
		'text1':'F',
		'icon':'bl-ccwdown',
		'col':2,
		'row':1
		},
	6:                                                  
		{
		'type':'movement',
		'action':'shoulder-up',
		'motor':'shoulder',
		'label':'Shoulder up',
		'char':'U',
		'text1':'U',
		'icon':'bl-cwup',
		'col':3,
		'row':0
		},
	7:
		{
		'type':'movement',
		'action':'shoulder-down',
		'motor':'shoulder',
		'label':'Shoulder down',
		'char':'J',
		'text1':'J',
		'icon':'bl-ccwdown',
		'col':3,
		'row':1
		},
	8:
		{
		'type':'movement',
		'action':'base-cw',
		'motor':'base',
		'label':'Base clockwise',
		'char':'I',
		'text1':'I',
		'icon':'bl-cwup',
		'col':4,
		'row':0
		},
	9:
		{
		'type':'movement',
		'action':'base-ccw',
		'motor':'base',
		'label':'Base anti-clockwise',
		'char':'K',
		'text1':'K',
		'icon':'bl-ccwup',
		'col':4,
		'row':1
		},
	10:
		{
		# light / LED toggle button - 
		'type':'light',
		'action':'toggle-light',
		'label':'Toggle light status',
		'char':'L',
		'text1':'L',
		'col':5,
		'row':0,
		'icon':'bl-light'
		}
	}


	
# This is the key entry for light / LED button above - provided as a const in case another button is added causing it to be at a different pos
LIGHT_BUTTON_POS = 10


# These are excluded from normal buttons as depends upon status
CONNECT_BUTTON = {
	'connect':
		# connect to robot arm
		{
		'type':'generic',
		'startx' : 30,
		'starty' : 5,
		'endx' : 105,
		'endy' : 45,
		'image' : 'widebutton',
		'text' : 'Connect',
		},
	 'offline' :
		# disconnect from robot arm (work offline)
		# this replaces the connect button above
		{
		'type':'generic',
		'startx' : 30,
		'starty' : 5,
		'endx' : 105,
		'endy' : 45,
		'image' : 'widebutton',
		'text1' : 'Work',
		'text2' : 'offline'		
		} 
	}
	

# OK button used in popup windows
# Position is not included - to be added later
OK_BUTTON = {
	'image' : 'widebutton',
	'text' : 'OK'
}


	
	
STATUS_LED = {
		'connection':	# are we connected to the robot arm
			{
				'centrex' : 15,
				'centrey' : 25
			},
		'light':		# is the light on the robot arm (LED) switched on
			{
				# position is set during setup
				'centrex' : 0,
				'centrey' : 0
			}
	
	}


''' Prevent keyboard exception trace when ctrl-c pressed on cmd line'''
import signal
def int_handler(signum,frame):
	sys.exit()
# Set the signal handler
signal.signal(signal.SIGINT, int_handler)




def main():
	'''Start Gooey Robot Arm graphic application'''
	setup()
	loop()


def setup():
	'''Initialise pygame and setup variables etc.'''

	global FPSCLOCK, DISPLAYSURF
	# load images as globals so that we don't need to keep reloading
	global IMG_ROBOT, IMG_BUTTONS, IMG_GOPEN, IMG_GCLOSE, ROBOTA
	
	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	
	# set up the window
	DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
	pygame.display.set_caption(APP_NAME+' '+APP_VERS)
	
	# initialise button x,y positions (start and end) - just for movement and light buttons
	for i in range(len(BUTTONS)):
		if (BUTTONS[i]['type'] == 'movement' or BUTTONS[i]['type'] == 'light') : 
			BUTTONS[i]['startx'] = MV_BUTTON_START_X + (BUTTONS[i]['col'] * (MV_BUTTON_SIZE_X + MV_BUTTON_PADDING_X))
			BUTTONS[i]['endx'] = BUTTONS[i]['startx'] + MV_BUTTON_SIZE_X
			BUTTONS[i]['starty'] = MV_BUTTON_START_Y + (BUTTONS[i]['row'] * (MV_BUTTON_SIZE_Y + MV_BUTTON_PADDING_Y))
			BUTTONS[i]['endy'] = BUTTONS[i]['starty'] + MV_BUTTON_SIZE_Y
			BUTTONS[i]['image'] = 'stdbutton'
			
	# set the status led position for the light (below the light button - button element 10
	STATUS_LED['light']['centrex'] = BUTTONS[LIGHT_BUTTON_POS]['startx'] + (MV_BUTTON_SIZE_X / 2)
	STATUS_LED['light']['centrey'] = BUTTONS[LIGHT_BUTTON_POS]['endy'] + MV_BUTTON_PADDING_Y + (MV_BUTTON_SIZE_Y / 2)

	# Load all the images we are going to use
	# loaded as globals so we can access later
	IMG_BUTTONS = {
		# stdbutton is the movement button - square 50 x 50
		'stdbutton-normal': pygame.image.load('stdbutton-normal.png'), 
		'stdbutton-pressed': pygame.image.load('stdbutton-pressed.png'), 
		'stdbutton-hover': pygame.image.load('stdbutton-hover.png'),
		# widebutton is a wide standard button - 75 x 40
		'widebutton-normal':pygame.image.load('widebutton-normal.png'),
		'widebutton-pressed':pygame.image.load('widebutton-pressed.png'),
		'widebutton-hover':pygame.image.load('widebutton-hover.png'),
		'bl-open': pygame.image.load('bl-open.png'), 
		'bl-close': pygame.image.load('bl-close.png'), 
		'bl-cwup': pygame.image.load('bl-cwup.png'), 
		'bl-ccwup': pygame.image.load('bl-ccwup.png'), 
		'bl-cwdown': pygame.image.load('bl-cwdown.png'), 
		'bl-ccwdown': pygame.image.load('bl-ccwdown.png'),
		'bl-light': pygame.image.load('bl-light.png')
		}
	
	
	IMG_ROBOT = pygame.image.load('robotarm.png')
	
	DISPLAYSURF.fill(BGCOLOUR)  
	
	# Create instance of ROBOTA (robotarm class)
	# Does not connect
	ROBOTA = robotarm.RobotArm()
	
	# autoconnect is after we have setup the GUI
	draw_screen()
	
	# Should we auto_connect (normally this would be the case, but can be turned off through config
	if (config.auto_connect):
		# check connect returns 1
		# currently this is a text error message - this should be output to the GUI
		if (ROBOTA.connect () !=1) :  
			message_popup ("Unable to connect", CONNECT_ERROR_TEXT)
		else :
			# set to connected
			# Flash LED to confirm connection
			if (config.test_on_connect) :
				ROBOTA.flash_light()
	

def loop():
	'''Program loop, handle key presses and button presses'''
	# globals
	global light_status
	
	''' For control buttons we track using the number of the switch (0 to 9) '''
	# buttons pressed can be multiple if we have multiple keys pressed down simultaneously
	buttons_pressed = []
	
	# previous buttons pressed to check for changes that need sending to the arm
	prev_action = [0,0,0]

	# mouse behaves differently to most apps for the control buttons
	# rather than requiring a click with mouse click down and up on a button
	# this acts on a mouse button down as we want to continue operating the
	# robot for as long as the button is held down

	# mouse can only interact with one button at a time so single entry rather than list used for key
	mouse_status = 'none'	# can be 'none', 'hover' (when over a button), 'pressed' (when left mouse button pressed on a button)
	# mouse button num is used for movement buttons - if -1 then see mouse_button_other
	mouse_button_num = -1
	# refactor this .... - too complex	
	# used for buttons other than movement buttons - string for button label
	#mouse_button_other = ''

	while True: # Main game loop
		
		# event loop - iterates once over the loop for each event - ignore movement keys as they have already been handled using get_pressed
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == KEYDOWN:
			# note by default all keys will match regardless of case 
			# would need to know status of shift / caps lock if wanted to
			# check case but not required for this
				#if (event.key in (K_ESCAPE, K_q)):
				if (event.key == K_ESCAPE):
					# check with user
					# Do you really want to quit Y/N?
					##TODO add confirmation request
					# treat as true
					sys.exit()
					
				if event.key == K_F1:
					message_popup ("About "+APP_NAME+" "+APP_VERS, ABOUT_TEXT)
					
				# LED toggle button - change status
				# ord (converts from char to num and add 32 which is char(a))
				if (event.key == ord(BUTTONS[LIGHT_BUTTON_POS]['char'])+32):
					# if added to buttons_pressed here would only apply for this loop - need to do it elsewhere instead
					#buttons_pressed = add_button_press (buttons_pressed, LIGHT_BUTTON_POS)
					# toggle light status (this works for 1 or 0)
					light_status = (light_status -1) * -1 
					continue

#			elif event.type == KEYUP:
#				# LED toggle button - just set button to up
#				if (event.key == ord(BUTTONS[LIGHT_BUTTON_POS]['char'])+32): 
#					buttons_pressed = del_button_press (buttons_pressed, 10)
#					continue

			# handle mouse button down on normal buttons
			# most buttons this just shows button pressed and then MOUSEBUTTONUP actions the button (as per most applications), but for light button we use this to trigger
			elif event.type == MOUSEBUTTONDOWN:
				# light button
				mouse_position = pygame.mouse.get_pos()
				if (mouse_position[0] >= BUTTONS[LIGHT_BUTTON_POS]['startx'] and mouse_position[0] <= BUTTONS[LIGHT_BUTTON_POS]['endx'] and mouse_position[1] >= BUTTONS[LIGHT_BUTTON_POS]['starty'] and mouse_position[1] <= BUTTONS[LIGHT_BUTTON_POS]['endy']):
					# if added to buttons_pressed here then would only show for this one go around the loop - so not done - need to do this a different way instead
					#buttons_pressed = add_button_press (buttons_pressed, LIGHT_BUTTON_POS)
					light_status = (light_status -1) * -1 
					continue
				# other buttons just change to click status - but wait until 
				# unclick before performing action
				
				# Connect / disconnect button
				# set to appropriate button
				if (ROBOTA.status() == 1) :
					current_connect_button = 'offline'
				else :
					current_connect_button = 'connect'
					
				if (mouse_position[0] >= CONNECT_BUTTON[current_connect_button]['startx'] and mouse_position[0] <= CONNECT_BUTTON[current_connect_button]['endx'] and mouse_position[1] >= CONNECT_BUTTON[current_connect_button]['starty'] and mouse_position[1] <= CONNECT_BUTTON[current_connect_button]['endy']):
					# due to complexity this currently works on first click
					# to refactor in future
					
					# change status as appropriate
					# connect to robot arm
					if (ROBOTA.status() == 0) :
						if (ROBOTA.connect() != 1) :
							message_popup ("Unable to connect", CONNECT_ERROR_TEXT)
						else :
							# set to connected
							# Flash LED to confirm connection
							if (config.test_on_connect) :
								ROBOTA.flash_light()
					# disconnect from robot arm
					else :
						ROBOTA.disconnect()

		# Now handle movement keys and mouse buttons on movement
		pressed_keys = pygame.key.get_pressed()
		# reset list of buttons
		buttons_pressed = []
		# check each of the action buttons to see if they are pressed (only for movement buttons and light)
		# other buttons track status using KEYDOWN / KEYUP instead
		for i in range(len(BUTTONS)):
			#if (BUTTONS[i]['type']=='movement' and pressed_keys[ord(BUTTONS[i]['char'])+32]):
			if (pressed_keys[ord(BUTTONS[i]['char'])+32]):
				buttons_pressed = add_button_press (buttons_pressed, i)
				
		# Is the mouse key currently pressed down 
		mouse_buttons = pygame.mouse.get_pressed()
		
		# Only care about button 1
		if (mouse_buttons[0] == True):
			# see if the mouse is over one of the movement buttons
			mouse_position = pygame.mouse.get_pos()
			
			for i in range(len(BUTTONS)):
				if (BUTTONS[i]['type']=='movement' and mouse_position[0] >= BUTTONS[i]['startx'] and mouse_position[0] <= BUTTONS[i]['endx'] and mouse_position[1] >= BUTTONS[i]['starty'] and mouse_position[1] <= BUTTONS[i]['endy']):
					buttons_pressed = add_button_press (buttons_pressed, i)
				
			##TODO add additional buttons in future


		# draw screen shows default button images (even for pressed buttons)
		draw_screen()

		# Check for key / mouse presses
		
		# Update buttons that are pressed
		for this_button in buttons_pressed:
			draw_button (BUTTONS[this_button], 'pressed')

		# Highlight relevant part of the robot
		##TODO implement this in future version

		# Send instruction to the robot arm
		# if no buttons pressed send cancel
		current_action = [0,0,0]
		for this_action in buttons_pressed:
			# only do this for motor buttons for light button we skip and add later (it's a toggle button)
			if (BUTTONS[this_action]['type'] != 'movement') :
				continue
			temp_action = ROBOTA.ROBOT_CMDS[BUTTONS[this_action]['action']]
			current_action[0] += temp_action[0]
			current_action[1] += temp_action[1]
			current_action[2] += temp_action[2]
		
		# add light status
		if (light_status == 1):
			lightcmd = 'light-on'
		else:
			lightcmd = 'light-off'
		temp_action = ROBOTA.ROBOT_CMDS[lightcmd]
		current_action[0] += temp_action[0]
		current_action[1] += temp_action[1]
		current_action[2] += temp_action[2]
		
		# check to see if changed
		if (prev_action[0] != current_action[0] or prev_action[1] != current_action[1] or prev_action[2] != current_action[2]):
			# send instruction
			ROBOTA.action(current_action)
			# update previous action
			prev_action = current_action
		
		# Add light status
		draw_status_led (STATUS_LED['light'], light_status)

		# update screen with changes
		pygame.display.update()
		FPSCLOCK.tick(FPS)
		
		# Delay to reduce CPU utilization
		#time.sleep (0.2)



def draw_screen():
	'''Draws the static components of the screen (including buttons in std position)'''

	# reset the screen background - removes items previously added to the screen (eg. popup)
	DISPLAYSURF.fill(BGCOLOUR)

	# setup font 
	button_font = pygame.font.Font(BUTTON_FONT_STYLE, BUTTON_FONT_SIZE)
	title_font = pygame.font.Font(TITLE_FONT_STYLE, TITLE_FONT_SIZE)	

	
	# Title text
	txt_title = title_font.render(APP_NAME, True, TITLE_TXT_COLOR)
	rect_title = txt_title.get_rect() 
	rect_title.center = (WINDOW_WIDTH/2, TITLE_LOC_Y)
	DISPLAYSURF.blit(txt_title, rect_title)
		
	# Robot img
	DISPLAYSURF.blit(IMG_ROBOT, IMAGE_LOC)
	draw_buttons()
	draw_connect_status()



def draw_connect_status ():
	''' Draw status LED, status and button to connect / go offline '''
	global ROBOTA
	
	connect_status = ROBOTA.status()
	
	# show status led
	draw_status_led (STATUS_LED['connection'], connect_status)
		
	# draw connect button depending upon status
	if (connect_status == 1) :	
		# if connected - button to go offline
		draw_button (CONNECT_BUTTON['offline'])
	else : 
		# if not connected - connect button 
		draw_button (CONNECT_BUTTON['connect'])



def draw_status_led (led, status) :
	'''Draw status LED
	
	:param led: led dictionary entry
	:type led: dictionary
	:param status: LED status (-1 = red, 0 = grey, 1 = green)
	:type status: number
	:returns: None
	'''

	pygame.draw.circle(DISPLAYSURF, LED_COLOUR[status], (int(led['centrex']),int(led['centrey'])), LED_SIZE, 0)



def draw_buttons ():
	'''Draw all the buttons in default state

	'''

	for i in range(len(BUTTONS)):
		draw_button (BUTTONS[i])

	return




def add_button_press (button_list, button_action):
	''' adds an button to the list of pressed buttons
	rather than just using the list functions this adds checks that we are not
	doing anything silly like trying to move the same motor up and down at the same time
	and prevents duplicates (eg. key and press on same button)
	
	In the case of a entry requested for the same device but different action
	then remove existing entry for that device
	which means that they effectively cancel each other out. A third entry would add it back
	eg. key for up, key for down and mouse press for up - would result in an up
	this works only if the keys are done before the mouse as otherwise two in a row could ignore the duplicate first
	
	:param action_list: Current list
	:type action_list: list of numbers
	:param new_action: The action to add
	:type action_list: number
	:returns: list of numbers
	'''
	
	# setup font 
	button_font = pygame.font.Font(BUTTON_FONT_STYLE, BUTTON_FONT_SIZE)
	
	# Gets the device for the new button - use either motor or if not motor then action
	if (BUTTONS[button_action]['type'] == 'movement') :
		this_device = BUTTONS[button_action]['motor']
	else :
		this_device = BUTTONS[button_action]['action']
	
	
	# iterate over list looking for duplicate device
	for existing_button in button_list :
		# if the existing button has a motor reference then we use that - else use action
		if (BUTTONS[existing_button]['type'] == 'movement') :
			existing_device = BUTTONS[existing_button]['motor']
		else :
			existing_device = BUTTONS[existing_button]['action']
		if (this_device == existing_device) :
			# check to see if this is the same (in which case ignore new)
			# or if it's a conflict in which case remove existing and don't add
			if (BUTTONS[button_action]['action'] != BUTTONS[existing_button]['action']) :
				# conflict so remove
				button_list.remove(existing_button)
				return button_list
			else :
				# no conflict so ignore this add and return original list
				return button_list
				
	# Not found duplicate / conflicting - so add
	button_list.append(button_action)
	return button_list


def del_button_press (button_list, existing_button):
	''' removes an entry from the list
	this could be done using the normal list.remove included as a method
	for consistancy with add_button_press
	
	:param action_list: Current list
	:type action_list: list of numbers
	:param new_action: The action to add
	:type action_list: number
	:returns: list of numbers
	'''
	
	# uses list.remove function
	button_list.remove(existing_button)
	return button_list


def draw_button (button_info, status='standard'):
	'''Draw a single main action buttons
	
	The button_info must include a location for the button either with the top left (startx and
	starty) or with the bottom right (endx and endy). If only one pair is provided then the
	image size is used to determine the missing values. These values should either exist as
	dictionary keys or not it will not try and work out whether the values are valid.

	Argument:
	:param button_info: Details of button to draw
	:type button: Dictionary
	:param status: Status of the button eg. 'normal', 'hover', 'pressed'
	:type status: string
	:returns: button_info for success (including updated coords), None for failure
	'''
	
	# setup font 
	button_font = pygame.font.Font(BUTTON_FONT_STYLE, BUTTON_FONT_SIZE)

	# set button to appropriate type
	if (status == 'pressed'):
		image_button = button_info['image']+'-pressed'
	else:
		image_button = button_info['image']+'-normal'

	# get the size of the button - this will be used later for start/end positions (if required) and for the text positions etc.
	button_height = IMG_BUTTONS[image_button].get_height()
	button_width = IMG_BUTTONS[image_button].get_width()
	
	
	# Check whether we have start and end, just start, just end - or error
	if (('startx' in button_info) and ('starty' in button_info) and ('endx' in button_info) and ('endy' in button_info)) :
		# We have the information we need 
		pass
	elif (('startx' in button_info) and ('starty' in button_info)) :
		# we have start so calculate the end
		button_info['endx'] = button_info['startx']+button_width
		button_info['endy'] = button_info['starty']+button_height
	elif (('endx' in button_info) and ('endy' in button_info)) :
		# we have end so calculate the start
		button_info['startx'] = button_info['endx']-button_width
		button_info['starty'] = button_info['endy']-button_height
	else :
		# don't have either start or end coords
		return None
	

	# Main button image
	DISPLAYSURF.blit(IMG_BUTTONS[image_button], (button_info['startx'], button_info['starty']))

	# 'text' is vert centre - OR 'text1' = line1, 'text2' = line2
	if 'text' in button_info.keys() :
		txt_button = button_font.render(button_info['text'], True, BUTTON_TXT_COLOR)
		rect_button = txt_button.get_rect() 
		rect_button.center = (button_info['startx']+(button_width/2), button_info['starty']+(button_height/2))
		DISPLAYSURF.blit(txt_button, rect_button)
	# button text top line (1 letter for action buttons)
	if 'text1' in button_info.keys() :
		txt_button = button_font.render(button_info['text1'], True, BUTTON_TXT_COLOR)
		rect_button = txt_button.get_rect() 
		rect_button.center = (button_info['startx']+(button_width/2), button_info['starty']+(button_height/4))
		DISPLAYSURF.blit(txt_button, rect_button)
	if 'text2' in button_info.keys() :
		txt_button = button_font.render(button_info['text2'], True, BUTTON_TXT_COLOR)
		rect_button = txt_button.get_rect() 
		rect_button.center = (button_info['startx']+(button_width/2), button_info['endy']-(button_height/4))
		DISPLAYSURF.blit(txt_button, rect_button)
	# button icon (eg. arrow)
	if 'icon' in button_info.keys() :
		DISPLAYSURF.blit(IMG_BUTTONS[button_info['icon']], (button_info['startx'], button_info['starty']))

	return button_info



def message_popup (title, message, buttons={0:'OK'}):
	''' Draw box in the middle of the screen with OK (close) button 
	then wait for click on button before returning to previous loop
	
	text can contain url bbcode eg. [url=http://website.com]linkname[/url] or [url]http://website.com[/url] - but only url per line and link will 
	work for that entire line
	
	WARNING - if two many text lines or the lines are too long then they will overwrite outside
	of the safe area. Calling code needs to keep these to reasonable lengths.
	
	Argument:
	:param title: Title of error
	:type title: string
	:param message: Strings for error message 
	:type message: list of strings
	:param buttons: dictionary of buttons (not currently supported)
	:type buttons: dictionary - seq number for keys, string for values (not currently supported)
	:returns: int of index of buttons dictionary
	'''
	
	# dictionary of urls key is the line number starting at 0 (ie. same as 
	# message key number)
	urls = {}
	
	# list of updated lines after urls removed
	text_lines = {}
	
	# Regular expression to find the url 
	# Does not remove the tags - just gets the url out - we remove the tags afterwards
	# The reg exp pull the entire line apart so that we can it back together using matches 
	# Easier than trying to use multiple subs to replace the [url] parts

	# reg exp with url in the [] tags
	re_1_string = r'(?P<pre>[^\]]*)(?P<start>\[url=(?P<url>[^\]]+)\])(?P<urltitle>[^\[]+)(?P<end>\[\/url\])(?P<post>.*)'
	url_re_1 = re.compile (re_1_string)
	# reg exp with url between the [url] tags
	re_2_string = r'(?P<pre>[^\]]*)(?P<start>\[url\](?P<url>[^\[]+))(?P<end>\[\/url\])(?P<post>.*)'
	url_re_2 = re.compile (re_2_string)

	
	
	# Search through the lines of the message looking for a BBcode for url
	# Only url supported and applies to entire line
	for i in range(len(message)) :
		# set text_lines - replace if we get a match
		text_lines[i] = message[i]
		matches = url_re_1.search(message[i])
		if (matches) :
			urls[i] = matches.group('url')
			text_lines[i] = matches.group('pre')+matches.group('urltitle')+matches.group('post')
		else :
			matches = url_re_2.search(message[i])
			if (matches) :
				urls[i] = matches.group('url')
				text_lines[i] = matches.group('pre')+matches.group('url')+matches.group('post')
	
	
	# setup font 
	# Note we use subtitle font - this should not be as large as the window title
	subtitle_font = pygame.font.Font(SUBTITLE_FONT_STYLE, SUBTITLE_FONT_SIZE)
	normal_font = pygame.font.Font(NORMAL_FONT_STYLE, NORMAL_FONT_SIZE)
	
	message_window_startx = (WINDOW_WIDTH/2)-(MSG_WINDOW_SIZE_X/2)
	message_window_starty = (WINDOW_HEIGHT/2)-(MSG_WINDOW_SIZE_Y/2)
	# Rect uses size rather than co-ords for bottom right
	
	# filled rectangle
	pygame.draw.rect(DISPLAYSURF, MSG_BGCOLOUR, [message_window_startx, message_window_starty, MSG_WINDOW_SIZE_X , MSG_WINDOW_SIZE_Y], 0)
	# border
	pygame.draw.rect(DISPLAYSURF, MSG_BORDERCOLOUR, [message_window_startx, message_window_starty, MSG_WINDOW_SIZE_X , MSG_WINDOW_SIZE_Y], 2)

	txt_title = subtitle_font.render(title, True, TITLE_TXT_COLOR)
	rect_title = txt_title.get_rect() 
	rect_title.center = (message_window_startx + (MSG_WINDOW_SIZE_X/2), message_window_starty+25)
	DISPLAYSURF.blit(txt_title, rect_title)
	
	# text start position (inc Y as each line is written)
	text_box_x = message_window_startx + 10
	text_box_y = message_window_starty + 75

	# text_string and rect_string are stored in dictionaries (so that we can use them later to check if mouse is over them (collide)
	text_string = {}
	rect_string = {}
	for i in range(len(text_lines)) :
		# print text lines
		text_string[i] = normal_font.render(text_lines[i], True, TITLE_TXT_COLOR)
		rect_string[i] = text_string[i].get_rect() 
		rect_string[i].topleft = (text_box_x, text_box_y)
		DISPLAYSURF.blit(text_string[i], rect_string[i])
		text_box_y += TEXT_SPACING

	# create button based on template
	close_errwin_button = OK_BUTTON
	close_errwin_button['endx'] = message_window_startx + MSG_WINDOW_SIZE_X  - 10
	close_errwin_button['endy'] = message_window_starty + MSG_WINDOW_SIZE_Y  - 10


	# as well as drawing the button, updates with the coords that are missing (ie. startx and starty)
	close_errwin_button = draw_button (close_errwin_button, status='standard')
	
	# A loop - we won't handle any of the previous loop until we close this window with the OK butotn
	# which key mouse was last pressed in
	# used so we only accept mouse press when it starts and ends on that button
	# use -2 for OK button, ** -1 for none pressed ** , 1,2... (for a line)
	MOUSE_PRESS_OK = -2
	MOUSE_PRESS_NONE = -1
	
	mouse_press = MOUSE_PRESS_NONE
	while True :
		# Need to put the quit event back in as we won't handle the one in the main loop
		for event in pygame.event.get():
			# have we handled this event (used to determine if we should continue the loop)
			event_handled = False
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			# Return pressed and released - accept the OK 
			elif (event.type == KEYUP and event.key == K_RETURN) :
				# no need to clean up, next iteration around previous loop will redraw the screen
				return

			## button pressed down (potentially first part of button click 
			# if we are over a valid button
			elif (event.type == MOUSEBUTTONDOWN) :
				mouse_position = pygame.mouse.get_pos()
				# loop over url links to see if we have a match
				# loops over all lines in message, but ignores those without a url entry
				for i in range(len(message)) :
					# does this key exist in the url array
					if (i in urls) :
						# is mouse over this line - use rect string and collide 
						if (rect_string[i].collidepoint(mouse_position)) :
							mouse_press = i
							event_handled = True
				if (event_handled) : 
					continue
							
				#OK button
				if (mouse_position[0] >= close_errwin_button['startx'] and mouse_position[0] <= close_errwin_button['endx'] and mouse_position[1] >= close_errwin_button['starty'] and mouse_position[1] <= close_errwin_button['endy']):
					mouse_press = MOUSE_PRESS_OK
				else :
					mouse_press = MOUSE_PRESS_NONE
					
			## button up - if button already pressed then this indicate run that action
			elif (event.type == MOUSEBUTTONUP) :

				mouse_position = pygame.mouse.get_pos()
				# loop over url links to see if we have a match
				# loops over all lines in message, but ignores those without a url entry
				for i in range(len(message)) :
					# does this key exist in the url array
					if i in urls :
						# is mouse over this line - use rect string and collide 
						if (rect_string[i].collidepoint(mouse_position)) :
							# open the url using system default browser
							webbrowser.open(urls[i], 1)
							event_handled = True
				if (event_handled) : 
					mouse_press = MOUSE_PRESS_NONE
					continue
				
				# OK button				
				if (mouse_press == MOUSE_PRESS_OK and mouse_position[0] >= close_errwin_button['startx'] and mouse_position[0] <= close_errwin_button['endx'] and mouse_position[1] >= close_errwin_button['starty'] and mouse_position[1] <= close_errwin_button['endy']):
					return 0
				
			else :
				# otherwise reset mouse_press variable
				mouse_press = MOUSE_PRESS_NONE
				
		pygame.display.update()
		FPSCLOCK.tick(FPS)


if __name__ == '__main__':
    main()
