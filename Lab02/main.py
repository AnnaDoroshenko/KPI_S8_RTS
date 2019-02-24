import numpy as np
import matplotlib.pyplot as plt
import random
import time


SCALE = 1024
HARMONICS = 8
FREQUENCY = 1200
STEP = FREQUENCY / HARMONICS


# class Harmonic:
#     def __init__(self, frequency, scale):
#         self.amplitude = random.uniform(0.0, 1.0)
#         self.phase = random.uniform(0.0, 2*np.pi)
#         current_xs = [0 for _ in range(scale)]
#         current_xs = [self.amplitude*np.sin(frequency*t+self.phase) for t in range(scale)]
#         self.xs = current_xs
#
#
# class Signal:
#     def __init__(self, harmonic_amount, scale):
#         current_sum = [0 for _ in range(scale)]
#         for i in range(1, harmonic_amount+1):
#             current_harmonic = Harmonic(STEP*i, scale)
#             current_sum = [current_sum[t]+current_harmonic.xs[t] for t in range(scale)]
#         self.xss = current_sum
#
#
# def generateSignal(harmonic_amount, scale):
#     signal = Signal(harmonic_amount, scale)
#     ts = [t for t in range(scale)]
#     plt.plot(ts, signal.xss, 'k')
#     plt.grid(True)
#     plt.show()
#
#
# generateSignal(HARMONICS, SCALE)
# plt.subplot(2, 1, 1)
# t = np.arange(0, SCALE, 1)
# plt.plot(t, x1, 'k')
# plt.xlabel('t')
# plt.ylabel('x(t)')
# plt.grid(True)
#
# plt.subplot(2, 1, 2)
# plt.plot(scales, times, 'r')
# plt.xlabel('N')
# plt.ylabel('t')
#
# plt.savefig('fig.png')
# plt.show()
