# gw

cosmosis params.ini

mpirun -n 8 cosmosis --mpi params.ini

postprocess  --burn 5000  -o plots -p gwem params.ini

