import numpy as np
from chainconsumer import ChainConsumer

def chain_desy3_plot(filename, out, chainnames, paranames,plotrange):
    #Plotting the DES Y3 forecast + GW
    d1read = np.genfromtxt(filename[0], usecols=(0, 1, 2, 6, 27))
    d2read = np.genfromtxt(filename[1], usecols=(0, 1, 2, 6, 27))

    w1 = np.genfromtxt(filename[0], usecols=(29))
    weightd1=np.array(np.exp(w1))

    w2 = np.genfromtxt(filename[1], usecols=(30))
    weightd2=np.array(np.exp(w2))
    
    #burn_in = 3500000 #Burn_in already removed for trimmed sample 
    #d1read = d1read[burn_in:, :]
    #d2read = d2read[burn_in:, :]

    c = ChainConsumer()
    c.add_chain(d1read,parameters=paranames, name=chainnames[0], weights=weightd1)
    c.add_chain(d2read,parameters=paranames, name=chainnames[1], weights=weightd2)
    print "Plotting..." 
    c.configure(kde=[2,2],colors=['c','y'], sigmas=[0,1,2],shade=True,shade_alpha=0.2,shade_gradient=0.0, legend_kwargs={"labelspacing": 0.1,"fontsize":20})
    fig = c.plotter.plot(figsize=1.7,filename="./"+out) #extents=plotrange,

filename=["./2pt_NG.fits_d_w_chain_trimmed.txt","./maria_o3_sim_test3.txt"]
chainnames=[r"DES Y3 3x2pt Forecast", r"DES Y3 Forecast + GW O3"]
paranames=[r"$\Omega_m$", r"$h_0$", r"$\Omega_b$", r"$w$", r"$\sigma_8$"]
plotrange=[(0.25,0.4),(0.75,0.9),(0.92,1.0),(-1.5,-0.5),(-1.5,1.5),(0.03,0.07),(0.5,0.9)]
chain_desy3_plot(filename,"DESY3forecast_3x2pt_GWO3_trimmed.pdf",chainnames,paranames,plotrange)
