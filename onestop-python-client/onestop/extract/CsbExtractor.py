import csv
from datetime import datetime

class CsbExtractor:

    """
    A class used to extract geospatial data from csv files in an s3 bucket

    Methods
    -------
    is_csv(file_name)
        Verifies a file name ends with '.csv'

    get_spatial_temporal_bounds(lon_column_name, lat_column_name, date_column_name)
        Gets the spacial bounding box for the open file. This seeks to the start of the file at start and the end.

    extract_coords(max_lon, max_lat, min_lon, min_lat)
        Given the max/min lon and lat, the function will parse the csv file to extract the coordinates within the given bounding box.
    """

    @staticmethod
    def is_csv(file_name):
        """
        Verifies a file name ends with '.csv'

        :param file_name: str
            File name with extension on the end.

        :return: str
            True if ends with csv
            False if doesn't end with csv
        """
        csv_str = '.csv'
        if file_name.endswith(csv_str):
            return True

        return False

    @staticmethod
    def get_spatial_temporal_bounds(sm_open_file, lon_column_name, lat_column_name, date_column_name):
        """
        Gets the spacial bounding box for the open file. This seeks to the start of the file at start and the end.

        :param sm_open_file: file-like object
            A file-like object that is open, say from smart_open's sm_open.
        :param lon_column_name: str
            Longitude column name
        :param lat_column_name: str
            Latitude column name
        :param date_column_name: str
            Date column name

        :return: dict
            geospatial and temporal fields of the bounding box for given constraints.
        """
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

        sm_open_file.seek(0)
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

        sm_open_file.seek(0)
        return geospatial_temporal_bounds

    @staticmethod
    def extract_coords(sm_open_file, max_lon, max_lat, min_lon, min_lat):
        """
        Given the max/min lon and lat, the function will parse the csv file to extract the coordinates within the given bounding box.

        :param sm_open_file: file-like object
            A file-like object that is open, say from smart_open's sm_open.
        :param max_lon: str
            Maximum longitude
        :param max_lat: str
            Maximum latitude
        :param min_lon: str
            Minimum longitude
        :param min_lat: str
            Minimum latitude

        :return: list
            List of the the coordinates (no duplicates) within the file that are within the given bounding box.
        """

        coords = []

        sm_open_file.seek(0)
        csv_reader = csv.DictReader(sm_open_file)
        for row in csv_reader:
            if float( row['LAT'] ) == min_lat or float( row['LAT'] ) == max_lat or \
               float( row['LON'] ) == min_lon or float( row['LON'] ) == max_lon:
                coord = [float( row['LON'] ), float( row['LAT'] )]
                # if this coordinate has already been appended to the list to return (no duplicates)
                if coord not in coords:
                    coords.append( coord )

        sm_open_file.seek(0)
        return coords
