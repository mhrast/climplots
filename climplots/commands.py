import argparse
import sys
import os
from pathlib import Path, PurePath
from . import io, compute, plotting


def climplots():
    """Entry point"""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input-file",
        dest="input_file",
        required=True,
        type=str,
        help="Filepath of input data.",
    )

    parser.add_argument(
        "--latitude-range",
        dest="latitude_range",
        metavar=('LAT_MIN', 'LAT_MAX'),
        nargs=2,
        required=False,
        type=float,
        help="If a netCDF file is read, provide an optional latitude range "
        "seperated by a space, e.g. --latitude-range -90 90 (default)",
    )

    parser.add_argument(
        "--timeseries",
        dest="timeseries",
        required=False,
        action="store_true",
        help="Plot the yearly absolute values.",
    )

    parser.add_argument(
        "--anomalies",
        dest="anomalies",
        required=False,
        action="store_true",
        help="Plot the yearly anomalies.",
    )

    parser.add_argument(
        "--trend",
        dest="trend",
        required=False,
        action="store_true",
        help="Draw a linear trend, optionally.",
    )

    parser.add_argument(
        "--output-file",
        dest="output_file",
        required=False,
        type=str,
        help="Save the plotted data to a netCDF file in the current working "
             "directory, optionally.",
    )

    if len(sys.argv) == 1:
        print("\n  *************************************************************")
        print(" **********************climplots 0.0.0************************")
        print("*************************************************************\n")
        # parser.print_help()
        parser.print_usage()
        print("\nThis program can plot either absolute values or anomalies of "
              "timeseries data from CSV and netCDF files. Type climplots -h "
              "for more information.")
        parser.exit()
    args = parser.parse_args()

    "Error handling"
    if not Path(args.input_file).exists():
        parser.error(f"Input file {args.input_file} does not exist!")
    if PurePath(args.input_file).suffix not in [".csv", ".nc"]:
        parser.error(f"Input file {args.input_file} is neither CSV nor netCDF "
                     "format!")
    if PurePath(args.input_file).suffix == ".csv":
        data = io.load_csv(args.input_file)
    if PurePath(args.input_file).suffix == ".nc":
        if args.latitude_range:
            lat_min = args.latitude_range[0]
            lat_max = args.latitude_range[1]
        else:
            lat_min = -90.0
            lat_max = 90.0
        print(f"Selecting latitudes {lat_min} to {lat_max}...")
        data = io.load_netcdf(args.input_file, lat_min, lat_max)
    if args.output_file and args.output_file[-3:] != ".nc":
        parser.error(f"Output file {args.output_file} must end with .nc!")
    if args.latitude_range and PurePath(args.input_file).suffix != ".nc":
        parser.error("Only netCDF files support a latitude range!")
    if not (args.timeseries or args.anomalies):
        parser.error("Either timeseries or anomalies must be selected!")
    if args.timeseries and args.anomalies:
        parser.error(
            "Either timeseries or anomalies must be selected, not both at the "
            "same time!"
        )

    "Main program"
    if args.timeseries:
        data = data.resample(time="Y").mean(keep_attrs=True)
    if args.anomalies:
        data = compute.anomalies(data).resample(time="Y").mean(keep_attrs=True)
    if args.trend:
        data = compute.linear_trend(data)
    if args.output_file:
        io.save_netcdf(data, os.path.join(os.getcwd(), args.output_file))
    plotting.timeseries(data, trend=args.trend)
