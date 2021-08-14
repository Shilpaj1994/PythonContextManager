"""
Module to read the files using context manager
Author: Shilpaj Bhalerao
Date: Aug 09, 2021
"""
# Standard Library Imports
import csv
import copy
import datetime
from collections import namedtuple, Counter
from itertools import islice
from collections.abc import Iterator, Iterable


# NamedTuples used for casting data
SSN = namedtuple('SSN', "AreaNumber GroupNumber SerialNumber")
Date = namedtuple('Date', "month day year")
DateTime = namedtuple('DateTime', "Year Month Day Hour Minute Second")

# Casted Data Format
personal_info_data_types = ['SSN', 'STRING', 'STRING', 'STRING', 'STRING']
vehicle_info_data_types = ['SSN', 'STRING', 'STRING', 'INT']
employment_info_data_types = ['STRING', 'STRING', 'STRING', 'SSN']
update_info_data_types = ['SSN', 'DateTime', 'DateTime']


class DataIterator:
    def __init__(self, fname, data_category, expected_data_types):
        self._fname = fname
        self._f = None
        self.headers = None
        self._data_category = data_category
        self._namedtuple = None
        self.expected_data_types = expected_data_types

        # Read and cast the data in proper namedtuple format
        self._f = DataIterator.read_file(self._fname)
        self.headers = next(self._f)
        self._namedtuple = namedtuple(self._data_category, self.headers)
        self.casted_data = (DataIterator.cast_row(self._namedtuple, row, self.expected_data_types) for row in self._f)

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.casted_data)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        return False

    @staticmethod
    def read_file(filename):
        """
        Function to read the csv file
        :param filename: Name of the file
        :return: Row from the file
        """
        with open(filename) as file:
            rows = csv.reader(file, delimiter=',', quotechar='"')
            yield from rows

    @staticmethod
    def cast_row(named_tuple, data_row, data_type):
        """
        Function to return the casted value of the data row
        :param named_tuple: Instance of namedtuple in which the output is expected
        :param data_row: Input data row
        :param data_type: Expected data type
        :return: Data row in the converted format
        """
        casted_data = (DataIterator.cast(data_type, value) for data_type, value in zip(data_type, data_row))

        _data = named_tuple(*casted_data)
        return _data

    @staticmethod
    def cast(data_type, value):
        """
        Function to cast appropriate data type for the input value
        :param data_type: Expected data type
        :param value: Input value
        :return: Converted value in the data_type
        """
        if data_type == 'STRING':
            return str(value)
        elif data_type == 'INT':
            return int(value)
        elif data_type == 'DATE':
            value = value.split('/')
            return Date(*value)
        elif data_type == 'SSN':
            value = value.split('-')
            return SSN(*value)
        elif data_type == 'DateTime':
            _date, _time = value.split('T')
            _date = _date.split('-')
            _time_data, _ = _time.split('Z')
            _time = _time_data.split(':')
            _datetime_date = _date + _time
            _format = [int(element) for element in _datetime_date]
            return datetime.datetime(*_format)


def goal_1():
    """
    Function to create iterators for each of the four files and represented by a named tuple.
    """
    # Create Iterator for all four files
    personal_info_iterator = DataIterator('personal_info.csv', 'PersonalInfo', personal_info_data_types)
    vehicle_info_iterator = DataIterator('vehicles.csv', 'VehicleInfo', vehicle_info_data_types)
    employment_info_iterator = DataIterator('employment.csv', 'EmploymentInfo', employment_info_data_types)
    update_info_iterator = DataIterator('update_status.csv', 'UpdateInfo', update_info_data_types)

    # Check if instances are Iterators
    print(f"Is `personal_info_iterator` an Iterator: {isinstance(personal_info_iterator, Iterator)}")
    print(f"Is `vehicle_info_iterator` an Iterator: {isinstance(vehicle_info_iterator, Iterator)}")
    print(f"Is `employment_info_iterator` an Iterator: {isinstance(employment_info_iterator, Iterator)}")
    print(f"Is `update_info_iterator` an Iterator: {isinstance(update_info_iterator, Iterator)}")


def goal_2():
    """
    Function to create single Iterable that combines all the data and yield named tuples
    """
    # Create Iterator for all four files
    personal_info_iterator = DataIterator('personal_info.csv', 'PersonalInfo', personal_info_data_types)
    vehicle_info_iterator = DataIterator('vehicles.csv', 'VehicleInfo', vehicle_info_data_types)
    employment_info_iterator = DataIterator('employment.csv', 'EmploymentInfo', employment_info_data_types)
    update_info_iterator = DataIterator('update_status.csv', 'UpdateInfo', update_info_data_types)

    # Extract each row from the Iterator
    combined_fields = []
    row1 = next(personal_info_iterator)
    row2 = next(vehicle_info_iterator)
    row3 = next(employment_info_iterator)
    row4 = next(update_info_iterator)

    # Collect all the field names from the namedtuple data
    [combined_fields.append(field) for field in row1._fields]
    [combined_fields.append(field) for field in row2._fields]
    [combined_fields.append(field) for field in row3._fields]
    [combined_fields.append(field) for field in row4._fields]

    # Remove the repeated fileds
    combined_fields = set(combined_fields)
    print(combined_fields)

    # Create NamedTuple for Combined Data
    CombinedData = namedtuple('CombinedData', combined_fields)

    # Since some samples from above Iterators are exhausted, creating new Iterators for combining all the data
    # Create Iterator for all four files
    with DataIterator('personal_info.csv', 'PersonalInfo', personal_info_data_types) as personal_info_iterator:
        with DataIterator('vehicles.csv', 'VehicleInfo', vehicle_info_data_types) as vehicle_info_iterator:
            with DataIterator('employment.csv', 'EmploymentInfo',
                              employment_info_data_types) as employment_info_iterator:
                with DataIterator('update_status.csv', 'UpdateInfo', update_info_data_types) as update_info_iterator:
                    # List to store the combined data
                    combined_data = []

                    # Iterate over each row in all the data
                    for personal_data, vehicle_data, employment_data, update_data in zip(personal_info_iterator,
                                                                                         vehicle_info_iterator,
                                                                                         employment_info_iterator,
                                                                                         update_info_iterator):
                        # Dictionary to store all the data
                        temp = dict()

                        # SSN of a person from personal information
                        _ssn = personal_data.ssn

                        # Store each type of a data in a separate temporary dictionary
                        temp_1 = {field: getattr(personal_data, field) for field in personal_data._fields}
                        temp_2 = {field: getattr(vehicle_data, field) for field in vehicle_data._fields if
                                  vehicle_data.ssn == _ssn}
                        temp_3 = {field: getattr(employment_data, field) for field in employment_data._fields if
                                  employment_data.ssn == _ssn}
                        temp_4 = {field: getattr(update_data, field) for field in update_data._fields if
                                  update_data.ssn == _ssn}

                        # Combine 4 different dictionaries into 1 dictionary
                        for data in (temp_1, temp_2, temp_3, temp_4):
                            temp.update(data)

                        # Convert the data into NamedTuple
                        combined_data.append(CombinedData(**temp))

                    print(len(combined_data))

    # Create an Iterable from Generator to yield the data
    class DataIterable:
        def __init__(self, n):
            self._n = n
            self._dataset = combined_data

        def __len__(self):
            return len(self._dataset)

        def __iter__(self):
            return DataIterable.fetch_data(self._n)

        @staticmethod
        def fetch_data(n):
            for i in range(n):
                yield combined_data[i]

    # Create an Iterable to print 5 samples
    combined_iterable = DataIterable(5)
    samples = [data for data in combined_iterable]
    print(samples)
    return DataIterable(len(combined_data))


def goal_3(dataset):
    """
    Function to Identify the stale records and return current records
    """
    # List to store the stale records
    stale_records = []
    stale_indexes = []
    stale_threshold = datetime.datetime(2017, 3, 1, 00, 00, 00)

    # Filter out all the stale data and stale indexes
    for index, data in enumerate(dataset):
        if data.last_updated < stale_threshold:
            stale_records.append(data)
            stale_indexes.append(index)

    # Create an Iterator for current records by removing the stale records from the dataset
    current_records = (data for data in dataset if data not in stale_records)

    # Print if the current_records is an Iterators
    print(f"Is current record an Iterator: {isinstance(current_records, Iterator)}")

    return current_records, dataset


def goal_4(total_dataset):
    """
    Function to print the largest group of car makes for each gender
    """
    vehicle_make_data_male = []
    vehicle_make_data_female = []

    for data in total_dataset:
        if data.gender == 'Male':
            vehicle_make_data_male.append(data.vehicle_make)
        elif data.gender == "Female":
            vehicle_make_data_female.append(data.vehicle_make)

    male_counter = Counter(vehicle_make_data_male)
    max_count_vehicle_make_male = max(male_counter.values())
    largest_group_of_car_for_male = [key for key, value in male_counter.items() if value == max_count_vehicle_make_male]
    print(f"Largest Group of Car for Male is {largest_group_of_car_for_male} with a number of {max_count_vehicle_make_male}")

    female_counter = Counter(vehicle_make_data_female)
    max_count_vehicle_make_female = max(female_counter.values())
    largest_group_of_car_for_female = [key for key, value in female_counter.items() if value == max_count_vehicle_make_female]
    print(f"Largest Group of Car for Female is {largest_group_of_car_for_female} with a number of {max_count_vehicle_make_female}")


if __name__ == '__main__':
    # Goal 1
    print("Goal 1 Output: ")
    goal_1()

    # Goal 2
    print("  ")
    print("Goal 2 Output: ")
    combined_iterable = goal_2()

    # Goal 3
    print("  ")
    print("Goal 3 Output: ")
    current_records, total_dataset = goal_3(combined_iterable)
    print(current_records)

    # Goal 4
    print("  ")
    print("Goal 4 Output: ")
    goal_4(total_dataset)
