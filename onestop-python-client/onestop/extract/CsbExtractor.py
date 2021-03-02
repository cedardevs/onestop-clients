import csv
from datetime import datetime

class CsbExtractor:

    # def __init__(self, file_name):
    #     self.file_name = file_name

    def __init__(self, su, key):
        self.su = su
        boto_client = self.su.connect("session", None)
        bucket = self.su.conf['s3_bucket']
        self.key = key

    # Function to check if a file is a csv file
    def is_csv(self, file_name):
        csv_str = '.csv'
        if file_name.endswith(csv_str):
            return True

        return False

    # def smart_open_read(self, key):
    #     boto_client = self.su.connect("session", None)
    #     bucket = self.su.conf['s3_bucket']
    #     self.su.read_csv_s3(boto_client, bucket, key)

    # Function to check if a file is a csv file
    def get_spatial_temporal_bounds(self, lon_column_name, lat_column_name, date_column_name):
        lon_min_val = None
        lon_max_val = None
        lat_min_val = None
        lat_max_val = None
        # variable used for comparison in date time format
        end_date = None
        # variable to be returned in string format
        end_date_str = ''
        begin_date = None
        # variable to be returned in string format
        begin_date_str = ''

        boto_client = self.su.connect("session", None)
        bucket = self.su.conf['s3_bucket']
        sm_open_file = self.su.get_csv_s3(boto_client, bucket, self.key)
        csv_reader = csv.DictReader(sm_open_file)

        for row in csv_reader:
            # first iteration, sets max to first element
            if not lon_max_val:
                lon_max_val = float(row[lon_column_name])
            else:
                lon_max_val = max(lon_max_val, float(row[lon_column_name]))
            if not lon_min_val:
                lon_min_val = float(row[lon_column_name])
            else:
                lon_min_val = min(lon_min_val, float(row[lon_column_name]))

            if not lat_max_val:
                lat_max_val = float(row[lat_column_name])
            else:
                lat_max_val = max(lat_max_val, float(row[lat_column_name]))
            if not lat_min_val:
                lat_min_val = float(row[lat_column_name])
            else:
                lat_min_val = min(lat_min_val, float(row[lat_column_name]))

            # Need to convert the string to python datetime for comparison
            end_date_time = datetime.strptime(row[date_column_name].replace('.000Z', '', 1), "%Y-%m-%dT%H:%M:%S")
            begin_date_time = datetime.strptime(row[date_column_name].replace('.000Z', '', 1), "%Y-%m-%dT%H:%M:%S")

            # first iteration
            if not begin_date:
                begin_date = begin_date_time
                begin_date_str = row[date_column_name]
            else:
                if begin_date_time < begin_date:
                    begin_date = begin_date_time
                    begin_date_str = row[date_column_name]

            # first iteration
            if not end_date:
                end_date = end_date_time
                end_date_str = row[date_column_name]
            else:
                if end_date_time > end_date:
                    end_date = end_date_time
                    end_date_str = row[date_column_name]

        geospatial_temporal_bounds = {
            "geospatial": [lon_min_val, lat_min_val, lon_max_val, lat_max_val],
            "temporal": [begin_date_str, end_date_str]
        }

        return geospatial_temporal_bounds


    # Given the max/min lon and lat, the function will parse the csv file to extract to according coordinates
    def extract_coords(self, max_lon, max_lat, min_lon, min_lat):
        # Keeps track of all coordinates that needs to be added to json payload
        coords = []

        boto_client = self.su.connect("session", None)
        bucket = self.su.conf['s3_bucket']
        sm_open_file = self.su.get_csv_s3(boto_client, bucket, self.key)
        csv_reader = csv.DictReader(sm_open_file)

        for row in csv_reader:
            if float( row['LAT'] ) == min_lat or float( row['LAT'] ) == max_lat or float(
                    row['LON'] ) == min_lon or float( row['LON'] ) == max_lon:
                coord = [float( row['LON'] ), float( row['LAT'] )]

                # check to see if that coordinate has already been appended to the list that is keeping track of our coordinates
                if coord not in coords:
                    coords.append( coord )

        return coords

