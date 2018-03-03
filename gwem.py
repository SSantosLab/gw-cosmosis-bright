import numpy as np
import os
from cosmosis.datablock import names as section_names
from cosmosis.datablock import option_section
from cosmosis.runtime.declare import declare_module
from scipy.interpolate import UnivariateSpline
import gwemlib

class gwem():

    likes = section_names.likelihoods
    dists = section_names.distances

    def __init__(self,config,name):
        
        data_dir = config.get_string(name,"data_dir",default="data")
        data_file = config.get_string(name,"data_file",default="test_simple.txt")
        self.data = np.genfromtxt(os.path.join(data_dir,data_file),names=True,unpack=True)        
        self.norm = 0.5 * np.log(2*np.pi) * self.data.size
        self.data["z"] = gwemlib.z(self.data["z"],self.data["zp"])
        
    def execute(self,block):

        dl_t = block[gwem.dists, "d_l"]
        z_t = block[gwem.dists,"z"]
        dl_theory = UnivariateSpline(z_t, dl_t)
        var = gwemlib.sigma2(self.data,dl_theory)
        chi2 = ((dl_theory(self.data["z"]) - self.data["dl"])**2 / var).sum()
        block[gwem.likes, "GWEM_LIKE"] =  - (chi2 / 2.0) - self.norm - ((np.log(var)).sum()/2.0) 
        return 0
        
    def cleanup(self):
        return 0

declare_module(gwem)
