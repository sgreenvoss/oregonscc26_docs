- First attempt to install: `spack install wrf build_type=dm+sm` with nvhpc_25.sh sourced

## WRF types
### wrf/kouzobr is **dmpar**, em_real, nesting=basic
- nohup mpirun -n 64 ./wrf.exe &
	- half utilization
	- i'm pointing my monitoring script at only one of the output files (it makes one per process) 
	- looks like it's moving pretty quickly, but am i missing something by only looking at one - does one process only look at one part, can they move through time differently?
		- i.e., how does the mpi decomposition work here?
	- died after 14 minutes - grep -i error rsl.\* yields `**ERROR**: ghg_input available only for these radiation schemes: CAM, RRTM, RRTMG, RRTMG_fast`
	- setting ghg_input = 0 in namelist.input
	- failed again - maybe -n 64 is too many? https://forum.mmm.ucar.edu/threads/choosing-an-appropriate-number-of-processors.5082/ 
		- A good **STARTING PLACE** is to use the following equations:  
			For your smallest-sized domain:  
			((e_we)/25) * ((e_sn)/25) = most amount of processors you should use  
			  
			For your largest-sized domain:  
			((e_we)/100) * ((e_sn)/100) = least amount of processors you should use
	- trying again with -n 32, which is a little greater than the starting place above
		- died again - trying to tmux it rather than nohup, jsut in case
	- the tmuxing worked. annoying - maybe it was hanging up despite being nohup'd. 
	- using 32 cores, we took 1.41 hours. that's WILDLY faster than smpar
	- scaling up to 64 cores i am actually seeing no projected improvement.
		- 1.39 hours. interesting.... strong scaling is bad at least with dmpar on this particular problem



### wrf/tq5cmx4 is **smpar**, em_real, nesting=basic
- run using ./wrf.exe
- note high cpu utilization across all cores, low memory usage
currently running smpar, started at 12:50 or so

judging by timestamps, it took a little over five hours. result of time command was not saved (lol) but a watch on wrf proc yields 18009s = 5 hours

![[img/t2_movie.gif]]

![[img/task2-tq.png]]

### wrf/2xtmm6n is dm+sm, yet to be evaluated
https://blog.mylab.cc/2021/02/05/Understanding-MPI-map-by-and-bind-to-option/
maybe necessary: `export PMIX_MCA_psec=^munge`
i had to copy wrfbdy, wrfinput, and all met_em alongside the namelist.input file

```
export OMP_NUM_THREADS=2 
export OMP_PLACES=cores 
export OMP_PROC_BIND=close 
mpirun -np 32 --map-by ppr:16:socket:PE=2 --bind-to core ./wrf.exe
```
note this is Open MPI 4.1.6 - maybe test on other distributions?

1.28 hours


64 ranks x 2 threads (each rank's OpenMP threads share one core's SMT pair)
```
export OMP_NUM_THREADS=2 
OMP_PLACES=threads 
OMP_PROC_BIND=close 
mpirun -np 64 --use-hwthread-cpus --map-by ppr:32:socket:PE=2 --bind-to hwthread ./wrf.exe
```