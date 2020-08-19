#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 20:10:54 2020

@author: jeldikk
"""
import yaml
from collections import namedtuple

field_tuple = namedtuple(
    'field_info',
    ['name', 'colno', 'ftype', 'ifnull', 'nullval']
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

        self.__field_data = list()
        for i in range(self.__dt['field_count']):
            # print(self.__dt['input'])
            self.__field_data.append(make_fielddata(**self.__dt['input'][i]))

    @property
    def field_labels(self):
        """property of config_file instance.

        Returns:
            tuple: all fields defined in the input config file
        """
        return tuple(self.__field_data[i].name for i in range(len(self)))

    @property
    def fields(self):
        """property of config_file instance

        Returns:
            list of dicts: contains list of all hashes containing input field info
        """
        return self.__field_data

    def __getitem__(self, ind):
        """this is called to access items using index

        Args:
            ind (slice object): [description]

        Raises:
            IndexError: [description]

        Returns:
            [type]: [description]
        """


        if ind > self.__dt['field_count'] - 1:
            raise IndexError("Index is out of bounds")

        return self.__field_data[ind]

    def __getattr__(self, field):

        if field in self.__dt.keys():
            return self.__dt.get(field)
        else:
            raise AttributeError("No such attribute found {}".format(field))

    def __len__(self):

        """length of input fields in the dataset

        Returns:
            int: Number of fields in the dataset
        """

        return self.__dt['field_count']

    def is_valid(self):

        """to validate whether config_file instance is a valid object

        Returns:
            bool: returns True if instance is valid else False
        """
        
        fieldcount_cond = self.__dt['field_count'] == len(self.__dt['input'])
        timestamp_cond = False if self.__dt['timestamp_in_filename'] and self.__dt["filename_format"] is None else True
        interp_cond = True if self.__dt['interpolation']['pivot'] in self.field_labels else False

        # if self.__dt['timestamp_in_filename'] and self.__dt['filename_format'] is None:
        #     cond2 = False
        # else:
        #     cond2 = True

        if fieldcount_cond and timestamp_cond and interp_cond:
            # yet more conditions are to be implemented
            return True
        else:
            # print(cond1, cond2)
            return False

    def show(self):
        # print(self.__dict__)
        print(self.__dt)


def make_fielddata(**kwargs):
    return field_tuple(
        kwargs['name'],
        kwargs['colno'],
        kwargs['ftype'],
        kwargs['ifnull'],
        kwargs['nullval']
    )
