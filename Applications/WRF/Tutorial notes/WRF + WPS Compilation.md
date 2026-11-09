[The video ](https://www.youtube.com/watch?v=zenCyRD08EE&list=PLJ_1sjucSSZCTNBRM4D3BfEak-XT7TKJo&index=10) links to this page https://www2.mmm.ucar.edu/wrf/OnLineTutorial/compilation_tutorial.php

## Libraries
NetCDF is the only required library; MPI needed for parallel, jasper, png, zlib needed for grib2. 

Must install all libraries using the same compilers.

## Configuration
- Distributed option is recommended (dmpar)
- can use flags: ./configure -d does not optimize, debugs
- multiple processor compilation: setenv J "-j 2"
## Compilation
./compile em_case >& log.compile

for real data: em_real

- Use log.compile to search for 'Error'. FAQ on the WRF support forum should help
- clean -a when reconfiguring and recompiling. Should be used when modifications have been made to configure.wrf.
i added the /include folder of netcdf to cpath


remember to source the env variables every time
edit namelist.wps to reflect the date and time of the data
