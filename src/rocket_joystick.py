#!/usr/bin/python
import cv

from pygtk import require
require('2.0')
import gtk, gobject


import pygame
#from pygame.locals import *

# ==================================

class JoystickManager:
	'''This class will be completed later.'''

	def __init__(self):
		self.joysticks = []

# ===============================

class StatefulJoystick:

	def __init__(self):

		self.joystick_debug = False
		self.joystick_object = None

    # ===============================

	def joystick_init(self):

		pygame.display.init()

		pygame.joystick.init()		#initialize joystick module
		pygame.joystick.get_init()	#verify initialization (boolean)

		joystick_count = pygame.joystick.get_count()	# get number of joysticks
		print('%d joystick(s) connected' %joystick_count)
		if not joystick_count:
			return False

		self.joystick_object = pygame.joystick.Joystick(0)
		self.joystick_object.init()

		self.num_axes = self.joystick_object.get_numaxes()
		self.num_buttons = self.joystick_object.get_numbuttons()



		self.prev_button_array = [0]*self.num_buttons
		self.prev_movement_state = [0, 0]
		self.prev_fire_button_state = 0

		gobject.idle_add( self.joystick_event_loop )

		return True

	# ===============================

	def joystick_event_loop(self):

		launcher = self.get_active_launcher()


		pygame.event.pump()	#necessary for os to pass joystick events

		axis_array = [self.joystick_object.get_axis(i) for i in range(self.num_axes)]
		button_array = [self.joystick_object.get_button(i) for i in range(self.num_buttons)]

		button_delta = map(lambda x, y: x-y, button_array, self.prev_button_array)


		if button_delta[1] > 0:
			self.laucher_id.set_value( self.laucher_id.get_value() + 1 )
		elif button_delta[2] > 0:
			self.laucher_id.set_value( self.laucher_id.get_value() - 1 )
		elif button_delta[3] > 0:
			fire_grp = self.stop_charge.get_group()
			fire_grp[ (self.get_fire_mode() + 1) % len(fire_grp) ].set_active(True)



		if self.joystick_debug:
#			print "Joystick Axes:", axis_array	# DEBUG
			print "Buttons:", button_delta	# DEBUG


		axis_array.reverse()



		if axis_array[0] < 0 and not self.prev_movement_state[0] < 0:
			self.movement_wrapper(1)
		elif axis_array[0] > 0 and not self.prev_movement_state[0] > 0:
			self.movement_wrapper(0)
		elif (axis_array[0] != self.prev_movement_state[0]):
			self.movement_wrapper(5)


		if axis_array[1] < 0 and not self.prev_movement_state[1] < 0:
			self.movement_wrapper(2)
		elif axis_array[1] > 0 and not self.prev_movement_state[1] > 0:
			self.movement_wrapper(3)
		elif (axis_array[1] != self.prev_movement_state[1]):
			self.movement_wrapper(5)


		self.prev_movement_state = axis_array[:2]


		if button_array[0]:
			launcher.start_movement(4)
		elif button_array[0] != self.prev_fire_button_state and self.stop_charge.get_group()[self.CONTINUOUS_CHARGE].get_active():
			self.movement_wrapper(5)

		self.prev_fire_button_state = button_array[0]


		self.prev_button_array = button_array[:]

		return True

    # ===============================

	def shutdown_joystick(self):
		pygame.joystick.quit()	# destroy objects and clean up
