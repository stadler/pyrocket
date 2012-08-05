#!/usr/bin/python

from pygtk import require
require('2.0')
import gtk, gobject

# ==============================================================================
# ==============================================================================

from rocket_backend import RocketManager
from rocket_webcam import VideoWindow
from rocket_joystick import StatefulJoystick

class RocketWindow:

	appname = "pyrocket"
	version = "0.7"
	local_share_dir = "/usr/share/"

	keymap = [65364, 65362, 65361, 65363]
	button_labels = ["Down", "Up", "Left", "Right", "_Fire"]
	button_stock_icons = [gtk.STOCK_GO_DOWN, gtk.STOCK_GO_UP, gtk.STOCK_GO_BACK, gtk.STOCK_GO_FORWARD, gtk.STOCK_DIALOG_WARNING]

	status_message_timeout = 5000

	PRECHARGE = 1
	CONTINUOUS_CHARGE = 2

	# ===============================

	def __init__(self, run_installed=True):

		self.joystick_state = StatefulJoystick()
#		self.joystick_state = None

		self.run_installed = run_installed

		self.img_path = ""
		self.doc_path = ""
		if run_installed:
			self.img_path = self.local_share_dir + self.appname + "/"
			self.doc_path = self.local_share_dir + "doc/" + self.appname + "/"

		self.status_message_list = [
			"ALT+arrowkeys move!",
#			"Supports "+RocketManager.launcher_types[0]+" and "+RocketManager.launcher_types[1]+" Launcher!"
			"Supports Striker II and Dream Cheeky Models!"
		]


		# create a new window
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
#		self.window.set_title(u"Dream Cheeky\u0099 Control")	# The "TM" symbol doesn't work in GNOME
#		self.window.set_title(u"Dream Cheeky\u00AE Control")
		self.window.set_title("USB Rocket Launcher Control")

		icon_path = self.img_path + "pyrocket.png"
		self.window.set_icon_from_file( icon_path )
		self.status_icon = gtk.status_icon_new_from_file( icon_path )
		self.status_icon.set_visible( True )

		self.window.set_resizable( False )
		self.window.connect("delete_event", self.delete_event)
		self.window.connect("key_press_event", self.handle_keyboard_press_event)
		self.window.connect("key_release_event", self.handle_keyboard_release_event)
		self.window.set_events(gtk.gdk.KEY_PRESS_MASK | gtk.gdk.KEY_RELEASE_MASK)

		self.window.connect("destroy", self.destroy)


		self.button_array = []
		for i, label in enumerate(self.button_labels):
			button = gtk.Button(label)
			button.set_use_underline(True)
			button_image = gtk.Image()
			button_image.set_from_stock(self.button_stock_icons[i], gtk.ICON_SIZE_BUTTON)
			button.set_image(button_image)
			self.button_array.append( button )


		vbox = gtk.VBox(False, 5)
		self.window.add(vbox)

		# ----------------------------

		top_menu = gtk.MenuBar()
		vbox.pack_start(top_menu, False, False)


		view_menu = gtk.MenuItem("_View")
		view_submenu = gtk.Menu()
		view_menu.set_submenu( view_submenu )
		self.camera_widget_visible = gtk.CheckMenuItem("Camera")
		self.camera_widget_visible.connect("toggled", self.cb_toggle_show_camera)
		view_submenu.append( self.camera_widget_visible )

		top_menu.append( view_menu )


		help_menu = gtk.MenuItem("_Application")
		help_submenu = gtk.Menu()
		help_menu.set_submenu( help_submenu )
		about_item = gtk.MenuItem("_About")
		about_item.connect("activate", self.cb_about_dialog)
		help_submenu.append( about_item )

		quit_item = gtk.MenuItem("_Quit")
		quit_item.connect("activate", self.destroy)
		help_submenu.append( quit_item )

		top_menu.append( help_menu )

		# ----------------------------

		self.video = VideoWindow()
		self.video.set_no_show_all(True)
		vbox.pack_start(self.video, False, False)

		# ----------------------------

		self.joystick_hbox = gtk.HBox(False, 5)
		vbox.pack_start(self.joystick_hbox, False, False)

		joystick_image = gtk.Image()
		joystick_image.set_from_file(self.img_path + "joystick.svg")
		self.joystick_hbox.pack_start(joystick_image, False, False)
		mini_joystick_vbox = gtk.VBox(False, 0)
		mini_joystick_vbox.pack_start(gtk.Label("Joystick detected:"), False, False)
		self.joystick_name_label = gtk.Label("")
		mini_joystick_vbox.pack_start(self.joystick_name_label, False, False)
		self.joystick_hbox.pack_start(mini_joystick_vbox, False, False)

		self.joystick_hbox.set_no_show_all(True)


		if self.joystick_state:
			if not self.joystick_state.joystick_init():
				self.status_message_list.append("Try connecting a Joystick!")
			else:
				self.joystick_hbox.set_no_show_all(False)	# huh?
				self.joystick_hbox.show_all()
				self.joystick_name_label.set_text( self.joystick_state.joystick_object.get_name() )
				print 'Joystick has %d axes and %d buttons' %(self.joystick_state.num_axes, self.joystick_state.num_buttons)



		# ----------------------------        
		control_hbox = gtk.HBox(False, 5)
		vbox.pack_start(control_hbox, False, False)
		control_hbox.pack_start(gtk.Label("Launcher ID:"), False, False)

		myadj = gtk.Adjustment(1, 0, 16, 1)
		self.laucher_id = gtk.SpinButton(myadj, 0, 0)
		self.laucher_id.set_numeric(True)
		self.laucher_id.connect("value-changed", self.cb_select_new_launcher)
		control_hbox.pack_start(self.laucher_id, False, False)

		self.limit_override = gtk.CheckButton("Override Limits")
		self.limit_override.connect("toggled", self.cb_limit_override)
		control_hbox.pack_end(self.limit_override, True, False)


		main_hbox = gtk.HBox(True, 5)
		vbox.pack_start(main_hbox, False, False)

		for button in self.button_array[:4]:
			main_hbox.pack_start(button, True, True)


		charging_options_hbox = gtk.HBox(False, 5)
		vbox.pack_start(charging_options_hbox, False, False)

		self.button_array[4].set_tooltip_text("Let 'er rip!")
		charging_options_hbox.pack_start(self.button_array[4], False, False)

		sub_vbox = gtk.VBox(False, 5)
		charging_options_hbox.pack_start(sub_vbox, True, True)

		charge_options = gtk.RadioButton(group=None, label="Charge Continuously")
		sub_vbox.pack_start(charge_options, False, False)

		charge_options = gtk.RadioButton(group=charge_options, label="Precharge (for sneak attacks)")
		sub_vbox.pack_start(charge_options, False, False)
		self.stop_charge = gtk.RadioButton(group=charge_options, label="Fire once")
		self.stop_charge.set_active(True)
		sub_vbox.pack_start(self.stop_charge, False, False)




		self.toggle_laser_button = gtk.Button("Toggle _Laser")
		self.toggle_laser_button.set_use_underline(True)
		button_image = gtk.Image()
		button_image.set_from_stock(gtk.STOCK_MEDIA_RECORD, gtk.ICON_SIZE_BUTTON)
		self.toggle_laser_button.set_image(button_image)
		vbox.pack_start(self.toggle_laser_button, False, False)
		




		self.status_bar = gtk.Statusbar()
		self.status_bar.set_has_resize_grip(False)
		vbox.pack_start(self.status_bar, False, False)
	



		self.window.show_all()

		self.connect_everything()
		self.cb_select_new_launcher(self.laucher_id)


		self.status_message_index = 1
		self.last_message_id = None
		self.cycle_status_message()

		gobject.idle_add( self.limit_checker_loop )

	# ===============================

	def cb_toggle_show_camera(self, widget):
		if widget.get_active():

			self.video.start_video()

			self.video.show()
			self.video.video_enabled_button.set_active(True)
		else:
			self.video.video_enabled_button.set_active(False)
			self.video.hide()

			self.video.stop_capture()

	# ===============================

	def cb_about_dialog(self, widget):

		about_dialog = gtk.AboutDialog()
		about_dialog.set_transient_for(self.window)
		about_dialog.set_version( self.version )
		about_dialog.set_logo( gtk.gdk.pixbuf_new_from_file(self.img_path + "msnmissile.png") )
		about_dialog.set_copyright(u"\u00A92008 Karl Ostmo")

		if self.run_installed:
			license_file = open(self.doc_path + "copyright", "r")
		else:
			license_file = open("debian/copyright", "r")

		about_dialog.set_license( license_file.read() )
		license_file.close()

		about_dialog.set_authors(["Karl Ostmo"])
		about_dialog.set_website("http://pyrocket.googlecode.com/")

		about_dialog.run()
		about_dialog.destroy()

	# ===============================

	def cb_limit_override(self, widget):
		if widget.get_active():
			for button in self.button_array[:4]:
				button.set_sensitive(True)

		else:
			launcher = self.get_active_launcher()

			for i, state in enumerate( launcher.check_limits() ):
				self.button_array[i].set_sensitive( not state )


	# ===============================

	def cb_select_new_launcher(self, widget):

		if len(self.rocket_controller.launchers):
			launcher = self.rocket_controller.launchers[widget.get_value_as_int()]
		else:
			return

		self.stop_charge.get_group()[self.PRECHARGE].set_sensitive( launcher.color_green )
		self.limit_override.set_sensitive( launcher.color_green )


		for i, state in enumerate( launcher.check_limits() ):
			self.button_array[i].set_sensitive( not state )

		if launcher.has_laser:
			self.toggle_laser_button.show()
		else:
			self.toggle_laser_button.hide()

	# ===============================

	def cycle_status_message(self):
		'''All this junk keeps the message stack from ever-increasing.  The Statusbar
		widget won't allow a message_id to be zero, so we have to shift the indices up by one.'''

		saved_id = self.last_message_id
		new_msg_text = self.status_message_list[(self.status_message_index-1) % len(self.status_message_list)]
		self.last_message_id = self.status_bar.push(0, new_msg_text)

		if not saved_id is None:
			self.status_bar.remove_message(saved_id, (self.status_message_index-1) % len(self.status_message_list) + 1)
		self.status_message_index += 1
		gobject.timeout_add( self.status_message_timeout, self.cycle_status_message)

	# ===============================

	def handle_keyboard_press_event(self, widget, event):

		try:
			if event.state & gtk.gdk.MOD1_MASK:
				idx = self.keymap.index( event.keyval )
#				print "Key pressed:", idx


#				self.cb_fire_click(widget)
				self.cb_button_press(None, idx)

		except ValueError:
			pass

	# ===============================

	def handle_keyboard_release_event(self, widget, event):

		try:
			if event.state & gtk.gdk.MOD1_MASK:
				idx = self.keymap.index( event.keyval )
#				print "Key released:", idx

				self.cb_button_release(None, idx)

		except ValueError:
			pass

	# ===============================

	def get_active_launcher(self):
		if len(self.rocket_controller.launchers):
			return self.rocket_controller.launchers[self.laucher_id.get_value_as_int()]

	# ===============================

	def cb_fire_click(self, widget):

		if not self.stop_charge.get_group()[self.CONTINUOUS_CHARGE].get_active():
			launcher = self.get_active_launcher()
			launcher.start_movement(4)

	# ===============================

	def cb_laser_click(self, widget):

		launcher = self.get_active_launcher()
		launcher.start_movement(6)

	# ===============================

	def movement_wrapper(self, direction):

		launcher = self.get_active_launcher()

		if direction == 5:
			launcher.stop_movement()
			return False

		if direction == 4 or not (launcher.previous_limit_switch_states[direction] and not self.limit_override.get_active()):
			launcher.start_movement(direction)

			if direction == 4:
				return self.stop_charge.get_group()[self.CONTINUOUS_CHARGE].get_active()

			return True
		return False

	# ===============================

	def get_fire_mode(self):
		for idx, radio_button in enumerate(self.stop_charge.get_group()):
			if radio_button.get_active():
				return idx

	# ===============================

	def cb_button_press(self, widget, button_index):

		if button_index == 4 and self.stop_charge.get_group()[self.CONTINUOUS_CHARGE].get_active():
			launcher = self.get_active_launcher()
			launcher.start_movement(4)

		elif button_index != 4:
			self.movement_wrapper(button_index)

	# ===============================

	def cb_button_release(self, widget, button_index):

		launcher = self.get_active_launcher()

		if button_index != 4 or button_index == 4 and self.stop_charge.get_group()[self.CONTINUOUS_CHARGE].get_active():
			launcher.stop_movement()

	# ===============================

	def connect_everything(self):

		self.rocket_controller = RocketManager()
	
		err_msg = self.rocket_controller.acquire_devices()
		if err_msg:
			dia = gtk.Dialog('Device Acquisition error',
				  self.window.get_toplevel(),  #the toplevel wgt of your app
				  gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,  #binary flags or'd together
				  ("Ignore", 77, gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE))

			v = gtk.VBox()
			v.pack_start(gtk.Label(err_msg), False, False)
			v.set_border_width(10)
			dia.vbox.pack_start( v )
			dia.show_all()
			result = dia.run()
			if result == 77:
				print "Continuing anyway."
			elif result == gtk.RESPONSE_CLOSE:
				exit(0)
			else:
				print "Exited abnormally."
				exit(1)
			dia.destroy()


		self.laucher_id.set_range(0, len(self.rocket_controller.launchers) - 1 )


		for i, button in enumerate(self.button_array):

			# Experimental
			button.connect("pressed", self.cb_button_press, i)
			button.connect("released", self.cb_button_release, i)

		button = self.button_array[4]
		button.connect("clicked", self.cb_fire_click)

		self.toggle_laser_button.connect("clicked", self.cb_laser_click)

	# ===============================

	def limit_checker_loop(self):

		launcher = self.get_active_launcher()
		if not launcher:
			return False

		prev_states = launcher.previous_limit_switch_states
		prev_fire_state = launcher.previous_fire_state
		new_states = launcher.check_limits()
		next_fire_state = launcher.previous_fire_state

		if not self.limit_override.get_active():

			for i in range(len(new_states)):
				if new_states[i] ^ prev_states[i]:
					self.button_array[i].set_sensitive(not new_states[i])

					if new_states[i]:	# For stopping the joystick movement
						launcher.stop_movement()

		# Terminate cylinder charging based on radio state
		grp = self.stop_charge.get_group()
		if len(grp) > 0 and grp[0].get_active():
			if prev_fire_state and not next_fire_state:
				launcher.stop_movement()
		elif len(grp) > 1 and grp[1].get_active():
			if not prev_fire_state and next_fire_state:
				launcher.stop_movement()

		return True

	# ===============================

	def main(self):
		# All PyGTK applications must have a gtk.main(). Control ends here
		# and waits for an event to occur (like a key press or mouse event).
		gtk.main()

	# ===============================

	def delete_event(self, widget, event, data=None):

		# Change FALSE to TRUE and the main window will not be destroyed
		# with a "delete_event".
		return False

	# ===============================

	def destroy(self, widget, data=None):

		if self.video:
			self.video.stop_capture()

		if self.joystick_state and self.joystick_state.joystick_object:
			self.joystick_state.joystick_object.quit()


		for launcher in self.rocket_controller.launchers:
			launcher.stop_movement()

		gtk.main_quit()

	# ===============================

if __name__ == "__main__":

	import sys, os
	# This is for loading the images
	pathname = os.path.dirname(sys.argv[0])
	fullpath =  os.path.abspath(pathname)
	os.chdir(fullpath)

	launcher = RocketWindow(False)
	launcher.main()

