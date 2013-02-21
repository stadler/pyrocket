#!/usr/bin/python

if __name__ == "__main__":

	from distutils.core import setup

	setup(name="pyrocket",
		description="control Striker II and Dream Cheeky USB Missile Launchers",
		long_description="""pyrocket is used to operate USB foam dart launchers. It supports many models,
and for some, has considerably more functionality than the drivers provided by
the manufacturer. One may find it useful as a starting point for controlling
other USB devices, or simply for waging cubicle warfare.

pyrocket automatically detects the launcher(s) and a joystick, and a video
window is provided for webcam-enabled devices. pyrocket currently supports the
"circus cannon", "original" and "webcam" USB Missile Launchers sold by Dream
Cheeky, as well as the Striker II USB Laser Guided Missile Launcher marketed
by Ninja Gizmos.""",
		author="Karl Ostmo",
		author_email="kostmo@gmail.com",
		maintainer="Jacques Stadler",
		maintainer_email="jacques.stadler@gmail.com",
		url="https://github.com/stadler/pyrocket",
		version="0.8",
		py_modules=["rocket_backend", "rocket_frontend", "rocket_webcam", "rocket_joystick"],
		scripts=["pyrocket"],
		data_files=[("share/pyrocket", ["joystick.svg", "pyrocket.png", "msnmissile.png"])]
	)

# ====================================================

def make_rules_file():

	from rocket_backend import RocketControl

	filename = "40-rocketlauncher.rules"
	file_handle = open(filename, "w")

	for ids in RocketControl.vendor_product_ids:
		file_handle.write( 'SUBSYSTEM=="usb", ENV{DEVTYPE}=="usb_device", ACTION=="add", SYSFS{idVendor}=="%04x", SYSFS{idProduct}=="%04x", GROUP="plugdev", MODE="0660"\n' % ids )

	file_handle.close()

