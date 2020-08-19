# -*- coding: utf-8 -*-

import os
import sys
from .dataset import datafile
from .config_parser import config_file
from .plotting import plot_line


# __all__ = ['config_file', 'plot_line', 'datafile']


def read_file(data_filename, config_filename):

    if not os.path.isfile(data_filename):
        raise TypeError("read_file accepts only filename but got something else")

    config = config_file(config_filename)

    if config.is_valid():
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

                    try:
                        if field.ftype == 'int':
                            val = int(samp_txt)
                        elif field.ftype == 'float':
                            val = float(samp_txt)
                        elif field.ftype == 'datetime':
                            val = str2timestamp(samp_txt,config.datetime_format)
                        else:
                            raise TypeError(f"ftype error: no such {field.ftype} field type defined")
                    except TypeError as type_error:
                        print(type_error)
                        sys.exit(-1)
                    except:
                        val = field.ifnull # keeping ifnull value if the parsing throws an exception
                    finally:
                        sample_dict[field.name] = val

                dict_list.append(sample_dict)
        return datafile(dict_list,config,os.path.basename(data_filename))
    else:
        raise ValueError("Invalid configuration file settings.")


def read_folder(folder_name, config_filename):
    pass

def read_netcdf(filename,config_filename):
    pass