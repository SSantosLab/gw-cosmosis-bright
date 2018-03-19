# gw

python cosmosis-trim-multinest chains/2pt_NG.fits_d_w_chain.txt chains/2pt_NG.fits_d_w_chain_trimmed.txt 

mpirun -n 8 cosmosis --mpi params.ini

postprocess  --burn 5000  -o plots -p gwem params.ini

--no-2d t
--only=cosmo


