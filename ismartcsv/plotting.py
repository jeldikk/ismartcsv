#!/usr/bin/env python3

'''
    @author : jeldikk
'''

# import matplotlib.pyplot as plt
import copy
import numpy as np

import matplotlib
# matplotlib.use('QT5Agg')
import matplotlib.pyplot as plt
from matplotlib import cm as colormap
import matplotlib.gridspec as gridspec


def plot_file(instance, variant, *args, **kwargs):

    """plotting function to render file variants of plot config section

    Args:
        instance (datafile): datafile object to be visualised
        variant (dict): a part of plot section with file variant

    Raises:
        AssertionError: error raised when both xaxis and yaxis attributes of variant are None
        ValueError: Error raised when xaxis field or yaxis field is not available in list of fields
    """
    
    plot_fields = variant['fields']
    xaxis = variant['xaxis']
    yaxis = variant['yaxis']
    window_title = variant['title']

    if xaxis is None and yaxis is None:
        raise AssertionError("line plot should have atleast one common axis")

    # if not instance.config.is_plottable():
    #     raise ValueError("no plot configuration section defined in config file")

    if xaxis is None:

        # plot something having common yaxis
        if not yaxis in instance.fields:
            raise ValueError("{} is not a registered field".format(yaxis))

        fig = plt.figure(constrained_layout=True)
        fig.canvas.set_window_title(window_title)
        spec = gridspec.GridSpec(nrows=1, ncols=len(plot_fields), figure=fig)
        
        ylims = [np.nanmin(instance(yaxis)), np.nanmax(instance(yaxis))]

        yaxis_field = instance.config.fields.get(yaxis)
        # print(yaxis_field)
        for ind, fld in enumerate(plot_fields):
            
            # print(fld)
            field = instance.config.get_field(fld)
            # print(field)
            temp_plot = fig.add_subplot(spec[ind])

            temp_plot.plot(instance(field.name), instance(yaxis))
            temp_plot.set_xlim(np.nanmin(instance(field.name)), np.nanmax(instance(field.name)))
            temp_plot.set_ylim(np.nanmin(instance(yaxis)), np.nanmax(instance(yaxis)))
            temp_plot.set_xlabel(f"{field.label}({field.units})")
            if ind == 0:
                temp_plot.set_ylabel(f"{yaxis_field.label}({yaxis_field.units})")
            # indices += 1
        
        fig.suptitle(window_title)
        fig.show()

    elif yaxis is None:
        # plot something having commong xaxis
        if not xaxis in instance.fields:
            raise ValueError("{} is not a registered field".format(xaxis))

        # plot_fields = instance.config.plot['file']['fields']
        fig = plt.figure(constrained_layout=True)
        fig.canvas.set_window_title(window_title)
        spec = gridspec.GridSpec(nrows=len(plot_fields), ncols=1, figure=fig)

        xaxis_field = instance.config.get_field(xaxis)

        for ind, fld in enumerate(plot_fields):
            field = instance.config.get_field(fld)
            temp_plot = fig.add_subplot(spec[ind])

            temp_plot.plot(instance(xaxis), instance(field.name))
            temp_plot.set_xlim(np.nanmin(instance(xaxis)), np.nanmax(instance(xaxis)))
            temp_plot.set_ylim(np.nanmin(instance(field.name)), np.nanmax(instance(field.name)))
            # temp_plot.set_xlabel(f"{axis_field.label}({axis_field.units})")
            temp_plot.set_ylabel(f"{field.label}({field.units})")
            if ind == len(plot_fields) - 1:
                temp_plot.set_xlabel(f"{xaxis_field.label}({xaxis_field.units})")

        fig.suptitle(window_title)
        fig.show()


def plot_folder(instance, variant, *args, **kwargs):
    """utility function to plot folder variant of plot config section 

    Args:
        instance (datafolder): ismartcsv datafolder instance
        variant (dict): a variant of folder plot section
    """
    
    ptype = variant['type']
    plot_fields = variant['fields']
    xaxis = variant['xaxis']
    yaxis = variant['yaxis']
    window_title = variant['title']

    if ptype == 'line':
        
        fig = plt.figure(constrained_layout=True)
        fig.canvas.set_window_title(window_title)
        spec = gridspec.GridSpec(nrows=1, ncols=len(plot_fields), figure=fig)

        yaxis_field = instance.config.get_field(yaxis)

        for idx, fld in enumerate(plot_fields):
            field = instance.config.get_field(fld)
            field_data = instance(fld)
            temp_plot = fig.add_subplot(spec[idx])
            for colno in range(instance.filecount):
                temp_plot.plot(field_data[:,colno], instance(yaxis))
            temp_plot.set_xlim(np.nanmin(field_data), np.nanmax(field_data))
            temp_plot.set_ylim(np.nanmin(instance(yaxis)), np.nanmax(instance(yaxis)))
            temp_plot.set_xlabel(f'{field.label}({field.units})')
            # temp_plot.set_title(plot_title)
            if idx == 0:
                temp_plot.set_ylabel(f'{yaxis_field.label}({yaxis_field.units})')

        fig.suptitle(window_title)
        fig.show()


    elif ptype == 'contour':
        
        fig = plt.figure(constrained_layout = True)
        fig.canvas.set_window_title(window_title)
        spec = gridspec.GridSpec(nrows=len(plot_fields), ncols=1, figure=fig)

        # xaxis_field = instance.config.get_field(xaxis)
        yaxis_field = instance.config.get_field(yaxis)

        for idx, fld in enumerate(plot_fields):

            field = instance.config.get_field(fld)
            field_data = instance(fld)
            # print(field_data)
            # print(field_data.shape)
            temp_plot = fig.add_subplot(spec[idx])
            cbar_levels = np.linspace(np.nanmin(field_data), np.nanmax(field_data), 10)
            cntr = temp_plot.contourf(instance.timestamps, instance(yaxis), field_data, levels=cbar_levels, cmap= colormap.jet)

            # temp_plot.set_xticks(instance.timestamps)
            # temp_plot.set_yticks(instance(yaxis))

            temp_plot.set_xlabel("File Timestamps")
            temp_plot.set_ylabel(f'{yaxis_field.label}({yaxis_field.units})')

            temp_plot.set_title(f'{field.label}({field.units})')

            fig.colorbar(cntr, ax=temp_plot, ticks=cbar_levels)

        fig.suptitle(window_title)
        fig.show()

    

