#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 20:11:45 2020

@author: jeldikk
"""

import os
import unittest
from ismartcsv import configuration



def datetime_parser(tm_str, format):
    print("This is from datetime_parser")

def datetime_encoder(tm_obj, format):
    print('This is from datetime_encoder')

def filename_parser(fn_str, format):
    print(format)
    print("this is filename_parser")

def filename_encoder(fn_obj, format):
    print(format)
    print("this is filename_encoder")


options = {
    'DATETIME_PARSER': datetime_parser,
    'DATETIME_ENCODER': datetime_encoder,
    'FILENAME_PARSER': filename_parser,
    'FILENAME_ENCODER': filename_encoder,
}


class TestConfigParser(unittest.TestCase):

    # filename = "./assets/configurations/uvw_config.yaml"


    def setUp(self):
        self.config_name = "./assets/configurations/uvw_config.yaml"
        self.config = configuration.config_file(self.config_name)

    def test_validity(self):
        # self.config.show()
        self.assertTrue(self.config.is_valid())

    def test_field_labels(self):

        field_labels = self.config.field_labels
        self.assertEqual(len(field_labels),self.config.field_count)


    def test_attributes(self):
        # print(self.config.interpolation['pivot'])
        
        self.assertEqual(self.config.delimiter,'comma')
        self.assertTrue(self.config.timestamp_in_filename)
        self.assertTrue(self.config.is_interpolatable(), "No interpolation config defined")
        self.assertTrue(self.config.is_plottable(), "No plot config defined")
        # self.assertEqual(self.config.delimiter)

    def test_plot(self):

        # print(self.config.plot['file'])
        # print(self.config.plot['file'][0])
        self.assertTrue(self.config.is_plottable())
        self.assertGreater(len(self.config.plot['file']),0)

    def test_formatters(self):
        self.config = configuration.config_file(self.config_name, **options)
        # print("this is to test formatters")
        print(self.config.timestamp_formatter)
        print(self.config.filestamp_formatter)
        self.config.filestamp_formatter.parse("2020-12-30 22:34:12")


# if __name__ == "__main__":
#     # import os
#     # print(os.curdir)
#     unittest.main()
