
# PiFace - PlexMediaServer Control
#
# Default Output:
# 	Server - Active/Down
#	Uptime - Time in hh:mm
#	... Possibly more information ...
#
# Switch Inputs:
#	S0 - Reboot RPi
#	S1 - Clean Restart PlexMediaServer

__author__ = "JP"


import pifacecad
import subprocess
import threading
import time
import sys
import os


# Function to execute shell commands
def execute_shell_cmd(cmd):
	process = subprocess.Popen(cmd,
			stdout=subprocess.PIPE, universal_newlines=True)

	while True:
		return_code = process.poll()
		if return_code is not None:
			# print("RETURN CODE", return_code)
			return process


# Plex CAD class
class PlexCAD(object):
	def __init__(self, cad, refresh_interval=60):
		# Initializing private members
		self.refresh_interval = refresh_interval
		self.timer = threading.Timer(self.refresh_interval, self.update_display)
		self.cad = cad
		self.status_down_detected = False
		self.latest_uptime = " "				# "Uptime- xh:ym"

		# Constructor methods
		self.update_display()
		self.cad.lcd.backlight_on()				# Adjust display params
		self.cad.lcd.blink_off()
		self.cad.lcd.cursor_off()


	# Destructor
	def fini(self):
		if self.timer is not None:
			self.timer.cancel()
		self.cad.lcd.clear()


	# Get CAD
	def get_cad(self):
		return self.cad


	# Get latest uptime
	def get_latest_uptime(self):
		return self.latest_uptime


	# Get status down detected
	def get_status_down_detected(self):
		return self.status_down_detected


	# Get status of the PlexMediaServer
	def get_PlexMediaServer_status(self):
		status = "Down!"

		if self.get_status_down_detected() is False:
			cmd, buffer = ["pidof", "Plex Media Server"], []
			process = execute_shell_cmd(cmd)

			for output in process.stdout.readlines():
				buffer.append(output.strip())

			if len(buffer) != 0:
				status = "Active"
			else:
				status = "Down!"
				self.status_down_detected = True

		return "Status- " + status


	# Get RPi uptime
	def get_uptime(self):
		cmd, buffer = ["uptime", "-p"], []
		process = execute_shell_cmd(cmd)

		for output in process.stdout.readlines():
			buffer.append(output.strip())

		tmp = str(buffer[0])

		tmp1 = tmp.replace("up", "Uptime-")

		if "hours" in tmp1:
			tmp2 = tmp1.replace(" hours", "h")
		elif "hour" in tmp1:
			tmp2 = tmp1.replace(" hour", "h")
		else:
			tmp2 = tmp1

		tmp3 = tmp2.replace(", ", ":")

		if "minutes" in tmp3:
			uptime = tmp3.replace(" minutes", "m")
		elif "minute" in tmp3:
			uptime = tmp3.replace(" minute", "m")

		return uptime


	# Set uptime
	def set_uptime(self, uptime):
		self.uptime = uptime


	# Set status down detected
	def set_status_down_detected(self, is_detected):
		self.status_down_detected = is_detected


	# Function to update display
	def update_display(self):
		# Clear LCD
		cad.lcd.clear()

		# Display status of PlexMediaServer
		status = self.get_PlexMediaServer_status()
		cad.lcd.write(status)

		# Adjust cursor at 1st column (0), 2nd row (1)
		cad.lcd.set_cursor(0, 1)

		# Display RPi Uptime
		uptime = self.get_uptime()
		cad.lcd.write(uptime)
		self.set_uptime(uptime)

		# Restart timer
		self.restart_timer()


	# Function to restart timer
	def restart_timer(self):
		self.timer = threading.Timer(self.refresh_interval, self.update_display)
		self.timer.start()


	# Function to reboot RPi
	def reboot_RPi(self):
		# TODO: Add this file to startup
		os.system('sudo reboot')


	# Function to clean restart PlexMediaServer
	def clean_restart_PlexMediaServer(self):
		cmd = ["Execute the manual restart file"]
		process = execute_shell_cmd(cmd)


	# Function to process switch inputs
	def process_switch_input(self, event):
		print("yay")
		switch = event.pin_num
		cad = event.chip
		print("Pressed Switch: %d", switch)

		if switch == 0:
			cad.lcd.write("Reboot RPi")
	#		reboot_RPi()
		elif switch == 1:
			cad.lcd.write("Restart Server")
#			clean_restart_PlexMediaServer()
		elif switch == 2:
			pass
		elif switch == 3:
			pass
		elif switch == 4:
			cad.lcd.write("Exit PiFace")
		elif switch == 5:
			pass
		elif switch == 6:
			pass
		else:
			pass
		time.sleep(1)


if __name__ == "__main__":
	PY3 = sys.version_info[0] >= 3
	if not PY3:
		print("Please execute using python3")
		sys.exit(1)

	try:
		# Multi-threading
		# This sequence is exited when '2' threads call barrier.wait()
		# First call happens after the switch_listener.activate()
		# listener is not sentient to deactivate itself, so assigning a switch (4)
		# When the cb func of that switch is handled, the second call to barrier.wait()
		# occurs, thereby ending the program.
		barrier = threading.Barrier(2)

		# Create an instance of CAD (Control And Display)
		cad = pifacecad.PiFaceCAD()

		# Create an instance of the Plex CAD class
		plexCad = PlexCAD(cad, 60)		# Refresh interval = 60sec

		# Create a listener (registered callback) for inputs from ALL switches
		switch_listener = pifacecad.SwitchEventListener(chip=plexCad.get_cad())

		application_switches = [0, 1, 2, 3, 5, 6, 7]
		for switch in application_switches:
			switch_listener.register(switch, pifacecad.IODIR_ON, plexCad.process_switch_input)
		switch_listener.register(4, pifacecad.IODIR_ON, barrier.wait)

		switch_listener.activate()

		# Debug
#		print("GPIO interrupts : ", str(cad.gpintena.value)) #255 == enabled
#		print("Switchport : ", cad.switch_port.value)
#		for i in range(8):
#			print("Switch ", i, ": ", cad.switches[i].value)

# TRY TO USE PORT EVENT LISTENER DIRECTLY...

		barrier.wait()				# Wait until exit

		# Exit sequence
		print("Exit sequence")
		plexCad.fini()
		switch_listener.deactivate()

	except KeyboardInterrupt:
		print("Cleanup sequence")
		plexCad.fini()
		switch_listener.deactivate()
		sys.exit(0)
