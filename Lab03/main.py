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


def calc_complexity(num):
    times = []
    for i in range(1, num+1):
        signal = generate_signal(HARMONICS, TICKS*i, STEP)
        start = time.time()
        calc_DFT(signal, TICKS*i)
        elapsed_time = time.time() - start + signal.elapsed_time
        times.append(elapsed_time)
    nums = [TICKS*i for i in range(1, num+1)]
    return times, nums


def calc_DFT(signal, ticks):
    re = []
    im = []
    for p in range(ticks-1):
        sum_re = 0
        sum_im = 0
        for k in range(ticks-1):
            sum_re += signal.xss[k]*np.cos(2*np.pi/ticks*p*k)
            sum_im += signal.xss[k]*np.sin(2*np.pi/ticks*p*k)
        re.append(sum_re)
        im.append(sum_im)
    return np.sqrt([((re[i]*re[i])+(im[i]*im[i])) for i in range(ticks-1)]), \
            [p for p in range(ticks-1)]


signal_x = generate_signal(HARMONICS, TICKS, STEP)

mean_x = calc_mean(signal_x, TICKS)
calc_dispertion(signal_x, mean_x, TICKS)
fourier_x, ps = calc_DFT(signal_x, TICKS)
compl_t, compl_n = calc_complexity(5)


plt.subplot(3, 1, 1)
plt.plot(signal_x.ts, signal_x.xss, 'k')
plt.xlabel('t')
plt.ylabel('x(t)')
plt.grid(True)

plt.subplot(3, 1, 2)
plt.plot(ps, fourier_x, 'b')
plt.xlabel('p')
plt.ylabel('F(p)')
plt.grid(True)

plt.subplot(3, 1, 3)
plt.plot(compl_n, compl_t, 'c')
plt.xlabel('N')
plt.ylabel('t')
plt.grid(True)


plt.savefig('fig.png')
plt.show()
