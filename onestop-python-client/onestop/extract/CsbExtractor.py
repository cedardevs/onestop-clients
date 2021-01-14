import csv
import yaml
from datetime import datetime
from onestop.util.ClientLogger import ClientLogger
from onestop.util.S3Utils import S3Utils

class CsbExtractor:
    def __init__(self, conf_loc, s3_utils):
        with open(conf_loc) as f:
            self.conf = yaml.load(f, Loader=yaml.FullLoader)

        self.s3_utils = s3_utils

    # checks if an s3 key is a csv file
    def is_csv(self, s3_key):
        csv_str = '.csv'
        if s3_key.endswith(csv_str):
            return True

        return False

    # Reads file data from a s3 bucket, decodes the data, and returns first line of data from a csv for iteration on rest of the file
    def get_line(self, s3_bucket, s3_key):
        # Use S3Utils to read the file as a raw text
        s3 = self.s3_utils.connect('s3', self.s3_utils.conf['s3_region'])
        file_data = self.s3_utils.read_bytes_s3(s3, s3_bucket, s3_key)

        # Extract the appropriate fields
        line = file_data.decode('utf-8').split('\n')

        return line

    """ 
    - Extracts the max value of a numeric column in a csv file
    - Takes in first line of csv file to be read, and the column name in which you want the max to be extracted
    """

    def get_max_numeric(self, line, column_name):
        max_val = None

        for row in csv.DictReader(line):
            # first iteration, sets max to first element
            if not max_val:
                max_val = float(row[column_name])
            else:
                max_val = max(max_val, float(row[column_name]))

        return max_val

    """ 
        - Extracts the min value of a numeric column in a csv file
        - Takes in first line of csv file to be read, and the column name in which you want the min to be extracted
    """

    def get_min_numeric(self, line, column_name):
        min_val = None

        for row in csv.DictReader(line):
            # first iteration, sets min to first element
            if not min_val:
                min_val = float(row[column_name])
            else:
                min_val = min(min_val, float(row[column_name]))

        return min_val

    """ 
        - Extracts the max value of a date/time column in a csv file, this will end up being the end date
        - Takes in first line of csv file to be read, and the column name in which you want the max to be extracted
    """

    def get_max_datetime(self, line, column_name):
        # variable used for comparison in date time format
        end_date = None
        # variable to be returned in string format
        end_date_str = ''
        for row in csv.DictReader(line):
            # Need to convert the string to python datetime for comparison
            date_time = datetime.strptime(row[column_name].replace('.000Z', '', 1), "%Y-%m-%dT%H:%M:%S")

            # first iteration
            if not end_date:
                end_date = date_time
                end_date_str = row[column_name]
            else:
                if date_time > end_date:
                    end_date = date_time
                    end_date_str = row[column_name]

        return end_date_str

    """ 
        - Extracts the min value of a date/time column in a csv file, this will end up being the start date
        - Takes in first line of csv file to be read, and the column name in which you want the max to be extracted
    """

    def get_min_datetime(self, line, column_name):
        # variable used for comparison in date time format
        begin_date = None
        # variable to be returned in string format
        begin_date_str = ''
        for row in csv.DictReader(line):
            # Need to convert the string to python datetime for comparison
            date_time = datetime.strptime(row[column_name].replace('.000Z', '', 1), "%Y-%m-%dT%H:%M:%S")

            # first iteration
            if not begin_date:
                begin_date = date_time
                begin_date_str = row[column_name]
            else:
                if date_time < begin_date:
                    begin_date = date_time
                    begin_date_str = row[column_name]

        return begin_date_str

    # Given the max/min lon and lat, the function will parse the csv file to extract to according coordinates
    def extract_coords(self, lines, max_lon, max_lat, min_lon, min_lat):
        # Keeps track of all coordinates that needs to be added to json payload
        coords = []

        # Second pass to grab the coordinates of the min and max values for lon and lat
        for row in csv.DictReader(lines):
            if float(row['LAT']) == min_lat or float(row['LAT']) == max_lat or float(row['LON']) == min_lon or float(row['LON']) == max_lon:
                coord = [float(row['LON']), float(row['LAT'])]

                # check to see if that coordinate has already been appended to the list that is keeping track of our coordinates
                if coord not in coords:
                    coords.append(coord)

        return coords

