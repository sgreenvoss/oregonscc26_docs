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

### WRF