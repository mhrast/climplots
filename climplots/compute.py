"""Compute monthly anomalies and linear trend"""
import numpy as np
import xarray as xr


def anomalies(ds, ref_period_start="1991-01-01", ref_period_end="2020-12-31"):
    """Computes the monthly anomalies relative to the given reference period.

    Args:
        ds: xarray dataarray containing the temperature data.
        ref_period_start: start date of the reference period.
        ref_period_end: end date of the reference period.

    Returns: xarray dataarray containing the anomalies.
    """
    print("Computing anomalies...")
    clim = (
        ds.sel(time=slice(ref_period_start, ref_period_end))
        .groupby("time.month")
        .mean(keep_attrs=True)
    )
    monthly_means = ds.groupby("time.month")

    anom = monthly_means - clim
    return anom


def linear_trend(ds):
    """Computes the linear trend of the given timeseries data, using numpy's
       polyfit.

    Args:
        ds: xarray dataarray containing the timeseries data.

    Returns: xarray dataset containing the timeseries, the trend and the
             fitting coefficients/uncertainties.
    """
    print("Computing linear trend...")
    ds = ds.resample(time="Y").mean(keep_attrs=True)

    x = ds.coords["time"].dt.year
    y = ds.values
    reg = np.polyfit(x, y, 1, cov=True, full=False)

    p = reg[0]
    c_p = reg[1]
    p_err = np.sqrt(np.diag(c_p))

    p = xr.DataArray(p, dims="i")
    p.attrs["info"] = "coefficients of linear trend"

    p_err = xr.DataArray(p_err, dims="i")
    p_err.attrs["info"] = "coefficient uncertainties of linear trend"

    ds = ds.to_dataset()
    ds = ds.assign(trend=p[0] * x + p[1], p=p, p_err=p_err)

    return ds


def linear_trend_xarray(ds):
    """Computes the linear trend of the given timeseries data, using polyfit
       internally in xarray. Currently not used in the program, since the
       coefficients have unknown values.

    Args:
        ds: xarray dataarray containing the timeseries data.

    Returns: xarray dataset containing the timeseries, the trend and the
             fitting coefficients/uncertainties.
    """
    print("Computing linear trend...")
    ds = ds.resample(time="Y").mean(keep_attrs=True)

    coeff = ds.polyfit(dim="time", deg=1, full=False, cov=True, skipna=True)

    p = coeff.polyfit_coefficients.values
    p_err = np.sqrt(np.diag(coeff.polyfit_covariance))

    trendval = xr.polyval(ds.coords["time"], coeff)

    ds = ds.to_dataset()
    ds = ds.assign(trend=trendval.polyfit_coefficients)

    return ds, p, p_err
