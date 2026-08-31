[link to video](https://www.youtube.com/watch?v=IrLfy4zi6kg&t=2s)
## Code changes
if we make changes to the code:
- must maintain application performance, portability, and quality
- changes are limited to +/- 5000 lines

## Model and Numerical Method
- Compressible and multiphase (density can change in each material)
	- n phases -> 2n + 4 equations solved per grid cell
- Time stepping is explicit Runge-Kutta
- Rectilinear grid (MPI decomp is easy) -> only 1-2% of the domain gets communicated in each direction.

## I/O
Two methods for I/O:
### file-per-process:
- simple and fast
- O(10^6) files, lots of concurrent metadata creation
### shared-file
- Parallel, O(10^3) files, minor metadata creation
- Only expressed in MPI and not fast on all systems.

## Code Design
Three executables: pre_process (only on CPU), simulation (CPU/GPU), post_process (only CPU)
- communicate through files written to disk
- pre_process writes rect grid and initial condition files
- simulation writes snapshots 
- post_process can write silo/HDF5 for visualization 

pre_process and post_process can be performed on CPU nodes with more ranks/node
post_process can be repeated if more derived quantities are needed

## GPU Kernels
- OpenACC and OpenMP offloading supported
	- OpenACC preferred for NVIDIA hardware, OpenMP for AMD hardware
- Possible through FYPP and compiler guards -> more details in presentation.

## Memory Model
- device-resident memory model
- CPU (host) -> arrays initialized. at initialization, GPU copy also created.
	- this represents the one large host -> device transfer in the code
- GPU takes state vars, fluxes, etc, does math and updates GPU copies.
	- MPI halo exchange -> buff_send, buff_recv (GPU-aware MPI, only on newer systems)
- large device -> host transfers happen when I/O operations occur
- small host <-> device transfers happen at halo exchanges (unless doing GPU-aware MPI)

## CI
- Correctness tests across different hardware/compilers -> comparison against golden files
- Performance tests -> grindtime measured between main and incoming branches
- Portability tests -> measured across compilers/hw for correctness and performance
- Quality tests -> code conformity (lint/style, test coverage, DRYness, etc)
Different tests run in different situations -> in depth perf/port tests usually require a non-draft PR
- code changes used in competition must pass all CI

## Performance Characteristics
- standard test case: spherical bubble collapse using reflective boundary conditions
	- Air bubble in water collapsing
- common two-fluid problem, lots of available performance results

### grind time
- **grind time**: RHS calculation, runge-kutta update, and application of additional physics
	- min taken on each rank over all stages and steps after a warmup period has passed
	- at the end, the max time is taken over all ranks and converted to the correct units (ns / grid cell / equation / RHS evaluation)
- excluded: I/O, MPI spin-wait, some chemistry + immersed boundary routines

### time step breakdown
- large portion of each time step spent in WENO and HLLC Riemann kernels
	- array packing: smaller fraction of runtime on NVIDIA hardware than AMD hardware
- Riemann memory-bound on all hardware
	- **potential for optimization here** -> relies on thread-private arrays for intermediate values
- WENO compute-bound on most hardware

scales both strongly and weakly

Compiler options don't need to pass full CI test suite, but must demonstrate that ./mfc.sh test passes on our hardware and disclose changes to judges in writeup. Code changes must pass full test suite via a public GitHub PR.

Points maybe involved in contributing to the code?