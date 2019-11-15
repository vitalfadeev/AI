import pandas as pd
import numpy as np
import re

"""
LOCATION:       ...\IXI oo\AI-DataPreAnalyser
DESCRIPTION:    Analyzed data from excel file.
MAIN FUNCTION:  analyse_source_data_find_input_output.
"""

# Regular expression patterns which will used for detecting column with some kind of date
# (datetime, date, time)
regular_expression_for_date = r'[\d]{4}-[\d]{2}-[\d]{2}\s00:00:00'
regular_expression_for_time = r'[\d]{1,2}:[\d]{1,2}'
regular_expression_for_datetime = r'[\d]{4}-[\d]{2}-[\d]{2}\s[\d]{2}:[\d]{2}:[\d]{2}'

threshold_percentage_of_missing_values = 0.01
threshold_percentage_of_number_in_titles = 0.25


# Class which contain all properties for analyzed object from file
class AnalyzedObject:

    def __init__(self):
        self.dataset                           = None
        self.column_names_input                = []
        self.column_names_output               = []
        self.column_types                      = {}
        self.errors_info                       = {}
        self.warning_info                      = {}

    def add_error_info_for_column(self, column, error_message):
        if column not in self.errors_info:
            self.errors_info[column] = error_message
        else:
            self.errors_info[column] += error_message

    def add_warning_info_for_column(self, column, warning_message):
        if column not in self.warning_info:
            self.warning_info[column] = warning_message
        else:
            self.warning_info[column] += warning_message


# Check count of missing values. In output columns should be the same number of missing values
def check_count_of_missing_rows_for_each_output(analyzer_object, columns_with_missing_data_dict):
    # Count unique numbers
    unique_count = set(columns_with_missing_data_dict.values())

    if unique_count == 1:
        return list(columns_with_missing_data_dict.keys())

    # Check columns with less missing values and write warning
    else:
        max_num = max(columns_with_missing_data_dict.values())
        for column in columns_with_missing_data_dict:
            if columns_with_missing_data_dict[column] < max_num:
                analyzer_object.add_warning_info_for_column(column, "In this column are less values than in another "
                                                                    "output columns\n")

        return list(columns_with_missing_data_dict.keys())


# Check type of columns data with regular expression ( Date, DateTime, Time )
def check_date_type(column_from_dataset, reg_pattern):
    return all(len(re.findall(reg_pattern, str(data))) == 1 or pd.isna(data) for data in column_from_dataset)


# Search column with data type - TAG_WEIGHT (Example: Word=Weight)
def check_tags_weight(column_from_dataset):
    count_tags_weight = 0
    for data in column_from_dataset:
        if pd.notna(data):
            count_tags_weight += str(data).count('=')

    # Check if tags with weight are more than 1%.
    if count_tags_weight > len(column_from_dataset)*threshold_percentage_of_missing_values:
        return 'TAGS_WEIGHT'


# Check string data type in column (tags (words split by comma, dotcomma), just words, text)
def check_tags(column_from_dataset):

    count_tags = 0
    count_label = 0
    count_urls = 0

    for data in column_from_dataset:
        # tags can be split by ',' or ';'. Labels are split by space
        count_tags += len(re.findall(r'[,;]', str(data)))
        count_label += len(re.findall(r' ', str(data)))
        count_urls += len(re.findall(r'http://|https://', str(data)))

    # Return most common type
    if count_label > len(column_from_dataset) * 2:
        return 'TEXT'

    elif count_urls:
        return 'URL'

    elif count_tags:
        return 'TAGS'

    else:
        unique_labels_count = len(pd.unique(column_from_dataset))
        if unique_labels_count == 2:
            return 'LABEL_BINARY'
        elif unique_labels_count < 25:
            return 'LABEL'
        else:
            return 'LABEL_LARGE'


# Using this function to check most common type of data in column with different data types
def check_most_common_type_for_column(analyzer_object, column_from_dataset):

    # Using list comprehension to create two list with indexes (for numbers and for string)
    count_numbers = [index for index in range(len(column_from_dataset))
                     if re.findall('[0-9]', str(column_from_dataset[index]))]

    count_string = [index for index in range(len(column_from_dataset))
                    if re.findall('[A-Za-z]', str(column_from_dataset[index]))]

    # Detect more common type of data and return this
    if len(count_string) > len(count_numbers):
        # Check if all data is string values.
        if len(count_string) == len(column_from_dataset):
            return 'STRINGS'
        else:
            # Add warning if column have different data types
            analyzer_object.add_warning_info_for_column(column_from_dataset.name, 'This column is string but have some '
                                                                                  'numeric data\n')
            analyzer_object.lines_to_skip_indexes_list += count_numbers
            return 'STRINGS'

    elif len(count_string) < len(count_numbers):
        analyzer_object.add_warning_info_for_column(column_from_dataset.name, 'This column is numeric but have some '
                                                                              'string data\n')
        analyzer_object.lines_to_skip_indexes_list += count_string
        return 'NUMERIC'


def determine_column_data_type(column, analyzed_object_from_file, dataframe_from_file):

    if dataframe_from_file[column].dtype == np.float64 or dataframe_from_file[column].dtype == np.int64:

        # If in column just 2 different values then type of column is BINARY
        if dataframe_from_file[column].nunique() == 2:
            return 'BINARY'

        # If in columns with numbers are less than 20 unique values then type of column is OPTION
        elif dataframe_from_file[column].nunique() < 20:
            return 'OPTION'

        else:
            return 'NUMERIC'

    elif check_date_type(dataframe_from_file[column], regular_expression_for_date):
        return 'DATE'

    elif check_date_type(dataframe_from_file[column], regular_expression_for_datetime):
        return 'DATETIME'

    elif check_date_type(dataframe_from_file[column], regular_expression_for_time):
        return 'TIME'

    # In column with type object can be data with different types.
    elif dataframe_from_file[column].dtype == object:
        # Choose most common type
        if check_tags_weight(dataframe_from_file[column]) == 'TAGS_WEIGHT':
            return 'TAGS_WEIGHT'

        elif check_most_common_type_for_column(analyzed_object_from_file, dataframe_from_file[column]) == 'STRINGS':
            return check_tags(dataframe_from_file[column])

        elif check_most_common_type_for_column(analyzed_object_from_file, dataframe_from_file[column]) == 'NUMERIC':
            dataframe_from_file[column] = pd.to_numeric(dataframe_from_file[column], errors='coerce')
            if dataframe_from_file[column].nunique() == 2:
                return 'BINARY'

            elif dataframe_from_file[column].nunique() < 20:
                return 'OPTION'
            else:
                return 'NUMERIC'


# Detect if number of columns with only number in title is more than 25% of all columns. if True - rename
def rename_columns_with_number_in_title(dataframe_from_file):
    # List contain True if title is number and False if not
    list_of_boolean_values = dataframe_from_file.columns.str.contains(r"^[0-9]")

    # Indexes of columns with number title
    to_rename_columns = [i for i in range(len(list_of_boolean_values)) if list_of_boolean_values[i] is True]

    if len(to_rename_columns) > len(list_of_boolean_values) * threshold_percentage_of_number_in_titles:
        for i in to_rename_columns:
            # Rename column
            dataframe_from_file = dataframe_from_file.rename(
                columns={dataframe_from_file.iloc[:, int(i)].name: 'Column{}'.format(i)})

    return dataframe_from_file


def analyse_source_data_find_input_output(loaded_data, user_input_columns=None, user_output_columns=None):

    analyzed_object_from_file = AnalyzedObject()
    dataframe_from_file = loaded_data
    print(dataframe_from_file)
    # Change titles with spaces
    dataframe_from_file.columns = [column_name.replace(' ', '_') for column_name in dataframe_from_file.columns]

    # Change titles with numbers
    dataframe_from_file = rename_columns_with_number_in_title(dataframe_from_file)

    columns_type = {}

    # User can define by himself output and input column so we just add it to list
    if isinstance(user_input_columns, list):
        analyzed_object_from_file.column_names_input = user_input_columns

    if isinstance(user_output_columns, list):
        analyzed_object_from_file.column_names_output = user_output_columns

    number_of_rows_in_dataset = len(dataframe_from_file)

    # Check size of dataframe. If size == 0 return message with error
    if number_of_rows_in_dataset == 0 or dataframe_from_file is None:
        analyzed_object_from_file.add_error_info_for_column('Dataset', 'Dataset is empty or bad file format\n')
        return analyzed_object_from_file

    # Search empty column and delete from dataset. Write info to warnings
    empty_columns = dataframe_from_file.columns[dataframe_from_file.isna().all()].tolist()

    # Add warnings that some columns are empty and remove them
    if empty_columns:
        for column in empty_columns:
            analyzed_object_from_file.add_warning_info_for_column(column, "All data is missing in column\n")
            columns_type[column] = 'EMPTY'

    dataframe_from_file = dataframe_from_file.drop(columns=empty_columns)

    # Create list of column names for columns without data in some rows
    list_of_columns_with_missing_values = dataframe_from_file.columns[dataframe_from_file.isna().any()].tolist()

    # Search to_predict_columns
    columns_with_missing_data_dict = {}
    for column in dataframe_from_file.columns:

        number_of_absent_rows_for_column = dataframe_from_file[column].isna().sum()
        if number_of_absent_rows_for_column > number_of_rows_in_dataset * threshold_percentage_of_missing_values:
            columns_with_missing_data_dict[column] = number_of_absent_rows_for_column
            # Remove to_predict column from list with columns with missing data
            list_of_columns_with_missing_values.remove(column)

        elif column in analyzed_object_from_file.column_names_output and column in list_of_columns_with_missing_values:
            list_of_columns_with_missing_values.remove(column)

    # Check if output columns are found and save output column names to analyzed object
    if len(columns_with_missing_data_dict) > 0:
        output_column_detected_by_analyser = check_count_of_missing_rows_for_each_output(analyzed_object_from_file,
                                                                                         columns_with_missing_data_dict)
        for output_column in output_column_detected_by_analyser:
            if output_column not in analyzed_object_from_file.column_names_output:
                analyzed_object_from_file.column_names_output.append(output_column)

    elif len(columns_with_missing_data_dict) == 0 and len(analyzed_object_from_file.column_names_output) == 0:
        analyzed_object_from_file.add_error_info_for_column('DATASET', 'Columns to predict not found\n')

    # Write warning message for all columns if column have nan and column not to_predict
    if list_of_columns_with_missing_values:
        for column in list_of_columns_with_missing_values:
            analyzed_object_from_file.add_warning_info_for_column(column, 'Have missing data in some rows\n')

    # Remove all rows with nan if nan not in to_predict column
    dataframe_from_file = dataframe_from_file.dropna(subset=list_of_columns_with_missing_values).reset_index(drop=True)

    # For each column save their data type
    for column in dataframe_from_file:
        columns_type[column] = determine_column_data_type(column, analyzed_object_from_file, dataframe_from_file)
        if columns_type[column] == 'TEXT':
            dataframe_from_file = dataframe_from_file.drop(columns=column)

    # Save dataset properties to object
    analyzed_object_from_file.column_types = columns_type
    analyzed_object_from_file.column_names_input += dataframe_from_file.columns[dataframe_from_file.notna().all()].tolist()

    analyzed_object_from_file.dataset = dataframe_from_file

    return analyzed_object_from_file


if __name__ == '__main__':
    data_from_file = pd.read_excel('datasets/wine.xls')
    A = analyse_source_data_find_input_output(data_from_file)
    print('-------------------INPUT COLUMNS----------------------')
    print(A.column_names_input)
    print('-------------------OUTPUT COLUMNS----------------------')
    print(A.column_names_output)
    print('-------------------COLUMN TYPES------------------------')
    print(A.column_types)
    print('-------------------WARNINGS--------------------------')
    print(A.warning_info)
    print('-------------------ERRORS---------------------------')
    print(A.errors_info)
