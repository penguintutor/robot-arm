# Python module for Maplin Robot Arm
# see http://www.penguintutor.com/grobot
# Copyright Stewart Watkiss 2013

'''Class for buttons

Draws the button, converts to rect, but does not do the collision detection 
which is handled by the main loop

'''

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

class Buttons:
	
	# static containing images
	images = {}
		
	def __init__(self, details={}):
		##-todo if details.has_key('type')
		pass
	
	
	def load_image(self, button_img, filename):
		'''
		Loads a button image
		
		:returns: None
		'''
		# Check to see if this image is already loaded in which case ignore
		if button_img in Buttons.images.keys() :
			return None
		
		# new image - load
		Buttons.images[button_img] = pygame.image.load(filename)
		return None
		
	
	def rect(self):
		'''Returns a rect object with co-ords of button
		
		:returns: rect
		'''
		rect = pygame.Rect(0, 0, 30, 60)
		return rect

		
	# def action(self, instruction):
		# '''Send instruction to robot arm 
		# This will run until an alternative instruction is sent or cancel is requested
		# 
		# Argument:
		# :param instruction: List of instruction [a,b,c]
		# :type instruction: list of numbers
		# :returns: None
		# 
		# ''' 
		# #self.robotarm.ctrl_transfer(0x40,6,0x100,0,instruction,1000)
		# return

	

