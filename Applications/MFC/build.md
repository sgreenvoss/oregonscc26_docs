# To build configure

cd Applications/MFC

source ./mfc.sh load -c my_h100 -m g

remeber to override Slurm's srun with --binary mpirun (as Slurm is quite buggy right now)

to see/change the configure, nano MFC/toolchain/module
# Important parameters list that may affect speed and accuracy

## GPU related

rdma_mpi ("T" to utilize NVlink) -> This is essential because it allows GPUs communicate directly to GPUs
- We are allowed to use this option, and Team Diablo seems to agree that setting this is critical.

NVCOMPILER_ACC_CUDA_HEAPSIZE = 2GB -> This parameter allocates a part of VRAM for dynamic object. When allocating memory, GPUs require fixed memory object however there is some dynamic variables in the simulation. Hence, we allocate a part of memory to deal with dynamic variables.

* --gpu acc/omp -> For acc, let GPUs do all the heavy math while for omp, let GPUs and CPUs do the math. (I believe acc is better in this case as the simulation is solving ODEs and also the GPUs itself can communicate to other)

-j n -> This number of thread each gpu can access (I believe if there is more threads ,they're just idle, losing more time due to context-switching between threads)


## Accuracy-related

floating-point precision (single or double but no mixed) -> This affects the acucracy and the runtime -> it's required to use double precision

*** resolution/domain decomposition (m,n,p) -> This affects the computing cells, which also affects accuracy and resolution of the simulation

** cfl_target (resolution jump step) -> This parameter affects the jump step of the simulation, which affects accuracy and runtime

dt (time step) -> specifies the constant time step size used in the simulation. The value of dt needs to be sufficiently small to satisfy the Courant-Friedrichs-Lewy (CFL) condition

cfl_adap_dt enables adaptive time stepping with a constant CFL when true

cfl_const_dt enables constant dt time-stepping where dt results in a specified CFL for the initial condition

## Numerical solver
 
riemann_solver = 1/2/3/4 -> Unsure

** time_stepper -> This is numerical algorithms (Runge Kutta 1/2/3) and many mores (We can utilize algorithmic advantage). From my understanding, 1/2/3 here means how many points we look before predicting the line.

WENO order = 1/3/5/7 -> This is how many neighbors a cell use to calculate its value
 (there are a lot of WENO-related parameters, such as weno_order, weno_eps, mapped_weno, wenoz, wenoz_q, teno, teno_CT, null_weights, mp_weno)

## Compiler-related

--case-optimized -> Automatic tuning, hard-coding parameters to speed up the simulation, however, accuracy remains unchanged.


# Cool parameters but unsure if it help

cyl_coord	Logical	Cylindrical coordinates (2D: Axisymmetric, 3D: Cylindrical)

nv_uvm_out_of_core	Logical	Enable NVIDIA Unified Virtual Memory out-of-core execution

nv_uvm_pref_gpu	Logical	Prefer GPU placement for NVIDIA UVM allocations -> borrow memory from CPUs, I think this is not a good idea

nv_uvm_igr_temps_on_gpu	Integer	Store IGR temporaries on GPU with UVM

## Formatted Output

if we allow more values written to the database, the simulation may slow down due to I/O process.

From my understanding, every necessary information for the simulation will be stored in GPUs' VRAM. Hence, we only need to turn on data which is required for validating from the SCC committee.

# Some questions worth answering:

there are a few numerical algorithms in time_stepper, I wonder what is their algorithmic advantage in our usage case?
- time_stepper basically is just how you want the result more accurate or less accurate. However, riemann_solver is quite interesting, when running, the physics object has sawtooth at its boundary, some algorithm use diffusion to calculate the middle point and end up being faster but blurry result. 


WENO order really plays an important role, of course, 7 is always give the most accurate result. But, can we find an example using lower WENO order gives a good result? In other words, any usage cases that knowing more neighbors doesn't affect the result much


double or single? does physics simulation affect by rounding off tiny number behind
- Per the [google group](https://groups.google.com/g/scc-connect-sc26/c/MGWbGteblvY), double-precision is required. 
- Team Diablo found that --single was ~23% faster. 


what does case-optimized change?
- it is a compiler trick avoid redundant steps (eliminating unused code, hardcoding variables to avoid memory access, loop unrolling for parallel programming) when running the code

ideal stress test that can show the difference between configures? I tried sphbubcollapse and 2D_shockdroplet.


