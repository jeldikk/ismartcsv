#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 10:06:16 2020

@author: jeldikk
"""
import datetime
import copy
import numpy as np
import collections


def str2timestamp(time_rep, datetime_format):
    '''
        utility function which converts timestamp in string format to datetime object

        input: 
            time_rep : datetime represented as string
            date_format : datetime format time_rep is formatted
        output:
            a datetime object
    '''
    return datetime.datetime.strptime(time_rep, datetime_format)


def timestamp2str(datetime_obj, datetime_format):
    
    """utitlity function which converts datetime object to string by using given format

    Arguments:
        datetime_obj {datetime} -- [datetime object]
        datetime_format {[type]} -- [description]

    Returns:
        [type] -- [description]
    """

    return datetime_obj.strftime(datetime_format)



def is_increasing(values):

    """function to find out if the iterator values are strictly increasing

    Arguments:
        values {[list]} -- [List of items whose __lt__, __gt__ etc., such magic methods are defined and items should be indexable]

    Returns:
        bool -- True if items are in increasing order else False
    """

    return all([i <= j for i, j in zip(values, values[1:])])


def is_decreasing(values):

    """function to find out if the iterator values are strictly decreasing

    Arguments:
        values {list} -- List of items whose comparative and indexing  magical methods are defined

    Returns:
        bool -- True if items are in decreasing order else false
    """

    return all([i >= j for i, j in zip(values, values[1:])])


def create_file_interpolator(instance, pivot):

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

    from .dataset import datafile

    if not isinstance(instance,datafile):
        raise TypeError("Only accepts of type datafile, but got something else")

    if not pivot in instance.fields:
        raise ValueError("No such field available by name {}".format(pivot))

    if not is_increasing(instance(pivot)):
        raise RuntimeError("Data {} is not in increasing order".format(pivot))

    def interp_func(wrt_ticks):
        # from .dataset import ismart_chunk

        ret_data = collections.OrderedDict()
        for field in instance.fields:
            if field == pivot:
                ret_data[field] = wrt_ticks
            else:
                ret_data[field] = np.interp(
                    wrt_ticks,
                    instance(pivot),
                    instance(field),
                    left=np.NaN,
                    right=np.NaN
                )

        datalist = list()
        for ind in range(len(wrt_ticks)):
            sample_dict = dict()
            for field in instance.fields:
                sample_dict[field] = ret_data[field][ind]
            datalist.append(sample_dict)
        

        return datafile(datalist,instance.config,instance.basename)

    return interp_func



def gps_balloon_traverse_phases(height_info):
    '''
    special method especially meant to differentiate surface, ascent, descent limits of height information
    this method is an experimental method for finding gps_sonde related data
    '''
    MIN_ASC_RATE = 1.5  # mps

    data_info = dict()
    # orig_copy = copy.copy(height_info)
    arr_length = len(height_info)
    # grad_data = np.gradient(height_info)
    diff_vals = np.diff(height_info)
    paav_len = arr_length//3
    # print(diff_vals[:paav_len])
    for ind, ele in enumerate(reversed(diff_vals[:paav_len])):
        if ele <= MIN_ASC_RATE:
            break
    data_info['asc_start'] = paav_len - ind + 1

    for ind, ele in enumerate(diff_vals[arr_length//2:]):
        if ele <= 0:
            break

    data_info['dsc_start'] = arr_length//2 + ind

    return data_info

