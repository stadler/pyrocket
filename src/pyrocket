#!/usr/bin/python

'''PyGTK Missile Command

Authors:	Karl Ostmo, Jacques Stadler
Inception Date:	January 21, 2008
E-mail:		jacques.stadler@gmail.com

Provides a graphical interface for controlling the Dream Cheeky USB
Rocket Launcher.  Arrow keys control direction, in addition to GUI buttons. "f" is fire.
The program will also accept joystick control.

Tested under Ubuntu 12.04 (Precise), 12.10 (Quantal).  
Requires: python-gtk2 python-pyusb python-pygame
'''

from rocket_frontend import RocketWindow

if __name__ == "__main__":

	import sys, os
	# This is for loading the images
	pathname = os.path.dirname(sys.argv[0])
	fullpath =  os.path.abspath(pathname)
	os.chdir(fullpath)

	launcher = RocketWindow()
	launcher.main()

