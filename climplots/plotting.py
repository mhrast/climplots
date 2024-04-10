"""plot timeseries data using matplotlib"""
import matplotlib.pyplot as plt


def timeseries(ds, trend=False):
    """PLots the given timeseries data.

    Args:
        ds: xarray dataarray containing the temperature data.
        trend: if true, ds should be a dataset containing timeseries and trend.
               Then, the timeseries and the trend are plotted, including the
               regression coefficients.
    """
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlabel("$t$ (y)")
    ax.set_ylabel("$T$ (°C)")
    if trend is False:
        print("Plotting data...")
        ax.plot(ds.coords["time"], ds.values, label="values")
    elif trend is True:
        x = ds.coords["time"].dt.year
        p = ds.p.values
        p_err = ds.p_err.values

        print("Plotting data and linear trend...")
        ax.plot(x, ds.t, label="values")
        ax.plot(
            x,
            ds.trend,
            label=r"trend: $T\;(\mathrm{^{\circ}C})=$"
            + f"$({p[0]:.3f}\pm{p_err[0]:.3f})\cdot t$"
            + r"$\;(\mathrm{y})$"
            + f"$ + ({p[1]:.3f}\pm{p_err[1]:.3f})$",
        )
        ax.legend()
    ax.grid()
    plt.show()
