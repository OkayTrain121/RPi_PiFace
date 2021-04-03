
# PiFace - PlexMediaServer Control
#
# Default Output:
# 	Server - Active/Down
#	Uptime - Time in hh:mm
#	... Possibly more information ...
#
# Switch Inputs:
#	S0 - <Not Configurable>
#	S1 - Reboot RPi
#	S2 - Clean Restart PlexMediaServer
#	S3 - Display IP Addresses
#	S4 - Display Memory Stats
#	S5 - <Exit PiFace>
#	S6 - <No Action>
#	S7 - <No Action>

__author__ = "JP"


import pifacecad
import subprocess
import threading
import time
import sys
import os


LOG_ENABLED = True


# Function to log flow
def logger(str):
	if LOG_ENABLED is True:
		print(str)


# Function to execute shell commands
def execute_shell_cmd(cmd):
	process = subprocess.Popen(cmd,
			stdout=subprocess.PIPE, universal_newlines=True)

	while True:
		return_code = process.poll()
		if return_code is not None:
			logger("RETURN CODE : " + str(return_code))
			return process


# Plex CAD class
class PlexCAD(object):
	def __init__(self, cad, refresh_interval=60, listener=None):
		# Initializing private members				# Default = 1min
		self.refresh_interval = refresh_interval
		self.timer = threading.Timer(self.refresh_interval, self.update_display)
		self.cad = cad
		self.listener = listener				# SwitchListener obj
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


	# Get listener object
	def get_listener(self):
		return self.listener


	# Get latest uptime
	def get_latest_uptime(self):
		return self.latest_uptime


	# Get status of the PlexMediaServer
	def get_PlexMediaServer_status(self):
		cmd, buffer = ["pidof", "Plex Media Server"], []
		process = execute_shell_cmd(cmd)
		for output in process.stdout.readlines():
			buffer.append(output.strip())

		if len(buffer) != 0:
			status = "Active"
		else:
			status = "Down!"

		return "Status- " + status


	# Get RPi uptime
	def get_uptime(self):
		cmd, buffer = ["uptime", "-p"], []
		process = execute_shell_cmd(cmd)
		for output in process.stdout.readlines():
			buffer.append(output.strip())

		tmp = str(buffer[0])

		tmp1 = tmp.replace("up", "Uptime-")

		tmp2 = tmp1
		if "hours" in tmp1:
			tmp2 = tmp1.replace(" hours", "h")
		elif "hour" in tmp1:
			tmp2 = tmp1.replace(" hour", "h")
		else:
			tmp2 = tmp1

		tmp3 = tmp2.replace(", ", ":")

		uptime = tmp3
		if "minutes" in tmp3:
			uptime = tmp3.replace(" minutes", "m")
		elif "minute" in tmp3:
			uptime = tmp3.replace(" minute", "m")

		return uptime


	# Set uptime
	def set_uptime(self, uptime):
		self.uptime = uptime


	# Set listener object
	def set_listener(self, listener):
		self.listener = listener


	# Set status down detected
	def set_status_down_detected(self, is_detected):
		self.status_down_detected = is_detected


	# Function to update display
	def update_display(self):
		self.get_cad().lcd.clear()

		# Display status of PlexMediaServer
		status = self.get_PlexMediaServer_status()
		self.get_cad().lcd.write(status)

		# Adjust cursor at 1st column (0), 2nd row (1)
		self.get_cad().lcd.set_cursor(0, 1)

		# Display RPi Uptime
		uptime = self.get_uptime()
		self.get_cad().lcd.write(uptime)
		self.set_uptime(uptime)

		# Restart timer
		self.restart_timer()


	# Function to restart timer
	def restart_timer(self):
		self.timer.cancel()
		self.timer = threading.Timer(self.refresh_interval, self.update_display)
		self.timer.start()


	# Function to reboot RPi
	def reboot_RPi(self):
		# TODO: Add this file to startup
		self.get_cad().lcd.clear()
		self.get_cad().lcd.write("Rebooting\n..please wait..")
		self.get_listener().deactivate()
		self.fini()
		os.system('sudo reboot')


	# Function to clean restart PlexMediaServer
	def clean_restart_PlexMediaServer(self):
		self.get_cad().lcd.clear()
		self.get_cad().lcd.write("Restarting\nPlexMediaServer")

		# Kill any running scripts
		raw = "sudo pkill -f -9 'manualRestartAllNoWatch'"  # Not working quite well
		cmd = []
		for token in raw.split():
			cmd.append(token)
			logger(token)
		process = execute_shell_cmd(cmd)

		# Rerun script
		raw = "/bin/bash /home/pi/Desktop/PlexAutomation/manualRestartAllNoWatch.sh"
		cmd = []
		for token in raw.split():
			cmd.append(token)
			logger(token)
		process = execute_shell_cmd(cmd)


	# Function to display IPv4 Addresses
	def display_ipv4_addresses(self):
		self.get_cad().lcd.clear()
		self.get_cad().lcd.write("Fetching\nIP Address")
		time.sleep(1)

		# Fetch private IPv4 Address
		raw = "hostname --all-ip-addresses"
		cmd, buffer = [], []
		for token in raw.split(" "):
			cmd.append(token)
			logger(token)
		process = execute_shell_cmd(cmd)
		for output in process.stdout.readlines():
			buffer.append(output.strip())

		all_ips = buffer[0].split()
		ipv4_private = all_ips[0]
		logger("IPv4 Private : " + str(ipv4_private))

		# Fetch public IPv4 Address
		raw = "dig +short myip.opendns.com @resolver1.opendns.com"
		cmd, buffer = [], []
		for token in raw.split(" "):
			cmd.append(token)
			logger(token)
		process = execute_shell_cmd(cmd)
		for output in process.stdout.readlines():
			buffer.append(output.strip())

		ipv4_public = buffer[0]
		logger("IPv4 Public : " + str(ipv4_public))

		self.get_cad().lcd.clear()
		self.get_cad().lcd.write(ipv4_public)
		self.get_cad().lcd.set_cursor(0, 1)
		self.get_cad().lcd.write(ipv4_private)


	# Function to display memory stats
	def display_memory_stats(self):
		self.get_cad().lcd.clear()
		self.get_cad().lcd.write("Fetching\nMemory Stats")
		time.sleep(1)

		cmd, buffer = ["free", "-m"], []
		process = execute_shell_cmd(cmd)
		for output in process.stdout.readlines():
			buffer.append(output.strip())

		memory = buffer[1].split()
		memory_used = memory[2]
		memory_available = memory[3]
		logger("Used : " + str(memory_used))
		logger("Available : " + str(memory_available))

		self.get_cad().lcd.clear()
		self.get_cad().lcd.write("Used  : " + str(memory_used) + " MB")
		self.get_cad().lcd.set_cursor(0, 1)
		self.get_cad().lcd.write("Avail : " + str(memory_available) + " MB")


	# Function to process switch inputs
	def process_switch_input(self, event):
		switch = event.pin_num
		logger("Pressed Switch : " + str(switch))

		if switch == 0:
			pass
		elif switch == 1:
			self.reboot_RPi()
		elif switch == 2:
			self.clean_restart_PlexMediaServer()
		elif switch == 3:
			self.display_ipv4_addresses()
		elif switch == 4:
			self.display_memory_stats()
#		elif switch == 5:
#			pass
		elif switch == 6:
			self.get_cad().lcd.clear()
			self.get_cad().lcd.write("Switch\nUnsupported")
			time.sleep(1)
		elif switch == 7:
			self.get_cad().lcd.clear()
			self.get_cad().lcd.write("Switch\nUnsupported")
			time.sleep(1)
		else:
			self.get_cad().lcd.clear()
			self.get_cad().lcd.write("Switch\nUnsupported")
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
		plexCad = PlexCAD(cad, 30)		# Refresh interval = 30sec

		# Create a listener (registered callback) for inputs from ALL switches
		switch_listener = pifacecad.SwitchEventListener(chip=plexCad.get_cad())

		application_switches = [0, 1, 2, 3, 4, 6, 7]
		for switch in application_switches:
			switch_listener.register(switch, pifacecad.IODIR_ON, plexCad.process_switch_input)
		switch_listener.register(5, pifacecad.IODIR_ON, barrier.wait)

		switch_listener.activate()
		barrier.wait()				# Wait until exit

		# Exit sequence
		plexCad.get_cad().lcd.write("Exit\nSequence")
		time.sleep(1)
		plexCad.fini()
		switch_listener.deactivate()
		sys.exit(0)

	except KeyboardInterrupt:
		plexCad.get_cad().lcd.write("Cleanup\nSequence")
		time.sleep(1)
		plexCad.fini()
		switch_listener.deactivate()
		sys.exit(0)

