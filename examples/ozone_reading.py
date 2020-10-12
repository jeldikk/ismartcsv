import os
import numpy as np
import datetime

from ismartcsv import read_file, read_folder


def datetime_parser(arg, format):
    hrs, mins, secs = arg.split(':')
    # python does not take simple datetime.time object to plot, so I took this workaround from this stackoverflow thread
    # https://stackoverflow.com/questions/32832431/how-to-use-datetime-time-to-plot-in-python/47059651

    return datetime.datetime.combine(datetime.date.today(),datetime.time(int(hrs), int(mins), int(secs)))

def datetime_encoder(arg, format):
    if format is None:
        return arg.strftime("%H:%M:%S")
    else:
        return arg.strftime(format)

def filename_parser(arg, format):
    # print(arg)
    if format is None:
        return datetime.datetime.strptime(arg[5:12], "%Y%m%d")
    else:
        return datetime.datetime.strptime(arg, format)

def filename_encoder(arg, format):
    if format is None:
        return arg.strftime("NewFile%Y%m%d")
    else:
        return arg.strftime(format)

options = {
    'DATETIME_PARSER': datetime_parser,
    'DATETIME_ENCODER': datetime_encoder,
    'FILENAME_PARSER': filename_parser,
    'FILENAME_ENCODER': filename_encoder
}

config_filename = "./assets/configurations/ozo_rs_config.yml"
# ozone_filename = os.path.abspath(
#     "../data/datafolder/RS/ozone_sonde/se_1_20191225_1130.csv")
ozone_filename = "./full_data/datafolder/RS/ozone_sonde/se_1_20191225_1130.csv"
# config = config_parser.config_file(config_filename)
# with open(gps_filename, "r") as filep:
#     gps = dataset.datafile(filep, config)

dfile = read_file(ozone_filename, config_filename, **options)

chunk = dfile[10:1000]
chunk.to_csv("path/to/desktop/somefilename.csv")

new_chunk = dfile[10:100]
new_chunk.to_csv("path/to/folder/where/file/to/be/stored/")
# dfile.plot()

