import unittest
import os

from ismartcsv import read_folder
from ismartcsv import dataset

class TestReadFolderTestCase(unittest.TestCase):

    def setUp(self):
        self.folder_name = "./assets/data/uvw/"
        self.config_filename = "./assets/configurations/uvw_config.yaml"
        self.datafolder = read_folder(self.folder_name,self.config_filename)

    def test_read_folder(self):
        self.assertIsInstance(self.datafolder,dataset.datafolder)

    def test_filecount(self):
        listdir = os.listdir(self.folder_name)
        self.assertEqual(self.datafolder.filecount, len(listdir))
        self.assertEqual(self.datafolder.filecount, len(self.datafolder.timestamps))


