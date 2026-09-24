- Located in ~/Applications/MFC
- Installed and used nvhpc 
	- to access, `source ~/util/nvhpc.sh`
- apt installed python3, cmake
- maybe necessary - if they are, will add to the setup script
	- `export FC=nvfortran`
	- `export CC=nvc`
	- `export CXX=nvc++`

## Problem 1: tests
- MPI was encountering issues with `ulimit -l` so I ran `export UCX_TLS=tcp,self,sm` before re-running the test suite. Yet to be seen if this has an impact on performance
	- With this change, the CPU-only tests pass
	- CPU utilization is low when running test - max observed was 20%
- The current installation's GPU test should be run using --gpu acc
	- had to do this: `export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/nvidia/hpc_sdk/Linux_x86_64/26.5/math_libs/lib64`
	- all tests yield OOM errors (even though the dashboard doesn't show that any GPU memory is in use)
		- tried using --gpu mp but got the same errors
	- Rebooting the node using `sudo reboot`
		- taking a while. let's not do this during competition lol**
Solution 1: MFC requires lower version of nvhpc. we tried version 25.7 and it worked; however, we need to consider what the recommended version is? (ask the SCC organizer?)
