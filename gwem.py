import numpy as np
import os
from cosmosis.datablock import names as section_names
from cosmosis.datablock import option_section
from cosmosis.runtime.declare import declare_module
from scipy.interpolate import interp1d

class gwem():

    likes = section_names.likelihoods
    dists = section_names.distances

    def __init__(self,config,name):
        
        data_dir = config.get_string(name,"data_dir",default="data")
        data_file = config.get_string(name,"data_file",default="test_simple.txt")
        self.data = np.genfromtxt(os.path.join(data_dir,data_file),names=True,unpack=True)        
        self.norm = 0.5 * np.log(2*np.pi**2) * self.data.size
        
    def execute(self, block):

        dl_t = block[gwem.dists, "d_l"]
        z_t = block[gwem.dists,"z"]
        dl_theory = interp1d(z_t, dl_t)

        dl_obs = self.data["dl"]
        dl_obs_err = self.data["dlerr"]
        z_obs = self.data["z"]
        z_obs_err = self.data["zerr"]

        chi2 = ((dl_theory(z_obs) - dl_obs)**2 / dl_obs_err**2).sum()
        block[gwem.likes, "GWEM_LIKE"] =  - chi2 / 2.0 - self.norm

        return 0
        
    def cleanup(self):
        return 0

declare_module(gwem)
