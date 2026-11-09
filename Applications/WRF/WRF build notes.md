[swmgr@login1 wrf]$ echo $NETCDF

/netcdf

[swmgr@login1 wrf]$ export DIR=$PWD/wrf_dependencies

[swmgr@login1 wrf]$ source wrf_envs 

[swmgr@login1 wrf]$ echo $NETCDF

/packages/wrf/wrf_dependencies/netcdf

[swmgr@login1 wrf]$

**Now close the current terminal window, and open a new one. Environment variables set earlier will no longer be set. In the new terminal window, open up the .bashrc (or similar) file and and or edit the following entries. When done, save the file.**
stopping at above and continuing with rest of main page

LOAD THE RIGHT GCC AFTER EXITING!

git clone --recurse-submodules https://github.com/wrf-model/WRF

[swmgr@login1 WRF]$ ./compile em_real >& log.compile

it's using the wrong cpp it looks like.