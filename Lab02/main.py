import numpy as np
import matplotlib.pyplot as plt
import random
import time


TICKS = 1024
HARMONICS = 8
FREQUENCY = 1200
STEP = FREQUENCY / HARMONICS


class Harmonic:
    def __init__(self, frequency, ticks):
        self.amplitude = random.uniform(0.0, 1.0)
        self.phase = random.uniform(0.0, 2*np.pi)
        current_xs = [0 for _ in range(ticks)]
        current_xs = [self.amplitude*np.sin(frequency*t+self.phase) for t in range(ticks)]
        self.xs = current_xs


class Signal:
    def __init__(self, harmonic_amount, ticks, step):
        current_sum = [0 for _ in range(ticks)]
        start = time.time()
        for i in range(1, harmonic_amount+1):
            current_harmonic = Harmonic(step*i, ticks)
            current_sum = [current_sum[t]+current_harmonic.xs[t] for t in range(ticks)]
        self.elapsed_time = time.time() - start
        self.xss = current_sum
        self.ts = [t for t in range(ticks)]


def generate_signal(harmonic_amount, ticks, step):
    return Signal(harmonic_amount, ticks, step)


def calc_mean(signal, ticks):
    # start = time.time()
    mean = sum(signal.xss) / ticks
    # elapsedTime = time.time() - start
    print("Mean = {}".format(mean))
    # print("Elapsed time for mean calculation = {}".format(elapsedTime))
    # print("----------------------------------------------------------")
    return mean


def calc_dispertion(signal, mean, ticks):
    # start = time.time()
    dispertion = sum(((x-mean)*(x-mean)) for x in signal.xss) / (ticks-1)
    # elapsedTime = time.time() - start
    print("Dispertion = {}".format(dispertion))
    # print("Elapsed time for dispertion calculation = {}".format(elapsedTime))
    print('----------------------------------------------------------')


def calc_autocorrelation(signal, mean, ticks):
    autocorr_sum = [sum([(signal.xss[t]-mean)*(signal.xss[t+tau]-mean) \
            for t in range(ticks)]) for tau in range(ticks)]
    autocorr_sum = np.divide(autocorr_sum, (ticks-1))
    return autocorr_sum


def calc_correlation(signal_1, signal_2, mean_1, mean_2, ticks):
    corr_sum = [sum([(signal_1.xss[t]-mean_1)*(signal_2.xss[t+tau]-mean_2) \
            for t in range(ticks)]) for tau in range(ticks)]
    corr_sum = np.divide(corr_sum, (ticks-1))
    return corr_sum


def calc_complexity(num):
    times = [generate_signal(HARMONICS, TICKS*i, STEP).elapsed_time for i in range(1, num+1)]
    nums = [TICKS*i for i in range(1, num+1)]
    return times, nums


signal_x = generate_signal(HARMONICS, TICKS*2, STEP)
signal_y = generate_signal(HARMONICS, TICKS*2, STEP)

mean_x = calc_mean(signal_x, TICKS*2)
calc_dispertion(signal_x, mean_x, TICKS*2)

mean_y = calc_mean(signal_y, TICKS*2)
calc_dispertion(signal_y, mean_y, TICKS*2)

autocorr_x = calc_autocorrelation(signal_x, mean_x, TICKS)
autocorr_y = calc_autocorrelation(signal_y, mean_y, TICKS)
corr_xy = calc_correlation(signal_x, signal_y, mean_x, mean_y, TICKS)

complexity_t, complexity_N = calc_complexity(10)


plt.subplot(3, 2, 1)
plt.plot(signal_x.ts, signal_x.xss, 'm')
plt.ylabel('x(t)')
plt.grid(True)

plt.subplot(3, 2, 3)
plt.plot(signal_y.ts, signal_y.xss, 'b')
plt.xlabel('t')
plt.ylabel('y(t)')
plt.grid(True)

plt.subplot(3, 2, 5)
plt.plot(complexity_N, complexity_t, 'k')
plt.xlabel('N')
plt.ylabel('t')
plt.grid(True)

ttau = np.arange(0, TICKS, 1)

plt.subplot(3, 2, 2)
plt.plot(ttau, autocorr_x, 'm')
plt.ylabel('Rxx')
plt.grid(True)

plt.subplot(3, 2, 4)
plt.plot(ttau, autocorr_y, 'b')
plt.ylabel('Ryy')
plt.grid(True)

plt.subplot(3, 2, 6)
plt.plot(ttau, corr_xy, 'c')
plt.xlabel('tau')
plt.ylabel('Rxy')
plt.grid(True)

plt.savefig('fig.png')
plt.show()
