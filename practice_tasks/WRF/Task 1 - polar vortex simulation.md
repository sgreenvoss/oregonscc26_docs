**WRF – SCC26 Polar Vortex Assignment Test Case**

**Event:** Polar Vortex Instability, Winter 2019

**Simulation Period:** 28–30 January 2019

**Description of event:** A large area of low pressure and extremely cold air usually swirls over the Arctic, with strong counter-clockwise winds that trap the cold around the Pole. Disturbances in the jet stream and the intrusion of warmer mid-latitude air masses can disturb this polar vortex and make it unstable, sending Arctic air south into mid-latitudes. This was the case in late January 2019.


27 January 2019, MODIS-Terra


**Domain & Resolution**

**Domain 1:**

●      **Domain Center:** South Bend (41.7° N, 86.2° W)

●      **Domain Size:** 150 × 150 cells

●      **Spatial Resolution:** 9 km

●      **Map Projection:** Lambert

●      **Vertical Levels:** 50 vertical levels (e_vert = 50)

●      Timestep for physics = 10 s 

●      Set debug level to 50

**Domain 2:**

●      **Spatial Resolution**: 3 km for nest

●      **Domain size**: 100 × 100 cells

●      **Vertical Levels:** 50 vertical levels (e_vert = 50)

●      Timestep for physics = 10 s 

●      Set debug level to 50

From the docs: If you are unsure about the number of levels your data has, you can use the following command:  
ncdump -h met_em.d01.\<date\> >& log.ncdump  
and look for the value near the top of the log.ncdump file.


**Data Provided**

●      **Meteorological Boundary Conditions:** North American Mesoscale (NAM) model at 12 km resolution (Located at [https://www.nco.ncep.noaa.gov/pmb/products/nam/](https://www.nco.ncep.noaa.gov/pmb/products/nam/))
- I couldn’t find data from 2019 here, so eventually I used GDEX to access historical data: https://gdex.ucar.edu/datasets/d609000/dataaccess/#201901anl

●      **Geographical Input Data:**
- For an easier link: [**https://www2.mmm.ucar.edu/wrf/users/download/get_sources_wps_geog.html**](https://www2.mmm.ucar.edu/wrf/users/download/get_sources_wps_geog.html)

o   **Let’s run one sim with the highest resolution tar and one with the lowest and compare resource usage/quality**

●      **Observations:** SBN Airport weather station observations: attached csv file

●      **Physics options:** https://www2.mmm.ucar.edu/wrf/users/wrf_users_guide/build/html/physics.html


**Table 1. Summary of Model & Physics Setup to use**

|   |   |   |
|---|---|---|
|**Physics**|**Scheme**|**Option number (I think)**|
|Microphysics|WRF Single-Moment 5-class|mp_physics=4|
|Longwave Radiation|RRTM|ra_lw_physics=1|
|Shortwave Radiation|Goddard|ra_sw_physics=2|
|Surface Layer|Monin Obhukov similarity|? unclear if MM5 or eta, assume eta: sf_sfclay_physics=2|
|Land Surface|Noah Land Surface Model|sf_surface_physics=2|
|Planetary Boundary Layer|Mellor-Yamada_janjic|bl_pbl_physics=2|
|Cumulus Parameterization|Grell 3|cu_physics=5|


**Setting up namelist:** [**https://www2.mmm.ucar.edu/wrf/users/namelist_best_prac_wrf.html#p_top_requested**](https://www2.mmm.ucar.edu/wrf/users/namelist_best_prac_wrf.html#p_top_requested)

**Tasks**

1. **Spatio-Temporal Visualization:** Produce a movie showing the spatio-temporal evolution of 2m temperatures over the two domains.

![[practice_tasks/WRF/img/t2_movie.gif]]

2. **Time Series Comparison:** Plot the simulated (2m) surface temperature time series over South Bend and compare it against the weather station observations at SBN airport for both domains.

![[practice_tasks/WRF/img/task2-tq.png]]

3. **Compare output from both domains/resolutions:** Compare the output from both domains at South Bend and quantify the differences with basic statistics (RMSE and Mean-bias error). Explain possible sources of differences and which resolution performed best.

RMSE for d1 is 1.955 degrees Celsius

RMSE for d2 is 1.909 degrees Celsius

