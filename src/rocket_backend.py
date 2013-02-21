#!/usr/bin/python

import logging
import sys
import usb.core
import usb.util



class RocketManager:

	vendor_product_ids = [(0x1941, 0x8021), (0x0a81, 0x0701), (0x0a81, 0xff01), (0x1130, 0x0202), (0x2123,0x1010)]
	launcher_types = ["Original", "Webcam", "Wireless", "Striker II", "OIC Webcam"]
	housing_colors = ["green", "blue", "silver", "black", "gray"]

	def __init__(self):
		logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG, stream=sys.stdout)
		self.launchers = []

	def is_supported_device(self, dev):
		for (cheeky_vendor_id, cheeky_product_id) in self.vendor_product_ids:
			if dev.idVendor == cheeky_vendor_id and dev.idProduct == cheeky_product_id:
				return True
		return False

	# -----------------------------

	def acquire_devices(self):

		device_found = False

		rocket_launchers = usb.core.find(find_all=True, custom_match = self.is_supported_device)
		for dev in rocket_launchers:
			logging.debug("vendorId=%02x, product_id=%02x\n", dev.idVendor, dev.idProduct)
			for i, (cheeky_vendor_id, cheeky_product_id) in enumerate(self.vendor_product_ids):
				if dev.idVendor == cheeky_vendor_id and dev.idProduct == cheeky_product_id:

					print "Located", self.housing_colors[i], "Rocket Launcher device."

					launcher = None
					if i == 0:
						launcher = OriginalRocketLauncher()
					elif i == 1:
						launcher = BlueRocketLauncher()
					elif i == 2:
	#							launcher = BlueRocketLauncher()	# EXPERIMENTAL
					
						return '''The '''+self.launcher_types[i]+''' ('''+self.housing_colors[i]+''') Rocket Launcher is not yet supported.  Try the '''+self.launcher_types[0]+''' or '''+self.launcher_types[1]+''' one.'''
					elif i == 3:
						launcher = BlackRocketLauncher()
					elif i == 4:
						launcher = GrayRocketLauncher()

					return_code = launcher.acquire( dev )
					if not return_code:
						self.launchers.append( launcher )
						device_found = True

					elif return_code == 2:
						print "Error"
						string = '''You don't have permission to operate the USB device.  To give
	yourself permission by default (in Ubuntu), create the file
	/etc/udev/rules.d/40-missilelauncher.rules with the following line:
	SUBSYSTEM=="usb", ENV{DEVTYPE}=="usb_device", ACTION=="add", SYSFS{idVendor}=="%04x", SYSFS{idProduct}=="%04x", GROUP="plugdev", MODE="0660"
	The .deb installer should have done this for you.  If you just installed
	the .deb, you need to unplug and replug the USB device now.  This will apply
	the new permissions from the .rules file.''' % (cheeky_vendor_id, cheeky_product_id)
						print string

						return '''You don't have permission to operate the USB device.
	If you just installed the .deb, you need to plug cycle the USB device now.  This will apply
	the new permissions from the .rules file.'''
					else:
						print "Something went wrong..."



		if not device_found:
			return 'No USB Rocket Launcher appears\nto be connected.'


# ============================================
# ============================================

class OriginalRocketLauncher:

	color_green = True
	has_laser = False

	green_directions = [1, 0, 2, 3, 4]

	def __init__(self):

		self.usb_debug = False

		self.previous_fire_state = False
		self.previous_limit_switch_states = [False]*4	# Down, Up, Left, Right

	# ------------------------------------------------------
	def acquire(self, dev):
		assert dev is not None
		
		'''
		if dev is None:
			print "device not found"
		else:
			print "device found"
		if dev.is_kernel_driver_active(0) is True:
			print "but we need to detach kernel driver"
		dev.detach_kernel_driver(0)
		print "claiming device"
		usb.util.claim_interface(dev, 0)
		
		
		print "release claimed interface"
		usb.util.release_interface(dev, 0)
		print "now attaching the kernel driver again"
		dev.attach_kernel_driver(0)
		print "all done"
		
		print "resetting device"
		dev.reset()
		print "device reset"'''
		# set the active configuration. With no arguments, the first
		# configuration will be the active one
		#dev.set_configuration()

		# get an endpoint instance
		self.handle = dev.open()
		#cfg = dev.get_active_configuration()
		#interface = cfg[(0,0)]
		#self.endpoint = interface[0]
		
		return 0

	# -----------------------------
	def issue_command(self, command_index):

		signal = 0
		if command_index >= 0:
			signal = 1 << command_index

		try:
			self.handle.controlMsg(0x21, 0x09, [signal], 0x0200)

		except usb.USBError:
			pass

	# -----------------------------
	def start_movement(self, command_index):
		self.issue_command( self.green_directions[command_index] )

	# -----------------------------
	def stop_movement(self):
		self.issue_command( -1 )

	# -----------------------------
	def check_limits(self):
		'''For the "green" rocket launcher, the MSB of byte 2 comes on when a rocket is ready to fire,
		and is cleared again shortly after the rocket fires and cylinder is charged further.'''

		bytes = self.handle.bulkRead(1, 8)


		if self.usb_debug:
			print "USB packet:", bytes


		limit_bytes = list(bytes)[0:2]
		self.previous_fire_state = limit_bytes[1] & (1 << 7)


		limit_signal = (limit_bytes[1] & 0x0F) | (limit_bytes[0] >> 6)

		new_limit_switch_states = [bool(limit_signal & (1 << i)) for i in range(4)]
		self.previous_limit_switch_states = new_limit_switch_states

		return new_limit_switch_states


# ============================================
# ============================================

class BlueRocketLauncher(OriginalRocketLauncher):

	color_green = False

	def __init__(self):
		OriginalRocketLauncher.__init__(self)

	# -----------------------------
	def start_movement(self, command_index):
		self.issue_command( command_index )

	# -----------------------------
	def stop_movement(self):
		self.issue_command( 5 )

	# -----------------------------
	def check_limits(self):

		'''For the "blue" rocket launcher, the firing bit is only toggled when the rocket fires, then
		is immediately reset.'''


		bytes = None
		self.issue_command( 6 )

		try:
			bytes = self.handle.bulkRead(1, 1)

		except usb.USBError, e:
			if e.message.find("No error") >= 0 \
			or e.message.find("could not claim interface") >= 0 \
			or e.message.find("Value too large") >= 0:

				pass
#				if self.usb_debug:
#					print "POLLING ERROR"

				# TODO: Should we try again in a loop?
			else:
				raise e


		if self.usb_debug:
			print "USB packet:", bytes

		self.previous_fire_state = bool(bytes)




		if bytes is None:
			return self.previous_limit_switch_states
		else:
			limit_signal, = bytes
			new_limit_switch_states = [bool(limit_signal & (1 << i)) for i in range(4)]

			self.previous_limit_switch_states = new_limit_switch_states
			return new_limit_switch_states



# ============================================
# ============================================

class BlackRocketLauncher(BlueRocketLauncher):

	striker_commands = [0xf, 0xe, 0xd, 0xc, 0xa, 0x14, 0xb]
	has_laser = True

	# -----------------------------
	def issue_command(self, command_index):

		signal = self.striker_commands[command_index]

		try:
			self.handle.controlMsg(0x21, 0x09, [signal, signal])

		except usb.USBError:
			pass

	# -----------------------------
	def check_limits(self):

		return self.previous_limit_switch_states



# ============================================
# ============================================

class GrayRocketLauncher(BlueRocketLauncher):

	striker_commands = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40]
	has_laser = False

	# -----------------------------
	def issue_command(self, command_index):

		signal = self.striker_commands[command_index]

		try:
			self.handle.controlMsg(0x21,0x09, [0x02, signal, 0x00,0x00,0x00,0x00,0x00,0x00])

		except usb.USBError:
			pass

	# -----------------------------
	def check_limits(self):

		return self.previous_limit_switch_states


