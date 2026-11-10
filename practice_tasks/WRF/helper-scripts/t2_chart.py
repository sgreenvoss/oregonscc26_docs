# Creates a line chart from simulated and measured data
# conda activate wrf_env2 for these libs

import matplotlib.pyplot as plt
import pandas as pd
from netCDF4 import Dataset
from wrf import ll_to_xy, getvar
import glob 
import datetime

f = "south_bend_temperature_Jan28_31_2019_observed.csv"
target_lat, target_lon = 41.7, -86.2
df = pd.read_csv(f)

df['simulated-temp'] = 0.0
df['sim-d2'] = 0.0
print(df)
files = glob.glob("./wrfout-tq/*")
files.sort()
times = len(files) // 2 # this is stupid

for i in range(times):
    print(files[i], files[i+times], df.iloc[i], "\n")
    ncfile = Dataset(files[i])
    dom_2 = Dataset(files[i + times])
    x_idx, y_idx = ll_to_xy(ncfile, target_lat, target_lon, as_int=True)
    x2, y2 = ll_to_xy(dom_2, target_lat, target_lon, as_int=True)

    t2 = getvar(ncfile, "T2")
    t2_d2 = getvar(dom_2, "T2")
    temp = t2.isel(west_east=x_idx, south_north=y_idx) #index selection (xarray)
    temp_2 = t2_d2.isel(west_east=x2, south_north=y2) 

    df.iat[i, -2] = temp.values - 273.15
    df.iat[i, -1] = temp_2.values - 273.15

stop_cond = (df["simulated-temp"] == 0.0).idxmax()
df = df.iloc[:stop_cond]

base_time = datetime.datetime(2019, 1, 28, 0, 0, 0)
x_times = [base_time + datetime.timedelta(hours=i) for i in range(times)]
fig, ax = plt.subplots(figsize=(8,6))
ax.plot(x_times, df['T_C'], label="Measured temperatures", marker='o', color='blue')
ax.plot(x_times, df['simulated-temp'], label="Domain 1", marker='x', color='red')
ax.plot(x_times, df['sim-d2'], label="Domain 2", marker='*', color='pink')
ax.set_xlabel("Time")
ax.set_ylabel("2m temperature (Celsius)")
plt.title("Simulated vs Measured Temperature")
ax.legend()

plt.savefig("task2.png")