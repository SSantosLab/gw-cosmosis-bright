import numpy as np
from scipy.interpolate import UnivariateSpline
from scipy.constants import speed_of_light 

c = speed_of_light / 1000. # [km/s]

# Compute the cosmological redshift using Davis et al. 2011 (eq. 15)
# http://adsabs.harvard.edu/abs/2011ApJ...741...67D
def z(zh,vp,frame="helio"):
    zCMB = 369.0 / c # Hinshaw et al. 2009
    if frame == "cmb": zCMB = 0.0
    zp = vp / c 
    z = ( (1+zh) / ((1+zp)*(1+zCMB)) ) - 1
#    print zh,zp,zCMB
    return z

# Compute the total variance sigma**2 for the chi**2 calculation.  
# Propagating uncertainties in both the redshift and distance. 
# Use correllation coefficients, if provided.
# Use counterpart probabilities as weights, if provided.
def sigma2(data,model):

    # compute first derivative of dl(z) function 
    f = model.derivative()
    g = f(data["z"])

    # load random uncertainties from data vector
    z_obs_err = np.zeros_like(data["z"])
    d_obs_err_plu = np.zeros_like(data["z"])
    d_obs_err_min = np.zeros_like(data["z"])
    if "zerr"  in data.dtype.names: z_obs_err = data["zerr"]
    if "dlerr" in data.dtype.names:
        d_obs_err_plu = data["dlerr"]
        d_obs_err_min = data["dlerr"]
    if "dlerrp" in data.dtype.names: d_obs_err_plu = data["dlerrp"]
    if "dlerrm" in data.dtype.names: d_obs_err_min = data["dlerrm"]

    # load systematic uncertainties in z, if provided
    if "vperr" in data.dtype.names:
        z_syst_err = data["vperr"] / c
    else:
    # otherwise, assume zero
        z_syst_err = np.zeros_like(z_obs_err)

    # load systematic uncertainties in d, if provided
    if "dlsyst" in data.dtype.names:
        d_syst_err = data["dlsyst"] 
    else:
    # otherwise, assume zero
        d_syst_err = np.zeros_like(z_obs_err)

    # compute total uncertainties
    zerr = np.sqrt(z_obs_err**2 + z_syst_err**2)
    derrplu = np.sqrt(d_obs_err_plu**2 + d_syst_err**2)
    derrmin = np.sqrt(d_obs_err_min**2 + d_syst_err**2)
    derr = (d_obs_err_plu + d_obs_err_min) / 2.

    # load correlation coefficient, if provided
    if "rho" in data.dtype.names:
        rho = data["rho"]
    else:
    # otherwise, assume that dl and z measurements are independent
        rho = np.zeros_like(z_obs_err)

    # load weights, if provided
    if "prand" in data.dtype.names:
        w = 1.0 - data["prand"]
    else:
    # otherwise, assume unity weights 
        w = np.ones_like(derrplu)

    # compute variance
    #
    #var = (derr**2) + (g**2 * zerr**2) + (2 * g * rho * zerr * derr)
    # 
    # using eq. 14-16 of arXiv:physics/0406120    
    sigmaplu = np.sqrt((derrplu**2) + (g**2 * zerr**2) + (2 * g * rho * zerr * derrplu))
    sigmamin = np.sqrt((derrmin**2) + (g**2 * zerr**2) + (2 * g * rho * zerr * derrmin))
    sigma = 2 * sigmaplu * sigmamin / (sigmaplu + sigmamin)
    sigmaprime = np.abs(sigmaplu - sigmamin) / (sigmaplu + sigmamin)
    var = (sigma + sigmaprime * np.abs(model(data["z"])-data["dl"]) )**2

    # apply weights and return
    return var/w


### 

