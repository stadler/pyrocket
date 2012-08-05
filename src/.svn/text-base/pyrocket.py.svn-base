#!/usr/bin/python

'''PyGTK Missile Command

Author:	Karl Ostmo
Date:	January 21, 2008
E-mail:	kostmo [at-symbol] g m a i l [dotcom]
Web:	http://kostmo.ath.cx/

Provides a graphical interface for controlling the Dream Cheeky USB
Rocket Launcher.  Arrow keys control direction, in addition to GUI buttons. "f" is fire.
The program will also accept joystick control.

Tested under Ubuntu 8.04 (Hardy).  Requires: python-gtk2 python-pyusb python-pygame
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

