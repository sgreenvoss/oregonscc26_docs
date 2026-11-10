#!/usr/bin/env python3
"""
Task 1: movie of 2 m temperature (T2) for WRF domains d01 (9 km) and d02 (3 km).

Usage:
    python make_t2_movie.py /path/to/wrf/run_dir --out t2_movie.mp4

Requires: numpy, matplotlib, netCDF4, cartopy, and ffmpeg (falls back to GIF).
"""
import argparse
import glob
from datetime import datetime, timedelta

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from netCDF4 import Dataset, chartostring

SBN_LAT, SBN_LON = 41.7087, -86.3173   # South Bend Intl Airport (KSBN)
EST_OFFSET = timedelta(hours=-5)        # local standard time, for the title


def load_domain(run_dir, dom):
    """Return lat, lon, T2 in deg C (nt, ny, nx), list of datetimes, projection attrs."""
    files = sorted(glob.glob(f"{run_dir}/wrfout_d{dom:02d}_*"))
    if not files:
        raise FileNotFoundError(f"No wrfout_d{dom:02d}_* files in {run_dir}")

    with Dataset(files[0]) as nc:
        lat = nc.variables["XLAT"][0, :, :]
        lon = nc.variables["XLONG"][0, :, :]
        proj = dict(cen_lat=nc.CEN_LAT, stand_lon=nc.STAND_LON,
                    truelat1=nc.TRUELAT1, truelat2=nc.TRUELAT2)

    t2, times = [], []
    for f in files:
        with Dataset(f) as nc:
            t2.append(np.asarray(nc.variables["T2"][:]))           # (nt, ny, nx), K
            for s in chartostring(nc.variables["Times"][:]):
                times.append(datetime.strptime(str(s), "%Y-%m-%d_%H:%M:%S"))
    t2 = np.concatenate(t2, axis=0) - 273.15
    return np.asarray(lat), np.asarray(lon), t2, times, proj


def add_map_features(ax):
    ax.add_feature(cfeature.COASTLINE.with_scale("50m"), linewidth=0.6)
    ax.add_feature(cfeature.STATES.with_scale("50m"), linewidth=0.4, edgecolor="k")
    ax.add_feature(cfeature.LAKES.with_scale("50m"), facecolor="none",
                   edgecolor="k", linewidth=0.5)
    gl = ax.gridlines(draw_labels=True, linewidth=0.3, color="gray", alpha=0.6)
    gl.top_labels = gl.right_labels = False


def box_outline(lat, lon):
    """Lon/lat of the outer edge of a grid (to draw the nest on the parent)."""
    lons = np.concatenate([lon[0, :], lon[:, -1], lon[-1, ::-1], lon[::-1, 0]])
    lats = np.concatenate([lat[0, :], lat[:, -1], lat[-1, ::-1], lat[::-1, 0]])
    return lons, lats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir")
    ap.add_argument("--out", default="t2_movie.mp4")
    ap.add_argument("--fps", type=int, default=6)
    ap.add_argument("--dpi", type=int, default=120)
    args = ap.parse_args()

    lat1, lon1, t2_1, times1, proj = load_domain(args.run_dir, 1)
    lat2, lon2, t2_2, times2, _ = load_domain(args.run_dir, 2)
    assert times1 == times2, "d01 and d02 time axes differ; check history_interval"
    times = times1

    # Shared color scale so the two panels (and all frames) are comparable
    vmin = np.floor(min(t2_1.min(), t2_2.min()))
    vmax = np.ceil(max(t2_1.max(), t2_2.max()))

    lcc = ccrs.LambertConformal(central_longitude=proj["stand_lon"],
                                central_latitude=proj["cen_lat"],
                                standard_parallels=(proj["truelat1"], proj["truelat2"]))
    pc = ccrs.PlateCarree()

    fig = plt.figure(figsize=(14, 6.5))
    axes, meshes = [], []
    for i, (lat, lon, t2, name) in enumerate(
            [(lat1, lon1, t2_1, "d01 (9 km)"), (lat2, lon2, t2_2, "d02 (3 km)")]):
        ax = fig.add_subplot(1, 2, i + 1, projection=lcc)
        ax.set_extent([lon.min(), lon.max(), lat.min(), lat.max()], crs=pc)
        m = ax.pcolormesh(lon, lat, t2[0], transform=pc, cmap="turbo",
                          vmin=vmin, vmax=vmax, shading="nearest")
        add_map_features(ax)
        ax.plot(SBN_LON, SBN_LAT, marker="*", color="white", markeredgecolor="k",
                markersize=14, transform=pc, zorder=5)
        ax.set_title(name)
        axes.append(ax)
        meshes.append(m)

    # Outline the nest on the parent panel
    bx, by = box_outline(lat2, lon2)
    axes[0].plot(bx, by, color="k", linewidth=1.5, transform=pc, zorder=4)

    cbar = fig.colorbar(meshes[0], ax=axes, orientation="horizontal",
                        fraction=0.05, pad=0.08)
    cbar.set_label("2 m temperature (°C)")
    suptitle = fig.suptitle("", fontsize=14)

    def update(k):
        meshes[0].set_array(t2_1[k].ravel())
        meshes[1].set_array(t2_2[k].ravel())
        utc = times[k]
        loc = utc + EST_OFFSET
        suptitle.set_text(f"WRF T2  |  {utc:%Y-%m-%d %H:%M} UTC  ({loc:%d %b %H:%M} EST)")
        return meshes

    anim = animation.FuncAnimation(fig, update, frames=len(times), blit=False)

    if args.out.endswith(".mp4") and animation.writers.is_available("ffmpeg"):
        writer = animation.FFMpegWriter(fps=args.fps, bitrate=4000)
        anim.save(args.out, writer=writer, dpi=args.dpi)
    else:
        out = args.out.rsplit(".", 1)[0] + ".gif"
        anim.save(out, writer=animation.PillowWriter(fps=args.fps), dpi=args.dpi)
        args.out = out
    print(f"Wrote {args.out} ({len(times)} frames, {vmin:.0f} to {vmax:.0f} °C)")


if __name__ == "__main__":
    main()
