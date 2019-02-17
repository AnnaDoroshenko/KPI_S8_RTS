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
x=[]

for harmonic in range(HARMONICS):
    amplitudes.append(random.uniform(0.1, 10.0))
    shifts.append(random.uniform(0.0, 2*np.pi))

start = time.time()
for t in range(SCALE):
    currentSum = 0;
    for harmonic in range(HARMONICS):
        currentSum += amplitudes[harmonic]*np.sin(STEP*(harmonic+1)*t+shifts[harmonic])
    x.append(currentSum)
elapsedTime = time.time() - start;
print("Elapsed time for x(t) calculation = {}".format(elapsedTime))
print("----------------------------------------------------------")

start = time.time()
ev = sum(x) / SCALE
elapsedTime = time.time() - start;
print("Expected value = {}".format(ev))
print("Elapsed time for expected value calculation = {}".format(elapsedTime))
print("----------------------------------------------------------")

start = time.time()
dispertion = sum(((v-ev)*(v-ev)) for v in x) / (SCALE-1)
elapsedTime = time.time() - start;
print("Dispertion = {}".format(dispertion))
print("Elapsed time for dispertion calculation = {}".format(elapsedTime))
print('----------------------------------------------------------')

# Drawing
t = np.arange(0, SCALE, 1)
plt.plot(t, x, 'k')
plt.xlabel('t')
plt.ylabel('x(t)')
plt.grid(True)
plt.savefig('fig.png')
# plt.show()
