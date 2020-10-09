#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 11:52:13 2020

@author: jeldikk
"""
import os
import unittest
import collections


from ismartcsv import dataset
from ismartcsv import configuration
from ismartcsv import read_file


class TestDataFile(unittest.TestCase):

    def aws_config(self):

        self.config_name = "./assets/configurations/aws_config.yaml"
        self.filename = "./assets/data/aws/AWS20180101.CSV"

    def uvw_config(self):
        self.config_name = "./assets/configurations/uvw_config.yaml"
        self.filename = "./assets/data/uvw/uvwD20191009T220158.csv"

    def setUp(self):
        self.uvw_config()
        self.df = read_file(self.filename,self.config_name)

    def __del__(self):
        pass
        # del self.config_name
        # del self.filename
        # del self.df

    def test_length(self):
        # print(type(self.df))
        self.assertTrue(len(self.df),160)

    def test_getitem(self):
        
        item = self.df[10]
        items = self.df[2:20:2]
        huha = self.df[:15]
        self.assertTupleEqual(tuple(item.keys()),self.df.config.field_labels)
        self.assertIsInstance(items,dataset.datafile)

    @unittest.skip
    def test_call(self):
        
        elements = self.df('timestamp')
        # print(elements)
        self.assertEqual(len(elements),len(self.df))

    def test_properties(self):
        fulldata = self.df.data
        fields = self.df.fields

        self.assertIsInstance(fulldata,collections.OrderedDict)
        self.assertTupleEqual(fields,self.df.config.field_labels)

    

if __name__ == "__main__":
    unittest.main()
