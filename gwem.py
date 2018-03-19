import numpy as np
import os
from cosmosis.datablock import names as section_names
from cosmosis.datablock import option_section
from cosmosis.runtime.declare import declare_module
from scipy.interpolate import UnivariateSpline
import scipy
import gwemlib

class gwem():

    likes = section_names.likelihoods
    dists = section_names.distances
    datav = section_names.data_vector

    def __init__(self,config,name):
        
        data_dir = config.get_string(name,"data_dir",default="data")
        data_file = config.get_string(name,"data_file",default="test.txt")
        self.data = np.genfromtxt(os.path.join(data_dir,data_file),names=True,unpack=True)
        self.norm = 0.5 * np.log(2*np.pi) * self.data.size
        z_frame = config.get_string(name,"z_frame",default="helio")
        if "vp" in self.data.dtype.names:
            self.data["z"] = gwemlib.z(self.data["z"],self.data["vp"],z_frame)
        else:
            self.data["z"] = gwemlib.z(self.data["z"],np.zeros_like(self.data["z"]),z_frame)
        
    def execute(self,block):

        dl_t = block[gwem.dists, "d_l"]
        z_t = block[gwem.dists,"z"]
        i = np.where(z_t < np.max(self.data["z"] + 3 * self.data["zerr"]))
        dl_theory = UnivariateSpline(z_t[i], dl_t[i])
        var = gwemlib.sigma2(self.data,dl_theory)
        chi2 = ((dl_theory(self.data["z"]) - self.data["dl"])**2 / var).sum()
        block[gwem.likes, "GWEM_LIKE"] =  - (chi2 / 2.0) - self.norm - ((np.log(var)).sum()/2.0) 

        # Fisher matrix calculations need this stuff:
        if self.data.size > 1:
            block[gwem.datav, "GWEM_THEORY"] = dl_theory(self.data["z"])
            block[gwem.datav, "GWEM_INVERSE_COVARIANCE"] = np.linalg.inv(np.diag(var))
        else:
            block[gwem.datav, "GWEM_THEORY"] = [dl_theory(self.data["z"])]
            block[gwem.datav, "GWEM_INVERSE_COVARIANCE"] = [1./var]

        return 0
        
    def cleanup(self):
        return 0

declare_module(gwem)
