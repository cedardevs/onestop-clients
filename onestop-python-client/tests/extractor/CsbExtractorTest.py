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
        csv_str = '.csv'
        self.assertTrue(self.csb_extractor.is_csv(self.csb_extractor.file_name))


    def test_get_geospatial_temporal_bounds(self):
        #max_lon = self.csb_extractor.get_max_numeric('LON')
        bounds_dict = self.csb_extractor.get_spatial_temporal_bounds('LON', 'LAT', 'TIME')
        coords = bounds_dict["geospatial"]
        print(str(coords))
        self.assertEqual(coords[0], -96.847995)
        self.assertEqual(coords[1], 29.373065)
        self.assertEqual(coords[2], -92.747995)
        self.assertEqual(coords[3], 33.373065)

        date_rng = bounds_dict["temporal"]
        self.assertEqual(date_rng[0], '2018-04-10T14:00:06.000Z' )
        self.assertEqual(date_rng[1], '2020-04-10T14:00:06.000Z' )


    def test_get_min_lon(self):
        bounds_dict = self.csb_extractor.get_spatial_temporal_bounds('LON', 'LAT', 'TIME')
        coords = bounds_dict["geospatial"]
        min_lon = coords[0]
        self.assertEqual(min_lon, -96.847995)


    def test_get_max_datetime(self):
        bounds_dict = self.csb_extractor.get_spatial_temporal_bounds('LON', 'LAT', 'TIME')
        date_rng = bounds_dict["temporal"]
        end_date = date_rng[1]
        self.assertEqual(end_date, '2020-04-10T14:00:06.000Z')


    def test_get_min_datetime(self):
        bounds_dict = self.csb_extractor.get_spatial_temporal_bounds('LON', 'LAT', 'TIME')
        date_rng = bounds_dict["temporal"]
        begin_date = date_rng[0]
        self.assertEqual(begin_date, '2018-04-10T14:00:06.000Z')


    def test_extract_coords(self):
        bounds_dict = self.csb_extractor.get_spatial_temporal_bounds('LON', 'LAT', 'TIME')
        coords = bounds_dict["geospatial"]

        min_lon = coords[0]
        min_lat = coords[1]
        max_lon = coords[2]
        max_lat = coords[3]

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