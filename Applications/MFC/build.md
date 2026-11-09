# To build configure

cd Applications/MFC

source ./mfc.sh load -c my_h100 -m g

remeber to override Slurm's srun with --binary mpirun (as Slurm is quite buggy right now)

to see/change the configure, nano MFC/toolchain/module
# Important parameters list that may affect speed and accuracy

rdma_mpi ("T" to utilize NVlink) -> This is essential because it allows GPUs communicate directly to GPUs
- We are allowed to use this option, and Team Diablo seems to agree that setting this is critical.

*** resolution/domain decomposition (m,n,p) -> This affects the computing cells, which also affects accuracy and resolution of the simulation

** cfl_target (resolution jump step) -> This parameter affects the jump step of the simulation, which affects accuracy and runtime

NVCOMPILER_ACC_CUDA_HEAPSIZE = 2GB -> This parameter allocates a part of VRAM for dynamic object. When allocating memory, GPUs require fixed memory object however there is some dynamic variables in the simulation. Hence, we allocate a part of memory to deal with dynamic variables.

** WENO order = 3/5/7 -> This is how many neighbors a cell use to calculate its value

* floating-point precision (single or double but no mixed) -> This affects the acucracy and the runtime

** time_stepper -> This is numerical algorithms (Runge Kutta 1/2/3) and many mores (We can utilize algorithmic advantage)

* --gpu acc/omp -> For acc, let GPUs do all the heavy math while for omp, let GPUs and CPUs do the math. (I believe acc is better in this case as the simulation is solving ODEs and also the GPUs itself can communicate to other)

-j n -> This number of thread each gpu can access (I believe if there is more threads ,they're just idle, losing more time due to context-switching between threads)

--case-optimized -> Automatic tuning, hard-coding parameters to speed up the simulation, however, accuracy remains unchanged.


# Some questions worth answering:

there are a few numerical algorithms in time_stepper, I wonder what is their algorithmic advantage in our usage case?


WENO order really plays an important role, of course, 7 is always give the most accurate result. But, can we find an example using lower WENO order gives a good result? In other words, any usage cases that knowing more neighbors doesn't affect the result much


double or single? does physics simulation affect by rounding off tiny number behind
- Per the [google group](https://groups.google.com/g/scc-connect-sc26/c/MGWbGteblvY), double-precision is required. 
- Team Diablo found that --single was ~23% faster. 
