# Cosmosis

0) Log into a Fermilab machine 

1) Run these commands:
```
$ source /cvmfs/des.opensciencegrid.org/users/cosmosis/neutrinoless_mass_function_2-20200630/setup-env.sh
$ spack load -r gcc@8.2.0
$ spack load -r cosmosis@neutrinoless_mass_function_2
$ spack load -r cmake
```

2) Create the working directory
```
$ mkdir des_gw_work
```

3) Create the following variables inside the working directory 
```
$ cd des_gw_work
$ export GW_DIR=$PWD
$ export DES_GW_WORK_DIR=${GW_DIR}/gw
```


4) Stay in the working dir and clone the gw repository 
```
$ git clone https://github.com/SSantosLab/gw.git
```

5) Change to the fermigrid branch
```
$git checkout fermigrid 
```

Now, you can run the mpirun command from the next section. 

Next time that you log-in, you just need to re-do the steps 1) and 3) to setup cosmosis.    


# gw

Get chains with burn-in applied. [For DES Y1, skip this step. The y1 chains are already trimmed]
```
python cosmosis-trim-multinest chains/2pt_NG.fits_d_w_chain.txt chains/2pt_NG.fits_d_w_chain_trimmed.txt 
```

Run the importance sampling
```
mpirun -n 8 cosmosis --mpi params.ini
```

Plot default cosmosis plots
```
postprocess  --burn 5000  -o plots -p gwem params.ini
```

If is too slow, add these options
```
--no-2d t
--only=cosmo
```

Or use this script to plot with Chainconsumer
```
python plot_chains.py
```

## Development notes

Nov/2020 Added the fermigrid branch
Mar/2021 Added the plot script with chainconsumer, cleaning some files 

