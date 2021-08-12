import csv
from datetime import datetime

class CsbExtractor:
    """
    A class used to extract geospatial data from csv files in an s3 bucket

    Attributes
    ----------
    su : S3 Utils object
        an instance of the s3 utils class used to connect to the corresponding s3 bucket to get access to the csv file for extraction
    boto_client: boto3 client
        specific boto3 client type (s3, s3_resource, glacier, session) used to access aws resources
    bucket: str
        the name of the s3 bucket in which you want to access
    key: str
        the name of key path for the specific item you want to access in the bucket


    Methods
    -------
    is_csv(file_name)
        checks to see if the given file is of type csv

    get_spatial_temporal_bounds(lon_column_name, lat_column_name, date_column_name)
        extracts min/max longitude and latitude values as well as beginning and ending dates from specified csv file

    extract_coords(max_lon, max_lat, min_lon, min_lat)
        extracts specific coordinates corresponding to min/max longitude and latitude values given from get_spatial_temporal_bounds(....) method
    """

    def __init__(self, su, key):
        """
        :param su: S3 Utils object
            an instance of the s3 utils class used to connect to the corresponding s3 bucket to get access to the csv file for extraction
        :param key: str
            the name of key path for the specific item you want to access in the bucket

        Other Attributes
        ________________
        boto_client: boto3 client
            specific boto3 client type (s3, s3_resource, glacier, session) used to access aws resources
        bucket: str
            the name of the s3 bucket in which you want to access
        """
        self.su = su
        boto_client = self.su.connect("session", None)
        bucket = self.su.conf['s3_bucket']
        self.key = key

    def is_csv(self, file_name):
        """
        Checks to see if the given file is of type csv

        :param file_name: str
            the name of the file in the s3 bucket  i.e. file1.csv

        :return: boolean
            True if the file name contains .csv and False otherwise
        """
        csv_str = '.csv'
        if file_name.endswith(csv_str):
            return True

        return False

    # def smart_open_read(self, key):
    #     boto_client = self.su.connect("session", None)
    #     bucket = self.su.conf['s3_bucket']
    #     self.su.read_csv_s3(boto_client, bucket, key)


    def get_spatial_temporal_bounds(self, lon_column_name, lat_column_name, date_column_name):
        """
        Extracts min/max longitude and latitude values as well as beginning and ending dates from specified csv file

        :param lon_column_name: str
            name of longitude column in the csv file
        :param lat_column_name: str
            name of the latitude column in the csv file
        :param date_column_name: str
            name of the date column in the csv file

        :return: dict
            Key : Value
            geospatial (str)  ->  List[float] containing min/max longitude and latitude values
            temporal (str) -> List[str] containing beginning and end dates

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


    def extract_coords(self, max_lon, max_lat, min_lon, min_lat):
        """
        Extracts specific coordinates corresponding to min/max longitude and latitude values given from get_spatial_temporal_bounds(....) method

        :param max_lon: float
            maximum longitude value
        :param max_lat: float
            maximum latitude value
        :param min_lon: float
            minimum longitude value
        :param min_lat: float
            minimum latitude value

        :return: List[ List[Float] ]
            Returns a list of lists. Each list contains floats (longitude and latitude ) value pairs corresponding to
            one of the min/max latitude and longitude values that were extracted previously from get_spatial_temporal_bounds (...)
        """

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

