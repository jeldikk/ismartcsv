#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 20:10:54 2020

@author: jeldikk
"""
import yaml
from collections import namedtuple

from .formatters import formatter

# from .utilities import timestamp_parser

field_tuple = namedtuple(
    'field_info',
    ['name', 'colno', 'ftype', 'factor', 'ifnull', 'nullval', 'label', 'units']
)


class config_file(object):

    """config_file class instance(object) will contains all the configuration related to the datafile

    Args:
        object (inbuilt object class): this is trivial mantra of OOP in python

    Raises:
        IndexError: raises when you access out of bounds data while accessing data using item index
        AttributeError: raises when you are accessing something not defined in configuration file

    Returns:
        config_file instance: instance of config_file blueprint, 
        this object contains configuration required for reading, writing, plotting and interpolation
    """
    # __dt = None
    # __field_data = None

    def __init__(self, filename, *args, **kwargs):
        
        """constructor of config_file class

        Args:
            filename (str): path of configuration file specifying data.
        """

        with open(filename, 'r') as fp:
            self.__dt = yaml.load(fp, Loader=yaml.FullLoader)

        self.__field_data = dict()
        for i in range(self.__dt['field_count']):
            # print(self.__dt['input'])
            # self.__field_data.append(make_fielddata(**self.__dt['fields'][i]))

            temp_field = make_fielddata(**self.__dt['fields'][i])
            self.__field_data[temp_field.name] = temp_field

        self.__ffmt = formatter.make_formatter('filename', self.__dt['filename_format'])
        self.__dfmt = formatter.make_formatter('datetime', self.__dt['datetime_format'])



        if not kwargs.get(self.__dt['parsers']['filename'], None) is None:
            # print("filename parser is assigned")
            self.__ffmt.set_parser(kwargs.get(self.__dt['parsers']['filename']))

        if not kwargs.get(self.__dt['encoders']['filename'], None) is None:
            # print("filename encoder is assigned")
            self.__ffmt.set_encoder(kwargs.get(self.__dt['encoders']['filename']))

        if not kwargs.get(self.__dt['parsers']['datetime'], None) is None:
            # print("datetime parser is assigned")
            self.__dfmt.set_parser(kwargs.get(self.__dt['parsers']['datetime']))

        if not kwargs.get(self.__dt['encoders']['datetime'], None) is None:
            # print("datetime encoder is assigned")
            self.__dfmt.set_encoder(kwargs.get(self.__dt['encoders']['datetime']))


        # if self.__dt['timestamp_in_filename']:
        #     self.__ffmt = formatter.make_formatter('filename',self.__dt['filename_format'])
        # else:
        #     self.__ffmt = None

    @property
    def field_labels(self):

        """property of config_file instance.

        Returns:
            tuple: all fields defined in the input config file
        """

        return tuple(self.fields.keys())

    @property
    def fields(self):

        """property of config_file instance

        Returns:
            dict with keys: contains list of all hashes containing input field info
        """

        return self.__field_data

    @property
    def filestamp_formatter(self):
        return self.__ffmt


    @property
    def timestamp_formatter(self):
        return self.__dfmt


    def __getitem__(self, ind):

        """this is called to access items using index

        Args:
            ind (int): [field item by index and index starts from 0]

        Raises:
            IndexError: [description]

        Returns:
            [type]: [description]
        """

        if ind > self.__dt['field_count'] - 1:
            raise IndexError("Index is out of bounds")

        field_name = list(self.__field_data.keys())[ind]
        return self.__field_data.get(field_name)

        
    def __getattr__(self, attr):

        if attr in self.__dt.keys():
            return self.__dt.get(attr)
        else:
            raise AttributeError("No such attribute found {}".format(attr))

    def __len__(self):

        """length of input fields in the dataset

        Returns:
            int: Number of fields in the dataset
        """

        return self.__dt['field_count']


    def get_field(self,name):


        # ind = self.__field_name_to_index(name)
        return self.__field_data.get(name)


    def __field_name_to_index(self,name):

        for ind,val in enumerate(self.field_labels):
            if val == name:
                return ind
        
        if val ==  self.field_count:
            raise ValueError(f"No field data with {name} registered")


    def is_interpolatable(self):

        return True if self.__dt.get('interpolation') else False

        
    def is_plottable(self):

        return True if self.__dt.get('plot') else False

    


    def is_valid(self):

        """to validate whether config_file instance is a valid instance

        Returns:
            bool: returns True if instance is valid else False
        """

        cond_checklist = list()

        fieldcount_cond = self.__dt['field_count'] == len(self.__dt['fields'])
        cond_checklist.append(fieldcount_cond)

        timestamp_cond = False if self.__dt['timestamp_in_filename'] and self.__dt["filename_format"] is None else True
        cond_checklist.append(timestamp_cond)

        if self.is_interpolatable():
            interp_cond = True if self.__dt['interpolation']['pivot'] in self.field_labels else False
            cond_checklist.append(interp_cond)

        if self.__dt.get('output',None):
            output_cond = all([True if field in self.field_labels else False for field in self.__dt['output']['fields']])
            cond_checklist.append(output_cond)

        # print(self.__dt.get('output', None))

        # print(cond_checklist)
        


        # print(f"Number of checklist items {len(cond_checklist)}")
        if all(cond_checklist):
            # yet more conditions are to be implemented
            return True
        else:
            return False

    def show(self):
        print(self.__dt)
        # pass



def make_fielddata(**kwargs):
    return field_tuple(
        kwargs['name'],
        kwargs['colno'],
        kwargs['ftype'],
        kwargs['factor'],
        kwargs['ifnull'],
        kwargs['nullval'],
        kwargs['label'],
        kwargs['units']
    )
