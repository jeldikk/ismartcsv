import unittest
import datetime

from ismartcsv.formatters import datetime_formatter, filename_formatter



class TestParserAndEncoderClass(unittest.TestCase):

    def setUp(self):
        self.config1()
        self.file_formatter = filename_formatter(self.filename_format)
        self.date_formatter = datetime_formatter(self.datetime_format)

    def config1(self):
        self.datetime_format = "%Y%m%d %H:%M:%S"
        self.filename_format = "uvwD%Y%m%dT%H%M%S.csv"
        

    def config2(self):
        self.datetime_format = None
        self.filename_format = None

    def test_parsing(self):
        self.date_formatter.parse("20020202 02:02:02")
        self.file_formatter.parse("uvwD20020202T020202.csv")

    def test_encoder(self):
        self.date_formatter.encode(datetime.datetime(2002,2,2,2,2,2))
        self.file_formatter.encode(datetime.datetime(2002,2,2,2,2,2))


    def test_datetime_formatter(self):
        pass