import numpy as np
import os
import sys
from chainconsumer import ChainConsumer
import matplotlib.pyplot as plt

true = [0.295,.8344]
true = [0.3156,.831]
c = ChainConsumer()
names=['$\\Omega_m$','$h$','$w$','$S_8$']#,'$h_0$','$\\Omega_b$','$n_s$','$A_s$']

dfile = '2pt_NG.fits_d_w_chain.txt' # DES Y1 data
gwfile = 'maria_o3_sim_test.txt'          # GW simulation O3
#gwfile= 'gw170817-holz_joint.txt'
#dfile='chains/2pt_sim_1110_baseline_Y3cov.fits_chain_d_w.txt'
#gwfile='marcelle_Y3_forcast.txt'
print

r1 = 0*np.random.random()
r2 = 0*np.random.random()
r3 = 0*np.random.random()

chaindir = '/Users/maria/current-work/des-gw/MainPaper/'
#chaindir='/data/des41.a/data/alyssag/cosmosis/gw/'

## DES Y3
print("--- Using file: ", dfile)
file = chaindir + dfile
f =open(file)
for i,line in enumerate(f):
    words=line.split("=")
    if '#nsample' in words:
        nstop = i
        nbegin = (nstop) -int(words[1])
        print( 'DES Y3 total chain size: ', nstop)
        print( 'DES Y3 burn-in: ', nbegin)
    if '#log_z' in words:
        #print file, 'log_z=', words[1]
    	dlz = float(words[1])
f.close()
f =open(file)
ch=[]
w=[]
for i,line in enumerate(f):
    if i < nstop and i >= nbegin:
        words=line.split()
        om=float(words[0])+r1
        sigma8=float(words[27])+r2
        s8=(om/0.3)**.5*sigma8
        h=float(words[1])+r1
        ch.append([om,h,float(words[6])+r2,s8])
        w.append(float(words[29]))
w=np.array(w)
ch=np.array(ch)

print('DES Y3 chain size after burn-in = ', len(ch), '\n')
f.close()
c.add_chain(ch,parameters=names,name=r'\textbf{DES Y3}',weights=w)

## DES Y1 + GW
print("--- Adding file: ", gwfile)
file = chaindir + gwfile
data = np.genfromtxt(file)
nstop = len(data)
nbegin = int(round(nstop/2.)) # Burn-in around 50% of the chain
print( 'DES Y3 + GW total chain size: ', nstop)
print( 'DES Y3 + GW burn-in: ', nbegin)

f=open(file)
ch=[]
w=[]
wold=[]
for i,line in enumerate(f):
    if i < nstop and i >= nbegin:
        words=line.split()
        om=float(words[0])+r1
        sigma8=float(words[27])+r2
        s8=(om/0.3)**.5*sigma8
        h=float(words[1])+r1
        ch.append([om,h,float(words[6])+r2,s8])
        w.append(float(words[30]))
        wold.append(float(words[28]))
w=np.array(wold)*np.array(np.exp(w))
#w=np.array(np.exp(w))
ch=np.array(ch)
print( 'DES Y3 + GW chain size after burn-in = ', len(ch))
f.close()
c.add_chain(ch,parameters=names,name=r'\textbf{DES Y3 + GW170817}',weights=w)

print( "Starting plot...")

c.configure(sigma2d=False,shade_alpha=[0.5, 0.5,.1,1.], kde=1.5, shade=['t','t','t','t'],colors=["b", "r","k","g"], linewidths=1.2, shade_gradient=1.0,legend_kwargs={"labelspacing": 0.1,"fontsize":20},diagonal_tick_labels=False,label_font_size=15, max_ticks=5)

fig = c.plotter.plot(figsize=1.7,extents=[[.19,.45],[.55,.85],[-1.8,-.4],[0.7,.9]])

filename='./desy1_joint_gwo3_maria.pdf'
ax = fig.get_axes()
ax[8].set_yticks([-1.6, -1.3, -1, -0.7, -0.4])
ax[14].set_xticks([-1.6, -1.3, -1, -0.7, -0.4])
#plt.show()
fig.savefig(filename, dpi=300, transparent=True, pad_inches=0.05)
