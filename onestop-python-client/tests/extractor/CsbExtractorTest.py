import unittest
from onestop.extract.CsbExtractor import CsbExtractor

class CsbExtractorTest(unittest.TestCase):
    def setUp(self):
        print("Set it up!")
        file_name = '../data/file4.csv'
        self.csb_extractor = CsbExtractor(file_name)


    def tearDown(self):
        print("Tear it down!")

    def test_is_csv(self):
        csv_str= '.csv'
        self.assertTrue(self.csb_extractor.is_csv(self.csb_extractor.file_name))


    def test_get_max_numeric(self):
        max_lon = self.csb_extractor.get_max_numeric( 'LON')
        self.assertEqual(max_lon, -92.747995)

    def test_get_min_numeric(self):
        min_lon = self.csb_extractor.get_min_numeric( 'LON')
        self.assertEqual(min_lon, -96.847995)


    def test_get_max_datetime(self):
        end_date = self.csb_extractor.get_max_datetime( 'TIME')
        self.assertEqual(end_date, '2020-04-10T14:00:06.000Z')


    def test_get_min_datetime(self):
        begin_date = self.csb_extractor.get_min_datetime( 'TIME')
        self.assertEqual(begin_date, '2018-04-10T14:00:06.000Z')


    def test_extract_coords(self):
        max_lon = self.csb_extractor.get_max_numeric('LON')
        min_lon = self.csb_extractor.get_min_numeric('LON')
        max_lat = self.csb_extractor.get_max_numeric('LAT')
        min_lat = self.csb_extractor.get_min_numeric('LAT')
        coords = self.csb_extractor.extract_coords(max_lon, max_lat, min_lon, min_lat)
        result = [[
            -94.847995,
            29.373065
        ],
            [
                -96.847995,
                29.373065
            ],
            [
                -94.847995,
                33.373065
            ],
            [
                -92.747995,
                29.383065
            ]
        ]
        self.assertEqual(coords, result)



if __name__ == '__main__':
    unittest.main()