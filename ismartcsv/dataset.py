#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 00:24:36 2020

@author: jeldikk
"""

import abc
import copy
import json
import collections
import numpy as np
from .utilities import str2timestamp, is_increasing, timestamp2str


class dataset(abc.ABC):
    """abstract class defining interfaces to be implemented by deriving classes

    Args:
        abc ([type]): [description]
    """

    @abc.abstractmethod
    def __add__(self, other):
        pass

    @abc.abstractmethod
    def __truediv__(self, val):
        pass

    @abc.abstractmethod
    def to_csv(self):
        pass

    @abc.abstractmethod
    def to_netcdf(self):
        pass

    @abc.abstractmethod
    def to_mat(self):
        pass

    @abc.abstractmethod
    def to_json(self):
        pass



class datafile(dataset):

    # __data = None

    def __init__(self, datalist, config, basename=None, *args, **kwargs):

        # if not config.is_valid():
        #     raise ValueError("Invalid configuration object provided")

        self.__data = collections.OrderedDict()
        self.__bname = basename

        for field in config.field_labels:
            self.__data[field] = list()

        self.__config = config

        if config.timestamp_in_filename:
            if basename is None or config.filename_format is None:
                raise ValueError(
                    "configuation error: either raw_name or filename_format is not provided"
                )
            else:
                self.__tm = str2timestamp(basename, config.filename_format)

        for dict_ele in datalist:
            for field in config.field_labels:
                self.__data[field].append(dict_ele[field])


    @property
    def config(self):
        return self.__config

    @property
    def fields(self):
        return self.__config.field_labels

    @property
    def data(self):
        return self.__data

    @property
    def timestamp(self):

        if not self.config.timestamp_in_filename:
            raise NotImplementedError("timestamp_in_filename field is not defined in the configuration file")

        return self.__tm

    @property
    def basename(self):
        if self.__bname == None:
            raise ValueError("No basename was provided during instantiation")

        return self.__bname

    def __add__(self, other):
        pass

    def __truediv__(self, other):
        pass

    def to_csv(self):
        pass

    def to_netcdf(self):
        pass

    def to_mat(self):
        pass

    def to_json(self):
        pass

    def __len__(self):
        first_label = self.__config.fields[0].name
        return len(self(first_label))

    def __getitem__(self, slc):
        temp_data = collections.OrderedDict()

        for label in self.fields:
            temp_data[label] = copy.copy(np.array(self.__data.get(label))[slc])

        if self.__config.timestamp_in_filename:
            return ismart_chunk(temp_data, self.__tm)
        else:
            return ismart_chunk(temp_data)

    def __call__(self, param):

        if not param in self.config.field_labels:
            raise KeyError("No such field defined in configuation file")

        ind = self.config.field_labels.index(param)

        field_data = self.config[ind]

        if field_data.ftype == 'datetime':
            return self.data.get(param)
        else:
            return np.array(self.data.get(param))

    # def create_interpolater(self, wrt):

    #     if not wrt in self.fields:
    #         raise ValueError("No such field available by name {} ".format(by))

    #     # all(i <= j for i, j in zip(self.data.get(wrt), self.data.get(wrt)[1:])):
    #     if not is_increasing(self.data.get(wrt)):
    #         raise RuntimeError(
    #             "data in {} is not strictly sorted to interpolate".format(wrt)
    #         )

    #     def interp_func(wrt_ticks):
    #         ret_data = collections.OrderedDict()
    #         for field in self.fields:
    #             if field == wrt:
    #                 ret_data[field] = wrt_ticks
    #             else:
    #                 ret_data[field] = np.interp(
    #                     wrt_ticks,
    #                     self(wrt),
    #                     self(field),
    #                     left=np.NaN,
    #                     right=np.NaN
    #                 )
    #         if self.__config.timestamp_in_filename:
    #             return ismart_chunk(ret_data, self.__tm)
    #         else:
    #             return ismart_chunk(ret_data)

    #     return interp_func

    def _to_user_interface(self, limits):

        item_list = list()
        for ind in range(len(self)):
            item = dict()
            for field in self.__config.fields:
                if field.ftype == 'float':
                    item[field.name] = round(self(field.name)[ind], 4)
                elif field.ftype == 'datetime':
                    item[field.name] = timestamp2str(
                        self(field.name)[ind], self.__config.datetime_format)
            if ind < limits['asc_start']:
                item['traverse'] = 's'
            elif limits['asc_start'] <= ind <= limits['dsc_start']:
                item['traverse'] = 'a'
            elif ind > limits['dsc_start']:
                item['traverse'] = 'd'

            item_list.append(item)

        return item_list


class datafolder(dataset):
    __data = None

    def __init__(self, foldername, config, *args, **kwargs):
        pass

    def __add__(self, other):
        pass

    def __truediv__(self, other):
        pass

    def to_csv(self):
        pass

    def to_netcdf(self):
        pass

    def to_mat(self):
        pass

    def to_json(self):
        pass


# class ismart_chunk(object):

#     def __init__(self, dict_chunk, timestamp=None, *args, **kwargs):

#         if not isinstance(dict_chunk, collections.OrderedDict):
#             raise ValueError("improper data chunk provided")

#         self._data = dict_chunk
#         self._labels = tuple(key for key in self._data.keys())

#         if not timestamp is None:
#             self.__tmstamp = timestamp

#     @property
#     def timestamp(self):
#         try:
#             return self.__tmstamp
#         except:
#             raise AttributeError("timestamp is not set in filename")

#     @property
#     def fields(self):
#         return self._labels

#     def __getattr__(self, label):
#         if label in self._labels:
#             return self._data.get(label)
#         else:
#             raise AttributeError("No key with name {} available".format(label))

#     def __call__(self, label):
#         if label in self._labels:
#             return self._data.get(label)
#         else:
#             raise KeyError("No key with name {} availabel".format(label))

#     def save_mat(self, filename):
#         pass

#     def save_csv(self, filename):
#         pass

#     def to_csv(self):
#         pass

#     def to_json():
#         pass
