from __future__ import division
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as sp
import pdb

if __name__ == "__main__":

rango_m = (10, 1100)
rango_n = (10, 1100)
a = np.zeros((rango_m[1]-rango_m[0], rango_n[1]-rango_n[0]))
b = np.zeros((rango_m[1]-rango_m[0], rango_n[1]-rango_n[0]))

archivo  = open("corridas/resultado_1.csv", "r") 

for line in archivo:
	m, n, g, h = line.split(",")
	a[int(n)-rango_n[0], int(m)-rango_m[0]] = float(g)
	b[int(m)-rango_m[0], int(n)-rango_n[0]] = float(h)

archivo.close()

fig, ax = plt.subplots()
im = ax.pcolormesh(np.arange(rango_m[0], rango_m[1]),  np.arange(rango_n[0], rango_n[1]), a)
fig.colorbar(im)
ax.axis('tight')
plt.xlabel('m')
plt.ylabel('n')
plt.title(r'P-Value test U1 x $\backsim$ N(0.1, 1) y $\backsim$ N(0, 1)')
plt.show()

fig, ax = plt.subplots()
im = ax.pcolormesh(np.arange(rango_m[0], rango_m[1]),  np.arange(rango_n[0], rango_n[1]), a)
fig.colorbar(im)
ax.axis('tight')
plt.xlabel('m')
plt.ylabel('n')
plt.title(r'P-Value test U2 x $\backsim$ N(0.1, 1) y $\backsim$ N(0, 1)')
plt.show()

	
		
	
n = 800
m = 700

a = []
b = []
for i in range(0, 2000):
	x = np.random.normal(mu1, sigma1, size=m)
	y = np.random.normal(mu2, sigma2, size=n)
	df = n + m - 2
	sx2 = s2(x)
	sy2 = s2(y)
	denominador = ( (1/m)+(1/n) )*(sx2+sy2) 
	u1 = ( x.mean()-y.mean() ) * np.sqrt(df/denominador)
	a.append(u1)
	x = np.random.normal(mu2, sigma1, size=m)
	y = np.random.normal(mu1, sigma2, size=n)
	df = n + m - 2
	sx2 = s2(x)
	sy2 = s2(y)
	denominador = ( (1/m)+(1/n) )*(sx2+sy2) 
	u1 = ( x.mean()-y.mean() ) * np.sqrt(df/denominador)
	b.append(u1)

plt.hist(b)
plt.hist(a)
plt.show()

