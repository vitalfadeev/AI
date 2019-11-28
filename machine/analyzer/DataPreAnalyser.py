import re
import ast
import json
import numpy as np
import pandas as pd

"""
LOCATION:       ...\IXI oo\AI_DataPreAnalyser
DESCRIPTION:    Analyzed data from excel file.
MAIN FUNCTION:  analyse_source_data_find_input_output.

MAIN FUNCTION ANALYZE DATASET AND DETECT TYPES OF COLUMNS:
COLUMN DATATYPE:
    _ OPTION         : column with numbers where are less than 20 different values
    _ NUMERIC        : column with numbers where are more than 20 different values
    _ TAGS           : column with text separated by ",", ";", "/", but not by spaces
    _ TAGS_WEIGHTED  : column with text separated by ",", ";", "/", but not by spaces and followed sometime by "= value"
    _ LABEL          : column with less than 25 distinct values
    _ LABEL_LARGE    : column with more than 25 distinct values
    _ TEXT           : column with text data. Have more spaces than ",", ";"
    _ DATE           : column with data in ##/##/#### date format
    _ DATE_LARGE     : column with data in ##/##/#### date format with more than 50 unique years
    _ TIME           : column with data in ##                                                                            : ## time format
    _ DATETIME       : column with data in ##/##/#### ##                                                                 : ## datetime format
    _ DATETIME_LARGE : column with data in ##/##/#### ##                                                                 : ## datetime format with more than 50 unique years
    _ JSON           : column contain json string
"""

# Regular expression patterns which will used for detecting column with some kind of date
# (datetime, date, time)
regular_expression_for_date = r'[\d]{4}_[\d]{2}_[\d]{2}\s00:00:00'
regular_expression_for_time = r'[\d]{1,2}:[\d]{1,2}'
regular_expression_for_datetime = r'[\d]{4}_[\d]{2}_[\d]{2}\s[\d]{2}:[\d]{2}:[\d]{2}'

threshold_percentage_of_missing_values = 0.1
threshold_percentage_of_number_in_titles = 0.25

all_possible_column_types = ['OPTION', 'FLOAT', 'LABEL', 'LABEL_LARGE', 'TAGS', 'TAGS_WEIGHTED', 'DATE', 'DATE_LARGE',
                             'TIME', 'DATETIME', 'DATETIME_LARGE', 'JSON']

all_possible_text_types = ['TEXT_WORDS_PKN_SMALL', 'TEXT_WORDS_PKN_LARGE', 'TEXT_SENTENCE', 'TEXT_PARAGRAPH']



# Class which contain all properties for analyzed object from file
class AnalyzedObject:

    def __init__(self, brain_mode):
        self.dataset                                = None
        self.brain_mode                             = brain_mode
        self.column_names_input                     = []
        self.column_names_output                    = []
        self.percentage_of_missing_value_for_column = {}
        self.column_types                           = {}
        self.errors_info                            = {}
        self.warning_info                           = {}
        self.count_group_dict_values                = {}
        self.lists_size                             = {}

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


# If in cell is list of values, this function will convert list to tags
def list_of_values_to_tags(x):
    if isinstance(x, list):
        return ';'.join(x)
    elif isinstance(x, str):
        return x
    else:
        return np.nan


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


# Search column with data type _ TAG_WEIGHT (Example: Word=Weight)
def check_tags_weight(column_from_dataset):
    count_tags_weight = 0
    for data in column_from_dataset:
        if pd.notna(data):
            count_tags_weight += str(data).count('=')

    # Check if tags with weight are more than 1%.
    if count_tags_weight > len(column_from_dataset)*threshold_percentage_of_missing_values:
        return 'TAGS_WEIGHT'


def check_json(column_from_dataset):
    count_jsons_dict = 0
    count_jsons_array = 0
    for data in column_from_dataset:
        if pd.notna(data):
            count_jsons_dict += len(re.findall(r'[\[{}\]]', str(data))) if not str(data).startswith('[[') else 0
            count_jsons_array += str(data).count("[[")*2

    if count_jsons_dict >= len(column_from_dataset)*2:
        return 'JSON'
    elif count_jsons_array > count_jsons_dict:
        return 'JSON_ARRAY_OF_ARRAYS'


# Check string data type in column (tags (words split by comma, dotcomma), just words, text)
def check_tags(column_from_dataset):

    count_tags = 0
    count_space = 0
    count_urls = 0

    for data in column_from_dataset:
        # tags can be split by ',' or ';'. Labels are split by space
        count_tags += len(re.findall(r'[,;]', str(data)))
        count_space += len(re.findall(r' ', str(data)))
        count_urls += len(re.findall(r'http://|https://', str(data)))

    # Return most common type
    if count_space > len(column_from_dataset) * 3:

        count_words = max([len(re.findall(r'[\w]+', value)) for value in column_from_dataset.values])
        if count_words <= 5 and len(column_from_dataset) < 1000:
            return 'TEXT_WORDS_PKN_SMALL'

        elif count_words <= 5 and len(column_from_dataset) >= 1000:
            return 'TEXT_WORDS_PKN_LARGE'

        elif 35 >= count_words >= 5:
            return 'TEXT_SENTENCE'

        else:
            return 'TEXT_PARAGRAPH'

    elif count_urls:
        return 'URL'

    elif count_tags > count_space:
        return 'TAGS'

    else:
        unique_labels_count = len(pd.unique(column_from_dataset))
        if unique_labels_count < 25:
            return 'LABEL'
        else:
            return 'LABEL_LARGE'


# Using this function to check most common type of data in column with different data types
def check_most_common_type_for_column(analyzer_object, column_from_dataset):

    count_number = 0
    count_string = 0
    for data in column_from_dataset:
        # tags can be split by ',' or ';'. Labels are split by space
        count_string += len(re.findall(r'[A_Za_z]', str(data)))
        count_number += len(re.findall(r'[0_9]', str(data)))

    # Detect more common type of data and return this
    if count_string > count_number:
        # Check if all data is string values.
        if count_number:
            # Add warning if column have different data types
            analyzer_object.add_warning_info_for_column(column_from_dataset.name, 'This column is string but have some '
                                                                                  'numeric data\n')
        return 'STRINGS'

    elif count_string < count_number:
        # Check if all data is numbers.
        if count_string:
            analyzer_object.add_warning_info_for_column(column_from_dataset.name, 'This column is numeric but have some '
                                                                                  'string data\n')
        return 'FLOAT'


def determine_column_data_type(column, analyzed_object_from_file, dataframe_from_file):

    if dataframe_from_file[column].dtype == np.float64 or dataframe_from_file[column].dtype == np.int64:

        # If in columns with numbers are less than 20 unique values then type of column is OPTION
        if dataframe_from_file[column].nunique() < 20:
            return 'OPTION'

        else:
            return 'FLOAT'

    # Check if data type is DATE or DATE_LARGE
    elif check_date_type(dataframe_from_file[column], regular_expression_for_date):
        if len(dataframe_from_file[column].dt.year.unique()) > 50:
            return 'DATE_LARGE'
        else:
            return 'DATE'

    # Check if data type is DATETIME or DATETIME_LARGE
    elif check_date_type(dataframe_from_file[column], regular_expression_for_datetime):
        if len(dataframe_from_file[column].dt.year.unique())> 50:
            return 'DATETIME_LARGE'
        return 'DATETIME'

    # Check if data type is TIME
    elif check_date_type(dataframe_from_file[column], regular_expression_for_time):
        return 'TIME'

    # In column with type object can be data with different types.
    elif dataframe_from_file[column].dtype == object:
        # Choose most common type
        if check_tags_weight(dataframe_from_file[column]) == 'TAGS_WEIGHT':
            return 'TAGS_WEIGHT'

        elif check_json(dataframe_from_file[column]) == 'JSON':
            # Search types of values in json
            detect_types_in_json_column(analyzed_object_from_file, dataframe_from_file[column])
            analyzed_object_from_file.lists_size[column] = max(len(json.loads(x)) for x in dataframe_from_file[column].values if x is not np.nan)
            return 'JSON'
        elif check_json(dataframe_from_file[column]) == 'JSON_ARRAY_OF_ARRAYS':
            # Search types of values in json
            detect_types_in_json_column(analyzed_object_from_file, dataframe_from_file[column])
            return 'JSON_ARRAY_OF_ARRAYS'

        elif check_most_common_type_for_column(analyzed_object_from_file, dataframe_from_file[column]) == 'STRINGS':
            column_type = check_tags(dataframe_from_file[column])
            # If column type is text and brain_mode is LSTM _ > all text columns become TEXT_WORDS_LIST
            if column_type in all_possible_text_types and analyzed_object_from_file.brain_mode == 'LSTM':

                analyzed_object_from_file.lists_size[column] = max([len(re.findall(r'[\w]+', value)) for value in dataframe_from_file[column].values if value is not None])
                return 'TEXT_WORDS_LIST'

            elif column_type in all_possible_text_types:
                analyzed_object_from_file.lists_size[column] = max(
                    [len(re.findall(r'[\w]+', value)) for value in dataframe_from_file[column].values if
                     value is not None])
                return column_type
            else:
                return column_type

        elif check_most_common_type_for_column(analyzed_object_from_file, dataframe_from_file[column]) == 'FLOAT':
            dataframe_from_file[column] = pd.to_numeric(dataframe_from_file[column], errors='coerce')
            if dataframe_from_file[column].nunique() < 20:
                return 'OPTION'
            else:
                return 'FLOAT'


def detect_types_in_json_column(analyzed_object_from_file, column_from_dataframe):
    all_jsons_strings = []
    if isinstance(ast.literal_eval(column_from_dataframe[0])[0], dict):
        for data in column_from_dataframe:
            if pd.notna(data) and len(ast.literal_eval(data)) == 1:
                all_jsons_strings.append(ast.literal_eval(data)[0])
            else:
                all_jsons_strings.append({})
    elif isinstance(ast.literal_eval(column_from_dataframe[0])[0], list):
        for data in column_from_dataframe:
            if pd.notna(data):
                one_dimensional_list = [item for sum_list_index in range(len(ast.literal_eval(data))) for item in ast.literal_eval(data)[sum_list_index]]
                all_jsons_strings.append({'Col'+str(index): value for index, value in enumerate(one_dimensional_list)})
            else:
                all_jsons_strings.append({})

    new_dataframe_with_jsons = pd.read_json(json.dumps(all_jsons_strings))
    new_dataframe_with_jsons.columns = [column_from_dataframe.name+'_'+str(column) for column in new_dataframe_with_jsons.columns]
    column_types = analyse_source_data_find_input_output(new_dataframe_with_jsons).column_types

    # Save to column types. In future will be used by EncDec
    analyzed_object_from_file.column_types.update(column_types)


# Detect if number of columns with only number in title is more than 25% of all columns. if True _ rename
def rename_columns_with_number_in_title(dataframe_from_file):
    # List contain True if title is number and False if not
    list_of_boolean_values = dataframe_from_file.columns.str.contains(r"^[0_9]")

    # Indexes of columns with number title
    to_rename_columns = [i for i in range(len(list_of_boolean_values)) if list_of_boolean_values[i] is True]

    if len(to_rename_columns) > len(list_of_boolean_values) * threshold_percentage_of_number_in_titles:
        for i in to_rename_columns:
            # Rename column
            dataframe_from_file = dataframe_from_file.rename(
                columns={dataframe_from_file.iloc[:, int(i)].name: 'Column{}'.format(i)})

    return dataframe_from_file


def CountGroupDictValues(DictToGroupCount, ListOfGroups):
    """
    :param DictToGroupCount: dict with columns and their types. Like {column_name: column_type}.
    :return: dict with column type and number of columns with this type.
    """
    """
    Function count types of columns. Save to dictionary.
    """
    from collections import defaultdict

    DictGroupedCounted = []

    # Create dict with all possible types as keys and 0 as default value
    dict_with_counted_types = defaultdict.fromkeys(ListOfGroups, 0)

    # Count types in dict
    for value in DictToGroupCount.values():
        if value in ListOfGroups:
            dict_with_counted_types[value] += 1

    DictGroupedCounted.append(dict(dict_with_counted_types))
    return DictGroupedCounted


def analyse_source_data_find_input_output(loaded_data, brain_mode='RNN', user_input_columns=None, user_output_columns=None):

    analyzed_object_from_file = AnalyzedObject(brain_mode)
    dataframe_from_file = loaded_data

    # Change titles with spaces
    dataframe_from_file.columns = [column_name.replace(' ', '_') for column_name in dataframe_from_file.columns]

    # Change titles with numbers
    # dataframe_from_file = rename_columns_with_number_in_title(dataframe_from_file)

    columns_type = {}

    # User can define by himself output and input column so we just add it to list
    if isinstance(user_input_columns, list):
        analyzed_object_from_file.column_names_input = user_input_columns

    if isinstance(user_output_columns, list):
        analyzed_object_from_file.column_names_output = user_output_columns

    number_of_rows_in_dataset = len(dataframe_from_file)

    # Check size of dataframe. If size == 0 return message with error
    if number_of_rows_in_dataset == 0 or dataframe_from_file is None:
        analyzed_object_from_file.add_error_info_for_column('Dataset', 'Dataset is empty\n')
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

        elif number_of_absent_rows_for_column:
            analyzed_object_from_file.percentage_of_missing_value_for_column[column] = round(number_of_absent_rows_for_column / number_of_rows_in_dataset * 100, 4)

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

    # For each column save their data type
    for column in dataframe_from_file:
        if any(isinstance(value, list) for value in dataframe_from_file[column].values):
            dataframe_from_file[column] = dataframe_from_file[column].apply(list_of_values_to_tags)
        columns_type[column] = determine_column_data_type(column, analyzed_object_from_file, dataframe_from_file)

    # Save dataset properties to object
    analyzed_object_from_file.column_types.update(columns_type)
    analyzed_object_from_file.column_names_input += dataframe_from_file.columns[dataframe_from_file.notna().all()].tolist()
    analyzed_object_from_file.count_group_dict_values = CountGroupDictValues(DictToGroupCount=columns_type,
                                                                             ListOfGroups=all_possible_column_types)
    analyzed_object_from_file.dataset = dataframe_from_file

    return analyzed_object_from_file


if __name__ == '__main__':
    from CreateConnectionToDB import get_db_connection
    data_from_file = pd.read_csv('csvInputDatalines.csv')
    # cn = get_db_connection(AI_CURSOR=True)
    # import json
    A = analyse_source_data_find_input_output(data_from_file, brain_mode='LSTM')
    print('___________________INPUT COLUMNS______________________')
    print(A.column_names_input)
    print('___________________OUTPUT COLUMNS______________________')
    print(A.column_names_output)
    print('___________________Missed values in columns____________')
    print(A.percentage_of_missing_value_for_column)
    print('___________________COLUMN TYPES________________________')
    print(A.column_types)
    print('___________________WARNINGS__________________________')
    print(A.warning_info)
    print('___________________ERRORS___________________________')
    print(A.errors_info)
    print(A.lists_size)

    # cn.execute(f"""UPDATE ai.brains SET AnalysisSource_ListsSize='{json.dumps(A.lists_size)}' WHERE Brain_ID=18""")
