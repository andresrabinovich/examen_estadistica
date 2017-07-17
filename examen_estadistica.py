from __future__ import division
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as sp

def s2(x):
    s2 = 0
    for i in range(0, len(x)):
        s2 = s2 + (x[i]-x.mean())**2
    return(s2)

np.random.seed(12345)

mu1 = 0.1
sigma1 = 1
mu2 = 0
sigma2 = 1
alfa = 0.05

#n_t = 100000
a = []
b = []
c = []
for n in range(10, 20):
    for m in range(10, 20):
        #archivo  = open("a.csv", "r") 

        #for line in archivo: 
        #    c.append(float(line))
        #archivo.close()

        #for i in range(0, 40):
        #    a.append(c[i])

        #for i in range(40, 75):
        #    b.append(c[i])

        #x = np.asarray(a)
        #y = np.asarray(b)
        #m = len(x)
        #n = len(y)
        pv1 = 0
        pv2 = 0
        for i in range(0, 100):
            x = np.random.normal(mu1, sigma1, size=m)
            y = np.random.normal(mu2, sigma2, size=n)
            df = n + m - 2
            sx2 = s2(x)
            sy2 = s2(y)
            denominador = ( (1/m)+(1/n) )*(sx2+sy2) 
            u1 = ( x.mean()-y.mean() ) * np.sqrt(df/denominador)
            u2 = ( x.mean()-y.mean() ) / np.sqrt( sx2/(m*(m-1)) + sy2/(n*(n-1)) )
            #t1 = np.sort(np.random.standard_t(df, size=n_t))
            dof = int((( sx2/(m*(m-1)) + sy2/(n*(n-1)) )**2)/ ( ( sx2/(m*(m-1)) )**2/(m-1) + ( sy2/(n*(n-1)) )**2/(n-1) ))
            #t2 = np.sort(np.random.standard_t(dof, size=n_t))
            pv1 = pv1 + (1-sp.t.cdf(u1, df))
            pv2 = pv2 + (1-sp.t.cdf(u2, dof))
            
        a.append(pv1/100)
        b.append(pv2/100)
            
#print(2*np.minimum( (1-(np.sum(t1<u1) / float(len(t1)))), ((np.sum(u1>t1) / float(len(t1))))))
#print(2*np.minimum( (1-(np.sum(t2<u2) / float(len(t2)))), ((np.sum(u2>t2) / float(len(t2))))))

#print(dof)
#print(df)
#a.append((1-(np.sum(t<u1) / float(len(t)))))
#b.append((1-(np.sum(t2<u2) / float(len(t2)))))
#if n%10 == 0:
#    print(n)
#print("n: %d, u1: %f, cuantil-%.3f: %f, p-value: %f" % (n, u1, 1-alfa, s[int(n_t*(1-alfa))], (1-(np.sum(s<u1) / float(len(s))))) )

#if n%100 == 0:
#bins = np.linspace(np.minimum(np.min(t1), np.min(t2)), np.maximum(np.max(t1), np.max(t2)), 100)   
#plt.hist(t1, bins, color="blue", alpha=0.2, normed=True)
#plt.hist(t2, bins, color="black", alpha=0.2, normed=True)
#plt.axvline(x=t1[int(n_t*(1-alfa))], linewidth=2, color='indigo')
#plt.axvline(x=t2[int(n_t*(1-alfa))], linewidth=2, color='violet')
#    #plt.axvline(x=s[int(n_t*alfa/2)], linewidth=2, color='red')
#plt.axvline(x=u2, linewidth=2, color='red')
#plt.axvline(x=u1, linewidth=2, color='green')
#plt.show()

plt.imshow(a, cmap='hot', interpolation='nearest')
plt.show()
        
plt.scatter(range(0, len(a)), a, color="blue")
#plt.scatter(range(0, len(b)), b, color="red")
plt.show()


archivow  = open("corridas/resultado_b.csv", "w") 
for i in [7, 8]:
     archivo  = open("corridas/resultado%d.csv" % i, "r") 
     for line in archivo:
         archivow.write(line)
     archivo.close()

archivow.close()

rango_m = (10, 1100)
rango_n = (10, 1100)
a = np.zeros((rango_m[1]-rango_m[0], rango_n[1]-rango_n[0]))
b = np.zeros((rango_m[1]-rango_m[0], rango_n[1]-rango_n[0]))
archivo  = open("corridas/resultado_a.csv", "r") 
for line in archivo:
    m, n, g, h = line.split(",")
    a[int(n)-rango_n[0], int(m)-rango_m[0]] = float(g)
    b[int(m)-rango_m[0], int(n)-rango_n[0]] = float(h)

archivo.close()

fig, ax = plt.subplots()
im = ax.pcolormesh(range(rango_m[0], rango_m[1]),  range(rango_n[0], rango_n[1]), a)
fig.colorbar(im)
ax.axis('tight')
plt.show()
 






