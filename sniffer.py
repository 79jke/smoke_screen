import scapy
from scapy.all import sniff
from scapy.all import AsyncSniffer

import numpy as np

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.lines import Line2D

from threading import Lock

import time

class Monitor(animation.TimedAnimation):
	def __init__(self, data_getter, interval=100, length=1024):
		self.length = length
		self.data_getter = data_getter

		self.fig = plt.figure(figsize=(12,18))
		self.ax_data = self.fig.add_subplot(2, 1, 1)
		self.ax_fft = self.fig.add_subplot(2, 1, 2)

		self.time = np.linspace(0, self.length, self.length)
		self.data = np.zeros(self.length)

		self.data_max = 0

		self.line_data = Line2D([], [], color='blue')
		self.ax_data.set_ylabel('data volume')
		self.ax_data.add_line(self.line_data)
		self.ax_data.set_xlim(0, self.length)

		self.line_fft = Line2D([], [], color='red')
		self.ax_fft.set_ylabel('fft')
		self.ax_fft.add_line(self.line_fft)
		self.ax_fft.set_xlim(0, self.length)
		self.ax_fft.set_ylim(-16, 16)

		animation.TimedAnimation.__init__(self, self.fig, interval=interval, blit=True)

	def _draw_frame(self, framedata):
		self.data = np.roll(self.data, -1)
		self.data[-1] = self.data_getter()

		if np.max(self.data) > self.data_max:
			self.data_max = int(np.max(self.data)) + 1
			self.ax_data.set_ylim(0, self.data_max * 1.1)
			self.fig.canvas.draw()

		fft_data = np.fft.fft(self.data / self.data_max)
		fft_data[0] = 0

		self.line_data.set_data(self.time, self.data)
		self.line_fft.set_data(self.time, fft_data)

		self._drawn_artists = [
			self.line_data,
			self.line_fft
		]

	def new_frame_seq(self):
		return iter(range(self.length))

	def _init_draw(self):
		lines = [
			self.line_data,
			self.line_fft
		]
		for l in lines:
			l.set_data([], [])

class Aggregator():
	def __init__(self):
		self.value = 0
		self.sniffer = None
		self.lock = Lock()

	def sniffer_callback(self, pkt):
		self.lock.acquire()
		self.value += len(pkt)
		self.lock.release()

	def sniffer_activate(self):
		self.sniffer = AsyncSniffer(prn=self.sniffer_callback)
		self.sniffer.start()

	def sniffer_deactivate(self):
		self.sniffer.stop()

	def flush(self):
		self.lock.acquire()
		res = self.value
		self.value = 0
		self.lock.release()
		return res


agg = Aggregator()
agg.sniffer_activate()

monitor = Monitor(data_getter=agg.flush, interval=10, length=4096)
plt.show()

agg.sniffer_deactivate()