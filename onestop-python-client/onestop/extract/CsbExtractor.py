import csv
from datetime import datetime

class CsbExtractor:

    def __init__(self, file_name):
        self.file_name= file_name

    # Function to check if a file is a csv file
    def is_csv(self, file_name):
        csv_str = '.csv'
        if file_name.endswith(csv_str):
            return True

        return False


    """ 
    - Extracts the max value of a numeric column in a csv file
    - Takes in first line of csv file to be read, and the column name in which you want the max to be extracted
    """
    def get_max_numeric(self, column_name):
        max_val = None

        # open file and read the contents
        with open(self.file_name, newline='') as csv_file:
            # reads data
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
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
    def get_min_numeric(self, column_name):
        min_val = None

        # open file and read the contents
        with open(self.file_name, newline='') as csv_file:
            # reads data
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
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
    def get_max_datetime(self, column_name):
        # variable used for comparison in date time format
        end_date = None
        # variable to be returned in string format
        end_date_str = ''

        # open file and read the contents
        with open(self.file_name, newline='') as csv_file:
            # reads data
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
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
    def get_min_datetime(self, column_name):
        # variable used for comparison in date time format
        begin_date = None
        # variable to be returned in string format
        begin_date_str = ''

        with open(self.file_name, newline='') as csv_file:
            # reads data
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
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
    def extract_coords(self, max_lon, max_lat, min_lon, min_lat):
        # Keeps track of all coordinates that needs to be added to json payload
        coords = []

        with open(self.file_name, newline='') as csv_file:
            # reads data
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                if float(row['LAT']) == min_lat or float(row['LAT']) == max_lat or float(row['LON']) == min_lon or float(row['LON']) == max_lon:
                    coord = [float(row['LON']), float(row['LAT'])]

                    # check to see if that coordinate has already been appended to the list that is keeping track of our coordinates
                    if coord not in coords:
                        coords.append(coord)

        return coords

