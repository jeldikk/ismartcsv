import unittest
import numpy as np


from ismartcsv import datafile, datafolder
from ismartcsv import read_file, read_folder

class TestInterpolators(unittest.TestCase):

    def setUp(self):
        self.filename = "./assets/data/uvw/uvwD20191009T220158.csv"
        self.foldername = "./assets/data/uvw/"
        self.config_filename = "./assets/configurations/uvw_config.yaml"
    
    def test_instances(self):
        dfile = read_file(self.filename,self.config_filename)
        # dfile.plot()
        dfolder = read_folder(self.foldername,self.config_filename)
        self.assertIsInstance(dfile,datafile)
        self.assertIsInstance(dfolder,datafolder)

    def test_file_interpolator(self):
        dfile = read_file(self.filename,self.config_filename)
        interp = dfile.get_interpolator()
        self.assertEqual(interp.__name__, 'file_interp_func')

    def test_folder_interpolator(self):
        dfolder = read_folder(self.foldername,self.config_filename)
        interp = dfolder.get_interpolator()
        self.assertEqual(interp.__name__,'folder_interp_func')

    def test_file_interp_dimensions(self):
        dfile = read_file(self.filename,self.config_filename)
        interp = dfile.get_interpolator()
        temp_dfile = interp(np.arange(2,20,0.01))
        self.assertEqual(len(temp_dfile),len(np.arange(2,20,0.01)))
    
    def test_folder_interp_dimensions(self):
        dfolder = read_folder(self.foldername,self.config_filename)
        interp = dfolder.get_interpolator()
        temp_dfolder = interp(np.arange(2,20,1))
        self.assertEqual(len(temp_dfolder),len(np.arange(2,20,1)))
