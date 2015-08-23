# Python module for Maplin Robot Arm
# see http://www.penguintutor.com/grobot
# Copyright Stewart Watkiss 2013

# The robot arm module is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# robotarm.py is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.

# required USB libraries 
import usb.core, usb.util, time


class RobotArm:
	'''Class for controlling the arm'''
	
	# dictionary of lists with the command to send to the arm
	ROBOT_CMDS = {
		'grip-open' : [2,0,0],
		'grip-close' : [1,0,0],
		'wrist-up' : [4,0,0],
		'wrist-down' : [8,0,0],
		'elbow-up' : [16,0,0],
		'elbow-down' : [32,0,0],
		'shoulder-up' : [64,0,0],
		'shoulder-down' : [128,0,0],
		'base-cw' : [0,1,0],			#clockwise
		'base-ccw' : [0,2,0],			#counter clockwise
		'light-on' : [0,0,1],
		'light-off' : [0,0,0],	# This is same as all-off
		'all-off' : [0,0,0]
		}
		
	def __init__(self):
		# status 0 = not connected, status 1 = connected, status neg = error
		self.connect_status = 0
	
	def connect(self):
		'''Establish connection to USB device
		
		If multiple robot arms are connected then it controls the first
		this could be updated to allow multiple arms using findAll but
		would then need a way to select the appropriate arm so that feature
		is not included in this version
		
		:returns: number (0 = failure, 1 = success)
		'''
		self.robotarm = usb.core.find(idVendor=0x1267, idProduct=0x000)
		if (self.robotarm == None):
			self.connect_status = 0
			return 0
		self.connect_status = 1
		return 1


	def disconnect(self):
		'''Disconnect from USB device
		
		Doesn't actually send anything to the arm - but updates status
		
		:returns: number (0 = disconnected)
		'''
		self.connect_status = 0
		return 0


	def status(self):
		return self.connect_status

	def action(self, instruction):
		'''Send instruction to robot arm 
		This will run until an alternative instruction is sent or cancel is requested
		
		Argument:
		:param instruction: List of instruction [a,b,c]
		:type instruction: list of numbers
		:returns: status
		
		''' 
		if (self.connect_status == 1) :
			self.robotarm.ctrl_transfer(0x40,6,0x100,0,instruction,1000)
			return 1
		else :
			return self.connect_status

	
	def cancel(self):
		'''Cancel any actions - ie send [0,0,0]'''
		if (self.connect_status == 1) :
			self.robotarm.ctrl_transfer(0x40,6,0x100,0,[0,0,0],1000)
			return 1
		else :
			return self.connect_status


	def flash_light(self):
		'''Flash LED twice to confirm it's working
		Normally called on first connect to show it's connected
		This will cancel any existing actions if run at another time
		'''
		
		if (self.connect_status == 1) :
			self.robotarm.ctrl_transfer(0x40,6,0x100,0,self.ROBOT_CMDS['light-on'],1000)
			time.sleep(0.5)
			self.robotarm.ctrl_transfer(0x40,6,0x100,0,self.ROBOT_CMDS['light-off'],1000)
			time.sleep(0.5)
			self.robotarm.ctrl_transfer(0x40,6,0x100,0,self.ROBOT_CMDS['light-on'],1000)
			time.sleep(0.5)
			self.robotarm.ctrl_transfer(0x40,6,0x100,0,self.ROBOT_CMDS['light-off'],1000)
			return 1
		else :
			return self.connect_status
			
			
