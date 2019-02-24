import numpy as np
import matplotlib.pyplot as plt
import random
import time


SCALE = 1024
HARMONICS = 8
FREQUENCY = 1200
STEP = FREQUENCY / HARMONICS


amplitudes = []
shifts = []


for harmonic in range(HARMONICS):
    amplitudes.append(random.uniform(0.0, 1.0))
    shifts.append(random.uniform(0.0, 2*np.pi))


def signal(scale, x):
    start = time.time()
    for t in range(scale):
        currentSum = 0;
        for harmonic in range(HARMONICS):
            currentSum += amplitudes[harmonic]*np.sin(STEP*(harmonic+1)*t+shifts[harmonic])
        x.append(currentSum)
    elapsedTime = time.time() - start;
    print("Elapsed time for x(t) calculation = {}".format(elapsedTime))
    print("----------------------------------------------------------")
    return elapsedTime;


x1 = []
signal(SCALE, x1)


x=[]
scales = []
times = []
for i in range(1, 5):
    currentScale = SCALE * i
    scales.append(currentScale)
    currentTime = signal(currentScale, x)
    times.append(currentTime)


start = time.time()
ev = sum(x1) / SCALE
elapsedTime = time.time() - start;
print("Expected value = {}".format(ev))
print("Elapsed time for expected value calculation = {}".format(elapsedTime))
print("----------------------------------------------------------")

start = time.time()
dispertion = sum(((v-ev)*(v-ev)) for v in x1) / (SCALE-1)
elapsedTime = time.time() - start;
print("Dispertion = {}".format(dispertion))
print("Elapsed time for dispertion calculation = {}".format(elapsedTime))
print('----------------------------------------------------------')


plt.subplot(2, 1, 1)
t = np.arange(0, SCALE, 1)
plt.plot(t, x1, 'k')
plt.xlabel('t')
plt.ylabel('x(t)')
plt.grid(True)

plt.subplot(2, 1, 2)
plt.plot(scales, times, 'r')
plt.xlabel('N')
plt.ylabel('t')

plt.savefig('fig.png')
plt.show()
