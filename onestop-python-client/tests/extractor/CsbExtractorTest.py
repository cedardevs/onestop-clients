import unittest
import os

from moto import mock_s3
from onestop.extract.CsbExtractor import CsbExtractor
from onestop.util.S3Utils import S3Utils

class CsbExtractorTest(unittest.TestCase):

    def setUp(self):
        print("Set it up!")
        self.root_proj_path = os.getcwd()
        self.assertIsNotNone(self.root_proj_path)
        self.key = "tests/data/file4.csv"
        # Use open instead of our methodfor simplicity and reliability, plus not testing our code here.
        self.file_obj = open(self.root_proj_path + '/' + self.key)

        config_dict = {
            "access_key": "test_access_key",
            "secret_key": "test_secret_key",
            "log_level": "DEBUG"
        }

        self.s3_utils = S3Utils(**config_dict)
        self.bucket = "bucket"
        self.region = "region"

    def tearDown(self):
        print("Tear it down!")
        self.file_obj.close()

    def test_is_csv(self):
        self.assertTrue(CsbExtractor.is_csv("test/blah/file.csv"), "Failed to determine a csv file name was a csv file.")

    def test_is_not_csv(self):
        self.assertFalse(CsbExtractor.is_csv("test/blah/file.txt"), "Failed to determine a csv file name was not a csv file.")

    @mock_s3
    def test_csb_SME_user_path(self):
        # Setup bucket and file to read
        s3 = self.s3_utils.connect('s3', self.region)
        s3.create_bucket(Bucket=self.bucket, CreateBucketConfiguration={'LocationConstraint': self.region})
        self.s3_utils.upload_s3(s3, self.root_proj_path + '/' + self.key, self.bucket, self.key, True)
        self.assertTrue(self.s3_utils.read_bytes_s3(s3, self.bucket, self.key))

        # This is how we would expect an external user to get the file.
        sm_open_file = self.s3_utils.get_csv_s3(self.s3_utils.connect("session", None), self.bucket, self.key)

        bounds_dict = CsbExtractor.get_spatial_temporal_bounds(sm_open_file, 'LON', 'LAT', 'TIME')
        coords = bounds_dict["geospatial"]
        self.assertEqual(coords[0], -96.847995)
        self.assertEqual(coords[1], 29.373065)
        self.assertEqual(coords[2], -92.747995)
        self.assertEqual(coords[3], 33.373065)

        date_rng = bounds_dict["temporal"]
        self.assertEqual(date_rng[0], '2018-04-10T14:00:06.000Z' )
        self.assertEqual(date_rng[1], '2020-04-10T14:00:06.000Z' )

    def test_get_geospatial_temporal_bounds(self):
        bounds_dict = CsbExtractor.get_spatial_temporal_bounds(self.file_obj, 'LON', 'LAT', 'TIME')

        coords = bounds_dict["geospatial"]
        self.assertEqual(coords[0], -96.847995)
        self.assertEqual(coords[1], 29.373065)
        self.assertEqual(coords[2], -92.747995)
        self.assertEqual(coords[3], 33.373065)

        date_rng = bounds_dict["temporal"]
        self.assertEqual(date_rng[0], '2018-04-10T14:00:06.000Z' )
        self.assertEqual(date_rng[1], '2020-04-10T14:00:06.000Z' )

    def test_get_min_lon(self):
        bounds_dict = CsbExtractor.get_spatial_temporal_bounds(self.file_obj, 'LON', 'LAT', 'TIME')

        coords = bounds_dict["geospatial"]
        min_lon = coords[0]
        self.assertEqual(min_lon, -96.847995)

    def test_get_max_datetime(self):

        bounds_dict = CsbExtractor.get_spatial_temporal_bounds(self.file_obj, 'LON', 'LAT', 'TIME')

        date_rng = bounds_dict["temporal"]
        end_date = date_rng[1]
        self.assertEqual(end_date, '2020-04-10T14:00:06.000Z')

    def test_get_min_datetime(self):
        bounds_dict = CsbExtractor.get_spatial_temporal_bounds(self.file_obj, 'LON', 'LAT', 'TIME')

        date_rng = bounds_dict["temporal"]
        begin_date = date_rng[0]
        self.assertEqual(begin_date, '2018-04-10T14:00:06.000Z')

    def test_extract_coords(self):
        coords = CsbExtractor.extract_coords(self.file_obj, -92.747995, 33.373065, -96.847995, 29.373065)
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