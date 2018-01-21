from calendar import monthrange
from dateutil.parser import parse
from datetime import datetime
import re
from os import listdir
from os.path import isfile, join


def process_files(data_directory):
    all_files = [file for file in listdir(data_directory) if isfile(join(data_directory, file))]
    mocap_file_pattern = r"^yellow_tripdata_(?P<year>\d+)-(?P<month>\d+)\.csv$"

    for file in all_files:

        m = re.match(mocap_file_pattern, file)
        if m is None:
            print("Skipping file " + file + " because " +
                  "it doesn't match pattern.")
            continue
        else:
            print("Processing " + file)

        with open(join(data_directory, file), 'r') as f:
            header_line = f.readline()
            header = {}
            for head in header_line.split(','):
                header[head] = len(header)
            f.readline()  # empty line

            week_files = {}
            for data_line in f:
                try:
                    data = data_line.split(',')
                    pickup_datetime = data[header['pickup_datetime']]
                    dropoff_datetime = data[header['dropoff_datetime']]

                    date = parse(pickup_datetime)
                    # weeknumber = datetime.date(date).isocalendar()[1]
                    weeknumber = datetime.date(date).timetuple().tm_yday

                    if weeknumber in week_files:
                        file_to_write = week_files[weeknumber]
                    elif isfile(join(data_directory, str(weeknumber))):
                        week_files[weeknumber] = open(join(data_directory, str(weeknumber)), 'a')
                        file_to_write = week_files[weeknumber]
                    else:
                        week_files[weeknumber] = open(join(data_directory, str(weeknumber)), 'a')
                        file_to_write = week_files[weeknumber]
                        file_to_write.write(header_line)
                        file_to_write.write('')

                    file_to_write.write(data_line)

                except ValueError:
                    print("Bad line: " + data_line)

            for week_file in week_files.values():
                week_file.close()


if __name__ == '__main__':
    process_files('aaa')
