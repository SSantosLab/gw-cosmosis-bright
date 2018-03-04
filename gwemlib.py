import numpy as np
from scipy.interpolate import UnivariateSpline
from scipy.constants import speed_of_light as c

# Compute the cosmological redshift using Davis et al. 2011 (eq. 15)
# http://adsabs.harvard.edu/abs/2011ApJ...741...67D
def z(zh,zp):
    zCMB = 369.0 / (c/1000.) # Hinshaw et al. 2009
    z = ( (1+zh) / ((1+zp)*(1+zCMB)) ) - 1
    return z

# Compute the total variance sigma**2 for the chi**2 calculation.  
# Propagating uncertainties in both the redshift and distance. 
# Use correllation coefficients, if provided.
# Use counterpart probabilities as weights, if provided.
def sigma2(data,d_model):

    # compute first derivative of dl(z) function 
    f = d_model.derivative()
    g = f(data["z"])

    # load random uncertainties from data vector
    z_obs_err = data["zerr"]
    d_obs_err = data["dlerr"]

    # load systematic uncertainties in z, if provided
    if "zperr" in data.dtype.names:
        z_syst_err = data["zperr"]
    else:
    # otherwise, assume zero
        z_syst_err = np.zeros_like(z_obs_err)

    # load systematic uncertainties in d, if provided
    if "dlsyst" in data.dtype.names:
        d_syst_err = data["dlsyst"] 
    else:
    # otherwise, assume zero
        d_syst_err = np.zeros_like(d_obs_err)

    # compute total uncertainties
    zerr = np.sqrt(z_obs_err**2 + z_syst_err**2)
    derr = np.sqrt(d_obs_err**2 + d_syst_err**2)

    # load correlation coefficient, if provided
    if "rho" in data.dtype.names:
        rho = data["rho"]
    else:
    # otherwise, assume that dl and z measurements are independent
        rho = np.zeros_like(z_obs_err)

    # load weights, if provided
    if "prob" in data.dtype.names:
        w = data["prob"]
    else:
    # otherwise, assume unity weights 
        w = np.ones_like(derr)

    # compute variance
    var = (derr**2) + (g**2 * zerr**2) + (2 * g * rho * zerr * derr)

    # apply weights and return
    return var/w


