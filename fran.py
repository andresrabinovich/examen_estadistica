from __future__ import division
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as sp
import pdb

if __name__ == "__main__":

	rango_m = (10, 110)
	rango_n = (10, 110)
	a = np.zeros((rango_m[1]-rango_m[0], rango_n[1]-rango_n[0]))
	b = np.zeros((rango_m[1]-rango_m[0], rango_n[1]-rango_n[0]))
	
	archivo  = open("resultado.csv", "r") 
	
	for line in archivo:
		m, n, g, h = line.split(",")
		a[int(n)-rango_n[0], int(m)-rango_m[0]] = float(g)
		b[int(m)-rango_m[0], int(n)-rango_n[0]] = float(h)

	archivo.close()

	
	fig, ax = plt.subplots()
	im = ax.pcolormesh(np.arange(rango_m[0], rango_m[1]),  np.arange(rango_n[0], rango_n[1]), a)
	fig.colorbar(im)
	ax.axis('tight')
	plt.show()

	fig, ax = plt.subplots()
	im = ax.pcolormesh(np.arange(rango_m[0], rango_m[1]),  np.arange(rango_n[0], rango_n[1]), b)
	fig.colorbar(im)
	ax.axis('tight')
	plt.show()

	
		
	
	






