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
    mean = sum(signal.xss) / ticks
    print("Mean = {}".format(mean))
    return mean

def calc_dispertion(signal, mean, ticks):
    dispertion = sum(((x-mean)*(x-mean)) for x in signal.xss) / (ticks-1)
    print("Dispertion = {}".format(dispertion))
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

def calc_DFT(signal, ticks, table=None):
    re = []
    im = []
    for p in range(ticks-1):
        sum_re = 0
        sum_im = 0
        for k in range(ticks-1):
            if (not table):
                arg = 2*np.pi/ticks*p*k
                sum_re += signal.xss[k]*np.cos(arg)
                sum_im += signal.xss[k]*np.sin(arg)
            else:
                w = p * k % ticks
                sum_re += signal.xss[k]*table[w][0]
                sum_im += signal.xss[k]*table[w][1]
        re.append(sum_re)
        im.append(sum_im)
    result = np.sqrt([((re[i]*re[i])+(im[i]*im[i])) for i in range(ticks-1)]), \
            [p for p in range(ticks-1)]
    return result

def generate_table(ticks):
    table_set = []
    for pk in range(ticks):
        arg = 2*np.pi/ticks*pk
        table_set.append((np.cos(arg), np.sin(arg)))
    return table_set

signal_x = generate_signal(HARMONICS, TICKS, STEP)

mean_x = calc_mean(signal_x, TICKS)
calc_dispertion(signal_x, mean_x, TICKS)
startTime = time.time()
fourier_x, ps = calc_DFT(signal_x, TICKS)
print("Elapsed time = {}".format(time.time()-startTime))
compl_t, compl_n = calc_complexity(1)

table = generate_table(TICKS)
startTime = time.time()
calc_DFT(signal_x, TICKS, table)
print("Elapsed time = {}".format(time.time()-startTime))

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

plt.savefig('fig3.png')
plt.show()
