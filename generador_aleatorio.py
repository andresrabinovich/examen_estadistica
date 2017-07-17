from __future__ import division
import multiprocessing
from multiprocessing import Process, Manager
import random
from time import time
import matplotlib.pyplot as plt
import numpy as np
import math

class miProceso (multiprocessing.Process):
    def __init__(self, processID, tiros, return_dict):
        multiprocessing.Process.__init__(self)
        self.processID = processID
        self.tiros = tiros
        return_dict[self.processID] = 0
    
    def run(self):
        #print("empezando %d" % self.processID)
        return_dict[self.processID] = tirar(self.tiros, self.processID)
        #print("terminando %d" % self.processID)

def f(x):
    mu = 0
    sigma = 1
    return 1/(math.sqrt(2*math.pi)*sigma)*math.exp(-0.5*((x-mu)/sigma)**2)
    
def tirar(tiros, semilla):
    local_random = random.Random()
    local_random.seed(semilla*100)
    a = []
    while len(a) < tiros:
    #for i in range(0, tiros):
        x = local_random.uniform(-5, 5)
        y = local_random.uniform(0, 1)
        if (f(x) > y):
            a.append(x)
    return a

manager = Manager()
return_dict = manager.dict()
tiros = 1000000
nprocesos = 4

procesos = []

for i in range(0, nprocesos):
    procesos.append(miProceso(i, int(tiros/nprocesos), return_dict))

for p in procesos:
    p.start()

startTime = time()

for p in procesos:
    p.join()

a = []

for i in range(0, nprocesos):
    a.extend(return_dict[i])

print("tardo %.2f segundos" % (time() - startTime))

thefile = open('test.txt', 'w')
for item in a:
  thefile.write("%s\n" % item)
thefile.close()

bins = np.linspace(-5, 5, 100)   
plt.hist(a, bins)
plt.title("Gaussian Histogram")
plt.xlabel("Value")
plt.ylabel("Frequency")

fig = plt.gcf()
plt.show()


