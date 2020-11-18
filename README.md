## Cosmosis

Log into a Fermilab machine 

Run these commands:
```
$ source /cvmfs/des.opensciencegrid.org/users/cosmosis/neutrinoless_mass_function_2-20200630/setup-env.sh
$ spack load -r gcc@8.2.0
$ spack load -r cosmosis@neutrinoless_mass_function_2
$ spack load -r cmake
```

Create the working directory
```
$ mkdir des_gw_work
```

Create the following variables inside the working directory 
```
$ cd des_gw_work
$ export GW_DIR=$PWD
$ export DES_GW_WORK_DIR=${GW_DIR}/gw
```


Stay in the working dir and clone the gw repository 
```
$ git clone https://github.com/SSantosLab/gw.git
```

Change to the fermigrid branch
```
$git checkout fermigrid 
```

Now, you can run the mpirun command from the next section. 

## gw

[skip this step, the y1 chains are already trimmed]
python cosmosis-trim-multinest chains/2pt_NG.fits_d_w_chain.txt chains/2pt_NG.fits_d_w_chain_trimmed.txt 

mpirun -n 8 cosmosis --mpi params.ini

postprocess  --burn 5000  -o plots -p gwem params.ini

--no-2d t
--only=cosmo


