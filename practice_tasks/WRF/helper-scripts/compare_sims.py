import argparse
import glob
from datetime import datetime

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from netCDF4 import Dataset, chartostring


def load_domain(run_dir, domain="d01"):
    """Return lat, lon, T2 in deg C (nt, ny, nx), list of datetimes, projection attrs."""
    files = sorted(glob.glob(f"{run_dir}/wrfout_{domain}_*"))
    if not files:
        raise FileNotFoundError(f"No wrfout_{domain}_* files in {run_dir}")

    with Dataset(files[0]) as nc:
        lat = np.asarray(nc.variables["XLAT"][0, :, :])
        lon = np.asarray(nc.variables["XLONG"][0, :, :])
        proj = dict(cen_lat=float(nc.CEN_LAT),
            stand_lon=float(nc.STAND_LON),
            truelat1=float(nc.TRUELAT1))
    t2, times = [], []
    for f in files:
        with Dataset(f) as nc:
            t2.append(np.asarray(nc.variables["QVAPOR"][:, 0, :, :]))
            for s in chartostring(nc.variables["Times"][:]):
                times.append(datetime.strptime(str(s), "%Y-%m-%d_%H:%M:%S"))
    t2 = np.concatenate(t2, axis=0)
    return lat, lon, t2, times, proj


def add_map_features(ax):
    ax.add_feature(cfeature.COASTLINE.with_scale("50m"), linewidth=0.6)
    ax.add_feature(cfeature.STATES.with_scale("50m"), linewidth=0.4, edgecolor="k")
    ax.add_feature(cfeature.BORDERS.with_scale("50m"), linewidth=0.5)
    ax.add_feature(cfeature.LAKES.with_scale("50m"), facecolor="none",
                   edgecolor="k", linewidth=0.5)
    gl = ax.gridlines(draw_labels=True, linewidth=0.3, color="gray", alpha=0.6)
    gl.top_labels = gl.right_labels = False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir_1")
    ap.add_argument("run_dir_2")
    ap.add_argument("--out", default="qvapor_delta.mp4")
    ap.add_argument("--fps", type=int, default=6)
    ap.add_argument("--dpi", type=int, default=120)
    args = ap.parse_args()

    lat, lon, t2, times, proj = load_domain(args.run_dir_1)
    lat2, lon2, t22, times2, proj2 = load_domain(args.run_dir_2)
    # Fixed color scale so all frames are comparable
    
    t2 = (t22 - t2)
    
    vmin, vmax = t2.min(), t2.max()

    pc = ccrs.PlateCarree()  # lat/lon data CRS
    mapproj = ccrs.Mercator(central_longitude=proj["stand_lon"],
                            latitude_true_scale=proj["truelat1"])

    fig = plt.figure(figsize=(9, 7))
    ax = fig.add_subplot(1, 1, 1, projection=mapproj)
    xyz = mapproj.transform_points(pc, lon, lat)   # mapproj = your Mercator CRS
    ax.set_xlim(np.nanmin(xyz[..., 0]), np.nanmax(xyz[..., 0]))
    ax.set_ylim(np.nanmin(xyz[..., 1]), np.nanmax(xyz[..., 1]))
    mesh = ax.pcolormesh(lon, lat, t2[0], transform=pc, cmap="turbo",
                         vmin=vmin, vmax=vmax, shading="nearest")
    add_map_features(ax)
    ax.set_title("Difference between sim 2 (with NARR boundary conditions) and sim 1 (with NAM boundary conditions)")

    cbar = fig.colorbar(mesh, ax=ax, orientation="horizontal",
                        fraction=0.05, pad=0.08)
    cbar.set_label("Difference (sim2 - sim1) of QVAPOR; kilograms of water vapor per kilogram of dry air")
    suptitle = fig.suptitle("", fontsize=14)

    def update(k):
        mesh.set_array(t2[k].ravel())
        suptitle.set_text(f"Simulated QVAPOR delta |  {times[k]:%Y-%m-%d %H:%M} UTC")
        return [mesh]

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