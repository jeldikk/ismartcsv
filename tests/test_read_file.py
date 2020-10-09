import unittest
from ismartcsv import read_file

from ismartcsv.utilities import create_file_interpolator


class TestReadFile(unittest.TestCase):

    def setUp(self):
        self.config_filename = "./assets/configurations/uvw_config.yaml"
        self.data_filename = "./assets/data/uvw/uvwD20191009T220158.csv"
        self.datafile = read_file(self.data_filename,self.config_filename)

    def test_readfile(self):
        self.assertEqual(len(self.datafile.fields),len(self.datafile.config.field_labels))

    def test_interpolator(self):
        interp = create_file_interpolator(self.datafile,'height')
        newfile = interp([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17])
        self.assertEqual(newfile('height')[-1],17)

      


