from threading import Thread
from time import sleep

STARTING_ALT = 'TODO'

SAFE_ALT_LOWER = 'TODO'
SAFE_ALT_UPPER = 'TODO'

class AvoidanceSystem:

	def __init__(self, plane):

		self.plane = plane

		self.active = False
		self.closed = False

		monitor_thread = Thread(target = _monitor_plane)
		thread.start()

	def _monitor_plane(self):

		count = 0

		while (count < 3):

			sleep(0.5)

			count = count + 1 if STARTING_ALT <= self.plane.loc.alt else 0

		while (not closed):

			if (active):

				#TODO

			sleep(0.1)

	def stop_monitoring(self):

		self.active = False

	def start_monitoring(self):

		self.active = True

	def close(self):

		self.closed = True
