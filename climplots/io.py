"""Import csv and netCDF files"""
import pandas as pd
import xarray as xr


def load_csv(fn):
    """Reads temperature data from file, assuming ZAMG CSV format.

    Args:
        fn: Filename of file containing the data.

    Returns: xarray dataarray containing the temperature data.
    """
    df = pd.read_csv(fn, parse_dates=["time"], index_col="time")
    ds = df.to_xarray()
    return ds.t.sel(time=slice("1922-01-01", "2021-12-31"))


def load_netcdf(fn, lat_min=-90, lat_max=90):
    """Reads temperature data from file, assuming WN netCDF format.

    Args:
        fn: Filename of file containing the data.
        lat_min: minimum latitude, default value is -90°.
        lat_max: maximum latitude, default value is +90°.

    Returns: xarray dataarray containing the temperature data.
    """
    with xr.open_dataset(fn) as ds:
        ds.load()
    ds = ds.sel(latitude=slice(lat_min, lat_max))
    ds = ds.rename({"temperature_2_meter": "t"})
    return ds.t.mean(dim=("latitude", "longitude"), keep_attrs=True) - 273.15


def save_netcdf(ds, fn):
    """Saves timeseries/anomalies and optional fit data in a netCDF file in the
       current working directory.

    Args:
        ds: xarray dataset containing the data.
        fn: Filename of file to be saved. Must end with .nc.
    """
    print(f'Saving data to "{fn}"...')
    ds.attrs["unit"] = "°C"
    ds.to_netcdf(fn)
