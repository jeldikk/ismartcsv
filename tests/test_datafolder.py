import unittest

from ismartcsv import datafolder
from ismartcsv import read_folder

class TestDataFolder(unittest.TestCase):

    def uvwconfig(self):
        self.config_filename = "./assets/configurations/uvw_config.yaml"
        self.foldername = "./assets/data/uvw/"
        self.dfolder = read_folder(self.foldername,self.config_filename)

    def rsconfig(self):
        pass

    def awsconfig(self):
        pass

    def setUp(self):
        self.uvwconfig()

    def test_data_dimension(self):
        
        # print(self.dfolder.config.field_count)
        # print(self.dfolder.conf)
        # print(self.dfolder('u'))
        # print(self.dfolder('height'))
        # print(self.dfolder.data['u'].shape)
        # print(self.dfolder.data['v'].shape)
        # print(len(self.dfolder.timestamps))
        self.assertTupleEqual(self.dfolder.data['u'].shape, self.dfolder.data['v'].shape)

    def test_getitem(self):

        item = self.dfolder[3]
        items = self.dfolder[2:30:4]
        # print(item)
        # print(items.data)
        # print(items.data['u'].shape)
        # print(items.data['v'].shape)
        # print(len(items))
        self.assertIsInstance(items,datafolder,"getitem slice is not an instance of datafolder")

    def test_attributes(self):
        # self.assertEqual(len(self.dfolder.data.keys()),self.dfolder.config.field_count-1)
        self.assertEqual(len(self.dfolder.timestamps), self.dfolder.filecount,"filecount and timestamp count mismatch occured")