## What is WRF
- research and forecasting tool for:
	- idealized simulations
	- experimental real-time forecast
	- other stuff: WRF-Fire, WRF-Hydro

## The Model
### Lateral boundary conditions
- can't do hi-res simulation of the globe - set over the region (limited area model)
- this region needs to know what's happening immediately outside of it - use either global models or reanalysis (?) data to determine this
### Model nesting
- Larger outer domain - decrease the domain size and decrease the grid spacing as you move closer to the relevant area
- Done to obtain high resolution model solutions efficiently
### Model grid
- computation done on grid, then interpolated

## Workflow
### WPS: preprocessing
- geogrid: defines map projection, location of domains, dimensions of domains, horizontal resolution
	- also provides values for static fields at each grid point and interpolates them 
- **namelist.wps**: user-specified runtime options
	- columns correspond to domains 
	- set time range: start_date, end_date
- ungrib
	- GRIB is a file format for storing gridded fields. compressed lossily
	- fields are identified by code numbers which are cross-referenced against external tables
	- ungrib writes data to intermediate file format
- metgrid
	- horizontally interpolates meteorological data (from ungrib) to simulation domains (from geogrid)
	- output: met_em files (netCDF)
	- after running metgrid, this is a good place to stop and visualize the files - is it reasonable?
### WRF
- namelist.input for WRF (rather than .wps for WPS)