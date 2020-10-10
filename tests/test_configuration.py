#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 20:11:45 2020

@author: jeldikk
"""

import os
import unittest
from ismartcsv import configuration


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


if __name__ == "__main__":
    # import os
    # print(os.curdir)
    unittest.main()
