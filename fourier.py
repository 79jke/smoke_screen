import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.animation as animation

class FourierAnimation(animation.TimedAnimation):
	def __init__(self):
		self.length = 1024

		fig = plt.figure(figsize=(12,18))

		ax_data = fig.add_subplot(2, 3, 1)
		ax_noise = fig.add_subplot(2, 3, 2)
		ax_sum = fig.add_subplot(2, 3, 3)

		ax_fft_data = fig.add_subplot(2, 3, 4)
		ax_fft_noise = fig.add_subplot(2, 3, 5)
		ax_fft_sum = fig.add_subplot(2, 3, 6)
		
		data_lim = 6
		freq_lim = 256

		self.time = np.linspace(0, self.length, self.length)
		self.generator = abs(np.random.rand(self.length) + np.sin(2 * np.pi * self.time / 10.))
		
		self.data = np.zeros(self.length)
		self.noise = np.zeros(self.length)

		self.line_data = Line2D([], [], color='blue')
		ax_data.set_ylabel('data')
		ax_data.add_line(self.line_data)
		ax_data.set_xlim(0, self.length)
		ax_data.set_ylim(0, data_lim)

		self.line_noise = Line2D([], [], color='green')
		ax_noise.set_ylabel('noise')
		ax_noise.add_line(self.line_noise)
		ax_noise.set_xlim(0, self.length)
		ax_noise.set_ylim(0, data_lim)

		self.line_sum = Line2D([], [], color='purple')
		ax_sum.set_ylabel('sum')
		ax_sum.add_line(self.line_sum)
		ax_sum.set_xlim(0, self.length)
		ax_sum.set_ylim(0, data_lim)

		self.line_fft_data = Line2D([], [], color='red')
		ax_fft_data.set_ylabel('fft data')
		ax_fft_data.add_line(self.line_fft_data)
		ax_fft_data.set_xlim(0, self.length)
		ax_fft_data.set_ylim(-1 * freq_lim, freq_lim)

		self.line_fft_noise = Line2D([], [], color='orange')
		ax_fft_noise.set_ylabel('fft spikes')
		ax_fft_noise.add_line(self.line_fft_noise)
		ax_fft_noise.set_xlim(0, self.length)
		ax_fft_noise.set_ylim(-1 * freq_lim, freq_lim)

		self.line_fft_sum = Line2D([], [], color='brown')
		ax_fft_sum.set_ylabel('fft sum')
		ax_fft_sum.add_line(self.line_fft_sum)
		ax_fft_sum.set_xlim(0, self.length)
		ax_fft_sum.set_ylim(-1 * freq_lim, freq_lim)

		animation.TimedAnimation.__init__(self, fig, interval=50, blit=True)

	def _draw_frame(self, framedata):
		self.data = np.roll(self.data, -1)
		self.generator = np.roll(self.generator, -1)
		self.noise = np.roll(self.noise, -1)

		self.data[-1] = self.generator[-1]

		fft_data = np.fft.fft(self.data)
		fft_data[0] = 0
		
		fft_spikes = fft_data.copy()
		fft_spikes[abs(fft_spikes) < np.amax(fft_spikes) * 0.9] = 0 

		noise_raw = -1 * np.fft.ifft(fft_spikes)
		noise_raw -= np.min(noise_raw)

		self.noise[-1] = noise_raw[-1]

		sum_noise_data = self.data + self.noise
		
		fft_sum = np.fft.fft(sum_noise_data)
		fft_sum[0] = 0

		self.line_data.set_data(self.time, self.data)
		self.line_noise.set_data(self.time, self.noise)
		self.line_sum.set_data(self.time, sum_noise_data)
		self.line_fft_data.set_data(self.time, fft_data)
		self.line_fft_noise.set_data(self.time, fft_spikes)
		self.line_fft_sum.set_data(self.time, fft_sum)

		self._drawn_artists = [
			self.line_data, 
			self.line_noise, 
			self.line_sum, 
			self.line_fft_data, 
			self.line_fft_noise, 
			self.line_fft_sum
		]

	def new_frame_seq(self):
		return iter(range(self.length))

	def _init_draw(self):
		lines = [
			self.line_data, 
			self.line_noise, 
			self.line_sum, 
			self.line_fft_data, 
			self.line_fft_noise, 
			self.line_fft_sum
		]
		for l in lines:
			l.set_data([], [])

ani = FourierAnimation()

plt.show()