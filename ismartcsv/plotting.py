#!/usr/bin/env python3

'''
    @author : jeldikk
'''

import matplotlib.pyplot as plt
import copy
import numpy as np


class ismart_interp(object):
    pass


def plot_line(instance, xaxis=None, yaxis=None, *args, **kwargs):

    if xaxis is None and yaxis is None:
        raise AssertionError("plots should have atleast one common axis")

    if xaxis is None:
        # print(args)
        ex_labels = 0
        if len(kwargs) > 0:
            if 'exclude' in kwargs:
                ex_labels = len(kwargs['exclude'])
        # plot something having common yaxis
        if not yaxis in instance.fields:
            raise ValueError("{} is not a registered field".format(yaxis))

        fig, axes = plt.subplots(
            nrows=1, ncols=len(instance.fields)-1 - ex_labels)
        indices = 0
        ylims = [min(instance(yaxis)), max(instance(yaxis))]

        for field in instance.fields:
            if ex_labels > 0:
                if field in kwargs['exclude']:
                    continue
            if field == yaxis:
                continue
            axes[indices].plot(instance(field), instance(yaxis))
            axes[indices].set_xlim(min(instance(field)), max(instance(field)))
            axes[indices].set_ylim(min(instance(yaxis)), max(instance(yaxis)))
            axes[indices].set(xlabel=field.upper(), ylabel=yaxis.upper())
            indices += 1

        plt.show()

    elif yaxis is None:
        # plot something having commong xaxis
        if not xaxis in instance.fields:
            raise ValueError("{} is not a registered field".format(xaxis))

        pass


def gps_balloon_traverse_phases(height_info):
    '''
    special method especially meant to differentiate surface, ascent, descent limits of height information
    this method is an experimental method for finding gps_sonde related data
    '''
    MIN_ASC_RATE = 1.5  # mps

    data_info = dict()
    orig_copy = copy.copy(height_info)
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
