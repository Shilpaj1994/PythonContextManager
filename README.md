[toc]

# Context Manager

- Open - Close
- Lock - Release
- Change - Reset
- Enter - Exit
- Start - Stop



[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1L-yGJIME21yQmp8ewpC_M5NtJQ1qZpWh?usp=sharing)

## Applications of Context Manager

### 1. Open File: Built-In

```python
with open('text.txt', 'w') as file:
    print('inside with: file closed?', file.closed)
print('after with: file closed?', file.closed)
```



### 2. Open File: Custom Content Manager

```python
class File:
    def __init__(self, name, mode):
        self.name = name
        self.mode = mode
        
    def __enter__(self):
        print('opening file...')
        self.file = open(self.name, self.mode)
        return self.file
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        print('closing file...')
        self.file.close()
        return False
```

```python
with File('test.txt', 'w') as f:
    f.write('This is some content that we are adding to the file using our own context manager.')
```

```python
with File('test.txt', 'r') as file_ctx:
    print(next(file_ctx))
    print(file_ctx.name)
    print(file_ctx.mode)
```



### 3. Resource Manager: Custom Context Manager

#### With Exception Handling

```python
class ResourceManager:
    def __init__(self, name):
        self.name = name
        self.resource = None
        
    def __enter__(self):
        print('entering context')
        self.resource = ResourceManager(self.name)
        self.resource.state = 'created'
        return self.resource
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        print('exiting context')
        self.resource.state = 'destroyed'
        if exc_type:
            print(f'*** Error occured: {exc_type}, {exc_value}***')
        return True
```

```python
with MyContext() as obj:
    raise ValueError
print('reached here without an exception')
```



#### Without Exception Handling

```python
class ResourceManager:
    def __init__(self, name):
        self.name = name
        self.resource = None
        
    def __enter__(self):
        print('entering context')
        self.resource = ResourceManager(self.name)
        self.resource.state = 'created'
        return self.resource
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        print('exiting context')
        self.resource.state = 'destroyed'
        if exc_type:
            print('error occurred')
        return False
```

```python
with ResourceManager('spam') as res:
    print(f'{res.name} = {res.state}')
print(f'{res.name} = {res.state}')
```



### 4. DataIterator

```python
class DataIterator:
    def __init__(self, fname):
        self._fname = fname
        self._f = None
    
    def __iter__(self):
        return self
    
    def __next__(self):
        row = next(self._f)
        return row.strip('\n').split(',')
    
    def __enter__(self):
        self._f = open(self._fname)
        return self
    
    def __exit__(self, exc_type, exc_value, exc_tb):
        if not self._f.closed:
            self._f.close()
        return False
```

```python
with DataIterator('nyc_parking_tickets_extract.csv') as data:
    for row in data:
        print(row)
```



### 5. Decimal Precision

```python
import decimal
```

```python
class precision:
    def __init__(self, prec):
        self.prec = prec
        self.current_prec = decimal.getcontext().prec

    def __enter__(self):
        decimal.getcontext().prec = self.prec

    def __exit__(self, exc_type, exc_value, exc_tb):
        decimal.getcontext().prec = self.current_prec
        return False
```

```python
decimal.getcontext().prec = 14
with precision(3):
    print(decimal.Decimal(1) / decimal.Decimal(3))

print(decimal.Decimal(1) / decimal.Decimal(3))
```



### 6. Timer

```python
from time import perf_counter, sleep

class Timer:
    def __init__(self):
        self.elapsed = 0

    def __enter__(self):
        self.start = perf_counter()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.stop = perf_counter()
        self.elapsed = self.stop - self.start
        return False
```

```python
with Timer() as timer:
    sleep(1)
print(timer.elapsed)
```



### 7.  Logger

```python
import sys

class OutToFile:
    def __init__(self, fname):
        self._fname = fname
        self._current_stdout = sys.stdout
        
    def __enter__(self):
        self._file = open(self._fname, 'w')
        sys.stdout = self._file
        return self
        
    def __exit__(self, exc_type, exc_value, exc_tb):
        sys.stdout = self._current_stdout
        if self._file:
            self._file.close()
        return False
```

```python
with OutToFile('test.txt') as o:
    print('Line 1')
    print('Line 2')
print('Line 3')
print(o)
```



### 8. HTML Tagging

```python
class Tag:
    def __init__(self, tag):
        self._tag = tag

    def __enter__(self):
        print(f'<{self._tag}>', end = '')

    def __exit__(self, e_t, e_v, e_tr):
        print(f'</{self._tag}>', end='')
        return False
```

```python
with Tag('p'):
    print('In F1, ', end='')
    with Tag('b'):
        print('Mercedes ', end='')
    print(' is the best team.', end='')
```



### 9. List Generator

```python
class ListMaker:
    def __init__(self, title, prefix='- ', indent=3):
        self._title = title
        self._prefix = prefix
        self._indent = indent
        self._current_indent = 0
        print(title)
        
    def __enter__(self):
        self._current_indent += self._indent
        return self
    
    def __exit__(self, exc_type, exc_value, exc_tb):
        self._current_indent -= self._indent
        return False
        
    def print(self, arg):
        s = ' ' * self._current_indent + self._prefix + str(arg)
        print(s)
```

```python
with ListMaker('Items') as lm:
    lm.print('Item 1')
    with lm:
        lm.print('item 1a')
        lm.print('item 1b')
    lm.print('Item 2')
    with lm:
        lm.print('item 2a')
        lm.print('item 2b')

print(lm)
```



---



## Generators and Context Managers

### Generators

```python
def my_gen():
    try:
        print('creating context and yeilding some object')
        lst = [1, 2, 3,4, 5, 'y']
        yield lst
    finally:
        print('exiting the context and cleaning up')

gen = my_gen()
lst = next(gen)
print(lst)
try:
    next(gen)
except StopIteration:
    pass
```



### Generic Context Manager for Generator

```python
class GenCtxManager:
    def __init__(self, gen_func, *args, **kwargs):
        self._gen = gen_func(*args, **kwargs)

    def __enter__(self):
        return next(self._gen)

    def __exit__(self, e_t, e_v, e_tr):
        try:
            next(self._gen)
        except StopIteration:
            pass
        return False
```

```python
with GenCtxManager(my_gen) as lst:
    print(lst)
```



## Context Managers, Generators and Decorators

Convert generator into context manager using decorator

### Custom

```python
def context_manager_dec(gen_fn):
    def helper(*args, **kwargs):
        gen = gen_fn(*args, **kwargs)
        ctx = GenCtxManager(gen)
        return ctx
    return helper
```

```python
@context_manager_dec
def open_file(fname, mode='r'):
    print("opening file")
    f = open(fname, mode)
    try:
        yield f

    finally:
        print("closing the file")
        f.close()
```

```python
with open_file('test.txt') as f:
    print(f.readlines())
```



### Built-In

```python
from contextlib import contextmanager
from time import perf_counter, sleep
```

```python
@contextmanager
def timer():
    stats = dict()
    start = perf_counter()
    stats['start'] = start
    try:
        yield stats
    finally:
        end = perf_counter()
        stats['end'] = end
        stats['elapsed'] = end - start
```

```python
with timer() as stats:
    sleep(1)
    
print(stats)
```



---



## Code Details

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1EeM-SfebFwBRXpjcVcJBnf4O5DElM6CI?usp=sharing)



### Problem Statement

For this project you have 4 files containing information about persons.

The files are:

- `personal_info.csv` - personal information such as name, gender, etc. (one row per person)
- `vehicles.csv` - what vehicle people own (one row per person)
- `employment.csv` - where a person is employed (one row per person)
- `update_status.csv` - when the person's data was created and last updated Each file contains a key, SSN, which uniquely identifies a person.

This key is present in all four files.

You are guaranteed that the same SSN value is present in every file, and that it only appears once per file.

In addition, the files are all sorted by SSN, i.e. the SSN values appear in the same order in each file.



### Solution

#### Goal 1

our first task is to create iterators for each of the four files that contained cleaned up data, of the correct type (e.g. string, int, date, etc), and represented by a named tuple.

For now these four iterators are just separate, independent iterators.

```python
# Standard Library Imports
import csv
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
        
# Create Iterator for all four files
personal_info_iterator = DataIterator('personal_info.csv', 'PersonalInfo', personal_info_data_types)
vehicle_info_iterator = DataIterator('vehicles.csv', 'VehicleInfo', vehicle_info_data_types)
employment_info_iterator = DataIterator('employment.csv', 'EmploymentInfo', employment_info_data_types)
update_info_iterator = DataIterator('update_status.csv', 'UpdateInfo', update_info_data_types)
```



#### Goal 2

Create a single iterable that combines all the columns from all the iterators.

The iterable should yield named tuples containing all the columns. Make sure that the SSN's across the files match!

All the files are guaranteed to be in SSN sort order, and every SSN is unique, and every SSN appears in every file.

Make sure the SSN is not repeated 4 times - one time per row is enough!

```python
# Code section to generate namedtuple for combinedtuple
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

# -------------------------------------------------------------------------------------------------------------------------------

# Since some samples from above Iterators are exhausted, creating new Iterators for combining all the data
# Create Iterator for all four files. Using DataIterator as Context Manager
with DataIterator('personal_info.csv', 'PersonalInfo', personal_info_data_types) as personal_info_iterator:
    with DataIterator('vehicles.csv', 'VehicleInfo', vehicle_info_data_types) as vehicle_info_iterator:
        with DataIterator('employment.csv', 'EmploymentInfo', employment_info_data_types) as employment_info_iterator:
            with DataIterator('update_status.csv', 'UpdateInfo', update_info_data_types) as update_info_iterator:
                # List to store the combined data
                combined_data = []

                # Iterate over each row in all the data
                for personal_data, vehicle_data, employment_data, update_data in zip(personal_info_iterator, vehicle_info_iterator, employment_info_iterator, update_info_iterator):
                    # Dictionary to store all the data
                    temp = dict()

                    # SSN of a person from personal information
                    _ssn = personal_data.ssn

                    # Store each type of a data in a separate temporary dictionary
                    temp_1 = {field: getattr(personal_data, field) for field in personal_data._fields}
                    temp_2 = {field: getattr(vehicle_data, field) for field in vehicle_data._fields if vehicle_data.ssn == _ssn}
                    temp_3 = {field: getattr(employment_data, field) for field in employment_data._fields if employment_data.ssn == _ssn}
                    temp_4 = {field: getattr(update_data, field) for field in update_data._fields if update_data.ssn == _ssn}
                    
                    # Combine 4 different dictionaries into 1 dictionary
                    for data in (temp_1, temp_2, temp_3, temp_4):
                        temp.update(data)

                    # Convert the data into NamedTuple
                    combined_data.append(CombinedData(**temp))

                print(len(combined_data))

# -------------------------------------------------------------------------------------------------------------------------------

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

combined_iterable = DataIterable(5)
[data for data in combined_iterable]
```



#### Goal 3

Next, you want to identify any stale records, where stale simply means the record has not been updated since 3/1/2017 (e.g. last update date < 3/1/2017). Create an iterator that only contains current records (i.e. not stale) based on the last_updated field from the status_update file.

```python
total_dataset = DataIterable(len(combined_data))

# List to store the stale records
stale_records = []
stale_indexes = []
stale_threshold = datetime.datetime(2017, 3, 1, 00, 00, 00)

# Filter out all the stale data and stale indexes
for index, data in enumerate(total_dataset):
    if data.last_updated < stale_threshold:
        stale_records.append(data)
        stale_indexes.append(index)

print(f"Dataset Size: {len(total_dataset)}")

# Create current data by removing the stale data from the combined dataset
print(f"Total Stale Records: {len(stale_indexes)}")

current_records = (data for data in total_dataset if data not in stale_records)

print(f"Is current record an Iterator: {isinstance(current_records, Iterator)}")
```



#### Goal 4

Find the largest group of car makes for each gender.

Possibly more than one such group per gender exists (equal sizes).

```python
# Largest Group of car for each gender in total dataset
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
```

