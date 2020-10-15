#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: jeldikk
"""
import os
import sys
import abc
import copy
import csv
import json
import collections
import numpy as np

from .formatters import formatter
from .configuration import config_file
from .utilities import str2timestamp, is_increasing, timestamp2str
from .plotting import plot_file, plot_folder


class dataset(abc.ABC):
    """abstract class defining interfaces to be implemented by deriving classes

    Args:
        abc ([type]): [description]
    """

    # @abc.abstractmethod
    # def __add__(self, other):
    #     pass

    # @abc.abstractmethod
    # def __truediv__(self, val):
    #     pass

    @abc.abstractmethod
    def to_csv(self, filename):
        pass

    @abc.abstractmethod
    def to_netcdf(self, filename):
        pass

    @abc.abstractmethod
    def to_mat(self, filename):
        pass

    @abc.abstractmethod
    def to_json(self):
        pass

    @abc.abstractmethod
    def plot(self):
        pass


class datafile(dataset):


    def __init__(self, datalist, config, basename=None, *args, **kwargs):

        self.__data = collections.OrderedDict()
        self.__bname = basename
        self.__length = len(datalist)

        for field in config.field_labels:
            self.__data[field] = list()

        self.__config = config

        # if config.timestamp_in_filename:
        if basename is None:
            # print(basename,'/',config.filename_format)
            raise ValueError(
                "configuation error: base filname is missing for parsing filestamp"
            )
        else:
            # self.__tm = str2timestamp(basename, config.filename_format)
            # print('basename in datafile:',basename)
            # print(config.file_formatter)
            self.__tm = config.filestamp_formatter.parse(basename)
                # print(self.__tm)

        for dict_ele in datalist:
            for field in config.field_labels:
                self.__data[field].append(dict_ele[field])

    def __del__(self):
        """
        destructor of datefile class instance
        """
        del self.__data
        # del self.__config

    @property
    def config(self):
        """getter property of datafile instance pointing to config_file instance

        Returns:
            config_file: instance of config_file of ismartcsv.configuration
        """
        return self.__config

    @property
    def fields(self):
        """getter property of datafile instance

        Returns:
            list: list of field names defined in fields config section
        """
        return self.__config.field_labels

    @property
    def data(self):
        """getter property of datafile instance

        Returns:
            OrderedDict: OrderedDict container with all field names as keys and data as values
        """
        return self.__data

    @property
    def filestamp(self):
        """getter property useful for referencing the datafile instance, this is useful for creating datafolder object

        Returns:
            [type]: [description]
        """

        # if not self.config.timestamp_in_filename:
        #     raise NotImplementedError(
        #         "timestamp_in_filename field is not defined in the configuration file")

        return self.__tm

    @property
    def basename(self):
        if self.__bname == None:
            raise ValueError("No basename was provided during instantiation")

        return self.__bname


    def __len__(self):

        """get the number of valid samples recorded from the file

        Returns:
            int: Length of data of each field
        """

        return self.__length


    def __getitem__(self, slc):
        
        if isinstance(slc,int):

            if slc > self.__length:
                raise IndexError(f"index: {slc} is out of range")

            item = dict()
            for field in self.__config.field_labels:
                item[field] = self.__data[field][slc]
            return item

        elif isinstance(slc,slice):
            
            dtlist = list()
            start,stop,step = slc.indices(self.__length)
            
            for index in range(start,stop,step):
                item = self[index]
                dtlist.append(item)

            return datafile(dtlist,self.__config,self.__bname)


    def add_fielddata(self, dataarr, field_spec):
        pass


    def get_interpolator(self,pivot=None):
        
        """A Closure which returns a interpolator function drived out of instance created

        Arguments:
            instance {datafile or ismart_chunk} -- instances whose classes define fields and __call__ methods
            wrt {[type]} -- [description]

        Raises:
            ValueError: wrt argument should be one of the fields defined in instance object
            RuntimeError: if the wrt fields values are not in increasing order this is raised

        Returns:
            [dataset.datafile] -- datafile object with interpolated values derived 
        """
        if pivot is None:
            if not self.__config.is_interpolatable():
                raise AssertionError("No pivot label provided in config file or as argument")
            else:
                pivot = self.__config.interpolation.get('pivot')

        if not pivot in self.fields:
            raise ValueError(f"{pivot} field not found in configured labels")

        if not is_increasing(self(pivot)):
            raise RuntimeError(f"data of field {pivot} is not in increasing order")

        def file_interp_func(wrt_ticks):

            ret_data = collections.OrderedDict()
            for field in self.fields:
                if field == pivot:
                    ret_data[field] = wrt_ticks
                else:
                    ret_data[field] = np.interp(
                        wrt_ticks,
                        self(pivot),
                        self(field),
                        left=np.NaN,
                        right=np.NaN
                        
                    )
            datalist = list()
            for ind in range(len(wrt_ticks)):
                sample_dict = dict()
                for field in self.fields:
                    sample_dict[field] = ret_data[field][ind]
                datalist.append(sample_dict)
            
            return datafile(datalist,self.__config,self.__bname)
        
        return file_interp_func

    def __call__(self, param):

        if not param in self.config.field_labels:
            raise KeyError("No such field defined in configuation file")

        ind = self.config.field_labels.index(param)

        field_data = self.config[ind]

        if field_data.ftype == 'datetime':
            return self.data.get(param)
        else:
            return np.array(self.data.get(param))


    def to_csv(self, filename):
        
        if os.path.isdir(filename):
            # if folder is provided add a filename using filestamp_formatter.encode().csv
            encodedname = self.__config.filestamp_formatter.encode(self.filestamp)
            if encodedname is None:
                raise ValueError("filestamp formatter encoder returned None value, define one encoder function")
            fname = os.path.join(filename, encodedname)
            # print(f'Writing {self.__length} rows to {fname}')
        else:
            #if not folder use filename to store the file
            fname = filename

        print(f"Writing {self.__length} rows to {fname}")
        with open(fname, 'w', newline='') as csvfile:
            outputfields = self.__config.output['fields']

            delimiter = self.__config.delimiter
            if delimiter == 'comma':
                delimiter = ','
            elif delimiter == 'tab':
                delimiter = '\t'
            elif delimiter == 'space':
                delimiter = ' '

            print('delimiter is ', delimiter)

            headerlist = list()
            for field_name in outputfields:
                field_spec = self.__config.get_field(field_name)
                headerlist.append(f'{field_spec.label}({field_spec.units})')

            csvfile.write(delimiter.join(headerlist) + '\n')

            for item_idx in range(self.__length):
                itemobj = self[item_idx]
                row = list()

                for field_name in outputfields:
                    field_spec = self.__config.get_field(field_name)
                    
                    if field_spec.ftype == 'datetime':
                        val = self.__config.timestamp_formatter.encode(itemobj[field_name])
                    else:
                        fmtr = formatter.make_formatter(field_spec.ftype)
                        val = fmtr.encode(itemobj[field_name])

                    row.append(val)
                print(row)
                csvfile.write(delimiter.join(row) + '\n')



    def to_netcdf(self, filename):
        
        if os.path.isdir(filename):
            #if folder is provide add a filename using filestamp_formatter.encode().nc
            pass
        else:
            #if not folder use filename to store the file
            pass

    def to_mat(self, filename):
        
        if os.path.isdir(filename):
            #if folder is provided add a filename using filestamp_formatter.encode().mat
            encoded_name = self.__config.filestamp_formatter.encode(self.filestamp)
            fname = os.path.join(filename, encoded_name)
        else:
            #if not folder user filename to store the file
            fname = filename
        
        

    def to_json(self):
        # this method call is specifically meant for working with userinterface... do not use this unless you know what you are doing

        pass


    def plot(self):

        if not self.__config.is_plottable():
            raise NotImplementedError("Plotting configuration is not defined in configuration, define one for file")

        if self.__config.plot.get('file') is None:
            raise ValueError("datafile plotting variants not provided")

        # plot_line(self, xaxis=self.__config.plot['file']['xaxis'], yaxis=self.__config.plot['file']['yaxis'])
        for variant in self.__config.plot['file']:

            if variant['type'] == 'contour':
                Warning("cannot plot a contour plot from a single dataset")
                continue

            plot_file(self, variant)


    @staticmethod
    def create_instance(datadict,config,basename=None):
        
        if not isinstance(datadict,dict):
            raise ValueError("data should be given in form of dict of lists")

        if not isinstance(config,config_file):
            raise ValueError("argument config should be of type config_file")

        dtlist = list()
        length = len(datadict[config.field_labels[0]])
        
        for i in range(length):
            item = dict()
            for field in config.field_labels:
                item[field] = datadict[field][i]
            dtlist.append(item)

        
        return datafile(dtlist,config,basename)





class datafolder(dataset):

    def __init__(self, datafilelist, pivot_list, config, *args, **kwargs):
        
        self.__data = collections.OrderedDict()

        for field in config.field_labels:
            if field == config.interpolation['pivot']:
                continue
            self.__data[field] = None

        self.__config = config
        self.__pivotlist = pivot_list
        self.__filecount = len(datafilelist)
        self.__length = len(pivot_list)


        # if config.timestamp_in_filename:
        self.__tmlist = list()

        if not all([True if isinstance(ele,datafile) else False for ele in datafilelist]):
            raise ValueError("One/Some of the element is out of context")

        for df_ele in datafilelist:
            for label in config.field_labels:

                if label == config.interpolation['pivot']:
                    continue

                dataarr = df_ele(label)
                
                if self.__data[label] is None:
                    self.__data[label] = dataarr
                else:
                    self.__data[label] = np.vstack((self.__data[label],dataarr))
            
            self.__tmlist.append(df_ele.filestamp)

        for key in self.__data.keys():
            self.__data[key] = self.__data[key].T

    def __del__(self):
        del self.__data

    @property
    def config(self):
        return self.__config

    @property
    def data(self):
        return self.__data

    @property
    def filestamps(self):
        
        # if not self.__config.timestamp_in_filename:
        #     raise NotImplementedError("Configuration setting timestamp_in_filename should be set")

        return self.__tmlist

    @property
    def filecount(self):
        return self.__filecount

    @property
    def fields(self):
        return self.__config.field_labels

    def __len__(self):
        return self.__length


    def __getitem__(self,slc):

        if isinstance(slc,int):
            
            if slc > self.__length:
                raise IndexError(f"index: {slc} is out of range")
            
            item = dict()
            for field in self.__config.field_labels:
                if field == self.__config.interpolation['pivot']:
                    item[field] = self.__pivotlist[slc]
                else:
                    item[field] = self.__data[field][slc]
            item['timestamp'] = self.__tmlist
            
            return item

        elif isinstance(slc,slice):
            
            dflist = list()
            start,stop,step = slc.indices(self.__length)
            pivotlist = self.__pivotlist[start:stop:step]

            for ind in range(self.filecount):
                datadict = dict()
                for label in self.fields:
                    if label == self.__config.interpolation['pivot']:
                        datadict[label] = pivotlist
                    else:
                        datadict[label] = self.__data.get(label,None)[start:stop:step,ind]
                
                # bname = timestamp2str(self.__tmlist[ind],self.__config.filename_format)
                bname = self.__config.filestamp_formatter.encode(self.__tmlist[ind])
                dflist.append(datafile.create_instance(datadict,self.config,basename=bname))
            
            return datafolder(dflist,pivotlist,self.config)


    def __call__(self,label):
        
        if not label in self.config.field_labels:
            raise KeyError(f"No such field {label} defined in configuration file")
            
        if label == self.__config.interpolation['pivot']:
            if isinstance(self.__pivotlist,np.ndarray):
                return self.__pivotlist
            else:
                return np.array(self.__pivotlist)
            
        return self.__data.get(label)


    def get_interpolator(self):
        # This will take pivot field of interpolation config section as reference
        
        pivot_label = self.__config.interpolation['pivot']

        def folder_interp_func(wrt_ticks):

            dflist = list()

            for ind in range(self.filecount):
                datadict = dict()
                for label in self.fields:
                    if label == pivot_label:
                        datadict[label] = wrt_ticks
                    else:
                        datadict[label] = np.interp(
                            wrt_ticks,
                            self.__pivotlist,
                            self.__data.get(label,None)[:,ind],
                            left=np.NaN,
                            right=np.NaN
                        )
                # bname = timestamp2str(self.__tmlist[ind],self.__config.filename_format)
                # print(self.__tmlist[ind])
                
                bname = self.__config.filestamp_formatter.encode(self.__tmlist[ind])
                dflist.append(datafile.create_instance(datadict,self.config,basename=bname))

            return datafolder(dflist,wrt_ticks,self.__config)

        return folder_interp_func



    def to_csv(self, filename):
        raise NotImplementedError("Cannot put a batch of datafiles in a single .csv file")

    def to_netcdf(self, filename):
        pass

    def to_mat(self, filename):
        pass

    def to_json(self):
        pass

    def plot(self):
        
        if not self.__config.is_plottable():
            raise NotImplementedError("Plotting configuration is not defined in configuration for folder")

        if self.__config.plot.get('folder') is None:
            raise ValueError("datafolder plotting variants not provided")

        for variant in self.__config.plot['folder']:
            if not  variant['type'] in ('line', 'contour', ):
                raise ValueError("Undefined variant type is provided")
            
            plot_folder(self, variant)



