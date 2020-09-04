# -*- coding: utf-8 -*-

import os
import sys
import numpy as np
from .dataset import datafile, datafolder
from .configuration import config_file
from .plotting import plot_line
from .utilities import str2timestamp, create_file_interpolator
from .formatters import formatter


# __all__ = ['config_file', 'plot_line', 'datafile']


def read_file(data_filename, config_filename,**kwargs):

    if not os.path.isfile(data_filename):
        raise TypeError("read_file accepts only filename but got something else")

    config = config_file(config_filename, **kwargs)

    if not config.is_valid():
        raise ValueError("Invalid configuration")

    
    # if config.is_valid():
    with open(data_filename,"r") as filep:

        for _ in range(config.skip_lines):
            filep.readline()

        dict_list = list()

        while True:
            line = filep.readline()

            if len(line) == 0:
                break

            line_split = line.strip().split(config.delimiter)
            line_split = [line.strip() for line in line_split]

            if not all([line_split[field.colno - 1] != field.nullval for field in config.fields]):
                continue

            sample_dict = dict()

            for ind, field in enumerate(config.fields):

                samp_txt = line_split[field.colno-1]
                # print(field.ftype)
                try:
                    # print('before making formatter')
                    fmter = formatter.make_formatter(field.ftype, config.datetime_format)
                    # print('fmter is ',fmter)
                    val = fmter.parse(samp_txt)
                    # print(f'The value in readfile: {val}')
                    # if field.ftype == 'int':
                    #     val = int(samp_txt)
                    # elif field.ftype == 'float':
                    #     # print('I am here in float')
                    #     val = float(samp_txt)
                    # elif field.ftype == 'datetime':
                    #     # print("I am in datetime")
                    #     val = str2timestamp(samp_txt,config.datetime_format)
                    #     # print("I am here in timestamp")
                    #     # print(val)
                    # else:
                    #     raise TypeError(f"ftype error: no such {field.ftype} field type defined")
                except Exception as ex:
                    print(ex)
                    val = field.ifnull
                finally:
                    # print(f'The value in readfile: {val}')
                    sample_dict[field.name] = val * field.factor

            dict_list.append(sample_dict)

    return datafile(dict_list,config,os.path.basename(data_filename))
    # else:
    #     raise ValueError("Invalid configuration file settings.")






def read_folder(folder_name, config_filename):

    if not os.path.isdir(folder_name):
        raise TypeError("read_folder accepts only folder but got something else")

    config = config_file(config_filename)

    if not config.is_valid():
        raise ValueError("configuration cannot be validated")

    # if config.is_valid():

    if config.is_interpolatable():
        try:
            start = config.interpolation['start']
            stop = config.interpolation['stop']
            step = config.interpolation['step']
        except:
            raise ValueError("Interpolation configurations needs start, stop, step fields for uniformity")
    else:
        raise ValueError("interpolation config section is missing, please add for handling folder")


    filenames = os.listdir(folder_name)
    dflist = list()
    pivot_values = np.arange(start,stop,step)
    for filename in filenames:
        dfile = read_file(os.path.join(folder_name,filename),config_filename)
        interp = dfile.get_interpolator()
        # interp = create_file_interpolator(dfile, config.interpolation['pivot'])
        temp_dfile = interp(np.arange(start,stop,step))
        dflist.append(temp_dfile)
    
    return datafolder(dflist,pivot_values,config,filename)
            
    # else:
    #     raise ValueError("Invalid configuration file settings.")

# def read_netcdf(filename,config_filename):
#     pass