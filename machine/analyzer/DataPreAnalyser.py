import re
import json
import numpy as np
import pandas as pd
"""
LOCATION:       ...\IXI oo\AI-DataPreAnalyser
DESCRIPTION:    Analyzed data from excel file.
MAIN FUNCTION:  analyse_source_data_find_input_output.

MAIN FUNCTION ANALYZE DATASET AND DETECT TYPES OF COLUMNS:
Datatypes are explained in the file I:\IXIoo\AI-DataPreAnalyser\DataTypes (full Schema with parameters).xlsx

"""


# Regular expression patterns which will used for detecting column with some kind of date
# (datetime, date, time)
regular_expression_for_date = r'[\d]{4}-[\d]{2}-[\d]{2}\s00:00:00'
regular_expression_for_time = r'[\d]{1,2}:[\d]{1,2}'
regular_expression_for_datetime = r'[\d]{4}-[\d]{2}-[\d]{2}\s[\d]{2}:[\d]{2}:[\d]{2}'

threshold_percentage_of_missing_values = 0.1
threshold_percentage_of_number_in_titles = 0.25

all_possible_column_types = ['OPTION', 'FLOAT', 'LABEL', 'LABEL_LARGE', 'TAGS', 'TAGS_WEIGHT', 'DATE', 'DATE_LARGE',
                             'TIME', 'DATETIME', 'DATETIME_LARGE', 'JSON1D', 'JSON2D', 'TEXT_WORDS', 'TEXT_SENTENCE',
                             'TEXT_PARAGRAPH']

all_possible_text_types = ['TEXT_WORDS', 'TEXT_SENTENCE', 'TEXT_PARAGRAPH']


# Class which contain all properties for analyzed object from file
class AnalyzedObject:

    def __init__(self):
        self.dataset                                      = None
        self.AnalysisSource_ColumnsNameInput              = {}
        self.AnalysisSource_ColumnsNameOutput             = {}
        self.AnalysisSource_ColumnsMissingPercentage      = {}
        self.AnalysisSource_ColumnsType                   = {}
        self.AnalysisSource_Errors                        = {}
        self.AnalysisSource_Warnings                      = {}
        self.AnalysisSource_ColumnType_GroupCountDataType = {}
        self.AnalysisSource_ColumnsListMaxSize                   = {}

    def add_error_info_for_column(self, column, error_message):
        if column not in self.AnalysisSource_Errors:
            self.AnalysisSource_Errors[column] = error_message
        else:
            self.AnalysisSource_Errors[column] += error_message

    def add_warning_info_for_column(self, column, warning_message):
        if column not in self.AnalysisSource_Warnings:
            self.AnalysisSource_Warnings[column] = warning_message
        else:
            self.AnalysisSource_Warnings[column] += warning_message


# If in cell is list of values, this function will convert list to tags
def list_of_values_to_tags(x):
    x = str(x)
    if isinstance(x, list):
        return ';'.join(x)
    elif isinstance(x, str):
        return x
    else:
        return np.nan


def try_literal_eval(x):
    if isinstance(x, str):
        x = x.replace("'", '"')
        try:
            return json.loads(x)
        except:
            return json.loads(json.dumps(x))
    else:
        return x


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
                                                                    "output columns")

        return list(columns_with_missing_data_dict.keys())


# Check type of columns data with regular expression ( Date, DateTime, Time )
def check_date_type(column_from_dataset, reg_pattern):
    try:
        column_from_dataset = pd.to_datetime(column_from_dataset)
    except:
        return False

    return all(re.match(reg_pattern, str(data)) or pd.isna(data) for data in column_from_dataset)


# Search column with data type - TAG_WEIGHT (Example: Word=Weight)
def check_tags_weight(column_from_dataset):
    count_tags_weight = 0
    for data in column_from_dataset:
        if isinstance(data, list):
            continue

        if pd.notna(data):
            count_tags_weight += str(data).count('=')

    # Check if tags with weight are more than 1%.
    if count_tags_weight > len(column_from_dataset)*threshold_percentage_of_missing_values:
        return 'TAGS_WEIGHT'


def check_json(column_from_dataset):
    count_jsons_dict = 0
    count_jsons_array = 0
    for data in column_from_dataset:
        count_jsons_dict += len(re.findall(r'[\[{}\]]', str(data))) if not str(data).startswith('[[') else 0
        count_jsons_array += str(data).count("[[")*2

    if count_jsons_dict >= len(column_from_dataset):
        return 'JSON1D'

    elif count_jsons_array > count_jsons_dict:
        return 'JSON2D'


# Check string data type in column (tags (words split by comma, dotcomma), just words, text)
def check_tags(column_from_dataset):

    count_tags = 0
    count_space = 0

    for data in column_from_dataset:
        # tags can be split by ',' or ';'. Labels are split by space
        count_tags += len(re.findall(r'[,;]', str(data)))
        count_space += len(re.findall(r' ', str(data)))

    # Return most common type
    if count_space > len(column_from_dataset) * 2:
        count_words = max([len(value.split()) for value in column_from_dataset.values])
        if count_words <= 5:
            return 'TEXT_WORDS'

        elif 35 >= count_words > 5:
            return 'TEXT_SENTENCE'

        else:
            return 'TEXT_PARAGRAPH'

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
        count_string += len(re.findall(r'[A-Za-z]', str(data)))
        count_number += len(re.findall(r'[0-9]', str(data)))

    # Detect more common type of data and return this
    if count_string > count_number:
        # Check if all data is string values.
        if count_number:
            # Add warning if column have different data types
            analyzer_object.add_warning_info_for_column(column_from_dataset.name, 'This column is string but have some '
                                                                                  'numeric data')
        return 'STRINGS'

    elif count_string < count_number:
        # Check if all data is numbers.
        if count_string:
            analyzer_object.add_warning_info_for_column(column_from_dataset.name, 'This column is numeric but have some '
                                                                                  'string data')
        return 'FLOAT'


def check_url_type(x):
    return bool(re.match(r"http://|https://", x))


def determine_column_data_type(column, analyzed_object_from_file, dataframe_from_file):

    if dataframe_from_file[column].dtype == np.float64 or dataframe_from_file[column].dtype == np.int64:

        # If in columns with numbers are less than 20 unique values then type of column is OPTION
        if dataframe_from_file[column].nunique() < 20:
            return 'OPTION'

        else:
            return 'FLOAT'

    # In column with type object can be data with different types.
    elif dataframe_from_file[column].dtype == object:
        # Choose most common type
        if all(dataframe_from_file[column].dropna().apply(check_url_type)):
            return 'URL'

        elif check_tags_weight(dataframe_from_file[column]) == 'TAGS_WEIGHT':
            return 'TAGS_WEIGHT'

        elif check_json(dataframe_from_file[column]) == 'JSON1D':
            # Search types of values in json
            detect_types_in_json_column(analyzed_object_from_file, dataframe_from_file[column])
            analyzed_object_from_file.AnalysisSource_ColumnsListMaxSize[column] = max(len(try_literal_eval(x)) for x in dataframe_from_file[column].values if x is not np.nan)
            return 'JSON1D'

        elif check_json(dataframe_from_file[column]) == 'JSON2D':
            # Search types of values in json
            x_axis_length = max(len(try_literal_eval(x)) for x in dataframe_from_file[column] if x is not np.nan)
            y_axis_length = max(len(y) for x in dataframe_from_file[column] if x is not np.nan for y in try_literal_eval(x))
            analyzed_object_from_file.AnalysisSource_ColumnsListMaxSize[column] = {'x': x_axis_length, 'y': y_axis_length}

            return 'JSON2D'

        elif check_most_common_type_for_column(analyzed_object_from_file, dataframe_from_file[column]) == 'STRINGS':
            column_type = check_tags(dataframe_from_file[column])
            if column_type in all_possible_text_types:
                analyzed_object_from_file.AnalysisSource_ColumnsListMaxSize[column] = max(
                    [len(value.split()) for value in dataframe_from_file[column].values if
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

    # Check if data type is DATE or DATE-LARGE
    elif check_date_type(dataframe_from_file[column], regular_expression_for_date):
        dataframe_from_file[column] = pd.to_datetime(dataframe_from_file[column])
        if len(dataframe_from_file[column].dt.year.unique()) > 50:
            return 'DATE_LARGE'
        else:
            return 'DATE'

    # Check if data type is DATETIME or DATETIME-LARGE
    elif check_date_type(dataframe_from_file[column], regular_expression_for_datetime):
        dataframe_from_file[column] = pd.to_datetime(dataframe_from_file[column])
        if len(dataframe_from_file[column].dt.year.unique()) > 50:
            return 'DATETIME_LARGE'
        return 'DATETIME'

    # Check if data type is TIME
    elif check_date_type(dataframe_from_file[column], regular_expression_for_time):
        return 'TIME'


def detect_types_in_json_column(analyzed_object_from_file, column_from_dataframe):
    all_jsons_strings = []

    # Denis work =(
    if isinstance(try_literal_eval(column_from_dataframe[0])[0], dict):
        for data in column_from_dataframe:
            if pd.notna(data) and len(try_literal_eval(data)) == 1:
                all_jsons_strings.append(try_literal_eval(data)[0])
            else:
                all_jsons_strings.append({})

    elif isinstance(try_literal_eval(column_from_dataframe[0])[0], list):

        if isinstance(try_literal_eval(column_from_dataframe[0])[0], list):
            for data in column_from_dataframe:
                if data is not None:
                    one_dimensional_list = [item for sum_list_index in range(len(data)) for item in data[sum_list_index]]
                    all_jsons_strings.append({'Col'+str(index): value for index, value in enumerate(one_dimensional_list)})
                else:
                    all_jsons_strings.append({})
        else:
            for data in column_from_dataframe:
                if isinstance(data, list) and not pd.isna(data).all() or not pd.isna(data):
                    all_jsons_strings.append({'Col'+str(index): value for index, value in enumerate(data)})
                else:
                    all_jsons_strings.append({})

    new_dataframe_with_jsons = pd.read_json(json.dumps(all_jsons_strings))
    new_dataframe_with_jsons.columns = [column_from_dataframe.name+'-'+str(column) for column in new_dataframe_with_jsons.columns]
    column_types = analyse_source_data_find_input_output(new_dataframe_with_jsons).AnalysisSource_ColumnsType
    # analyzed_object_from_file.column_names_output += \
    #     [column_from_dataframe.name+'-'+str(column) for column in new_dataframe_with_jsons.columns]

    # Save to column types. In future will be used by EncDec
    analyzed_object_from_file.AnalysisSource_ColumnsType.update(column_types)


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


def analyse_source_data_find_input_output(loaded_data, user_input_columns=None, user_output_columns=None):
    
    analyzed_object_from_file = AnalyzedObject()
    dataframe_from_file = loaded_data

    # Change titles with spaces
    dataframe_from_file.columns = [column_name.replace(' ', '_') for column_name in dataframe_from_file.columns]

    # Change titles with numbers
    # dataframe_from_file = rename_columns_with_number_in_title(dataframe_from_file)

    columns_type = {}

    # User can define by himself output and input column so we just add it to list
    if isinstance(user_input_columns, list):
        analyzed_object_from_file.AnalysisSource_ColumnsNameInput = {column: True for column in user_input_columns}

    if isinstance(user_output_columns, list):
        analyzed_object_from_file.AnalysisSource_ColumnsNameOutput = {column: True for column in user_output_columns}

    number_of_rows_in_dataset = len(dataframe_from_file)

    # Check size of dataframe. If size == 0 return message with error
    if number_of_rows_in_dataset == 0 or dataframe_from_file is None:
        analyzed_object_from_file.add_error_info_for_column('Dataset', 'Dataset is empty')
        return analyzed_object_from_file

    # Search empty column and delete from dataset. Write info to warnings
    empty_columns = dataframe_from_file.columns[dataframe_from_file.isna().all()].tolist()

    # Add warnings that some columns are empty and remove them
    if empty_columns:
        for column in empty_columns:
            analyzed_object_from_file.add_warning_info_for_column(column, "All data is missing in column")
            columns_type[column] = 'EMPTY'

    dataframe_from_file = dataframe_from_file.drop(columns=empty_columns)

    list_of_columns_with_missing_values = dataframe_from_file.columns[dataframe_from_file.isna().any()].tolist()
    # Search to_predict_columns
    columns_with_missing_data_dict = {}
    for column in dataframe_from_file.columns:

        number_of_absent_rows_for_column = dataframe_from_file[column].isna().sum()
        if number_of_absent_rows_for_column > number_of_rows_in_dataset * threshold_percentage_of_missing_values:
            columns_with_missing_data_dict[column] = number_of_absent_rows_for_column
            # Remove to_predict column from list with columns with missing data
            list_of_columns_with_missing_values.remove(column)

        elif column in analyzed_object_from_file.AnalysisSource_ColumnsNameOutput and column in list_of_columns_with_missing_values:
            list_of_columns_with_missing_values.remove(column)

        elif number_of_absent_rows_for_column:
            analyzed_object_from_file.AnalysisSource_ColumnsMissingPercentage[column] = round(number_of_absent_rows_for_column / number_of_rows_in_dataset * 100, 4)

    # Check if output columns are found and save output column names to analyzed object
    if len(columns_with_missing_data_dict) > 0:
        output_column_detected_by_analyser = check_count_of_missing_rows_for_each_output(analyzed_object_from_file,
                                                                                         columns_with_missing_data_dict)
        for output_column in output_column_detected_by_analyser:
            if output_column not in analyzed_object_from_file.AnalysisSource_ColumnsNameOutput:
                analyzed_object_from_file.AnalysisSource_ColumnsNameOutput[output_column] = True
                analyzed_object_from_file.AnalysisSource_ColumnsNameInput[output_column] = False

    elif len(columns_with_missing_data_dict) == 0 and len(analyzed_object_from_file.AnalysisSource_ColumnsNameOutput) == 0:
        analyzed_object_from_file.add_error_info_for_column('DATASET', 'Columns to predict not found')

    # Write warning message for all columns if column have nan and column not to_predict
    if list_of_columns_with_missing_values:
        for column in list_of_columns_with_missing_values:
            analyzed_object_from_file.add_warning_info_for_column(column, 'Have missing data in some rows')

    # For each column save their data type
    for column in dataframe_from_file:
        if any(isinstance(try_literal_eval(value), list) for value in dataframe_from_file[column] if try_literal_eval(value) is list and try_literal_eval(value)[0] is list):
            dataframe_from_file[column] = dataframe_from_file[column].apply(list_of_values_to_tags)

        if column not in analyzed_object_from_file.AnalysisSource_ColumnsNameOutput:
            analyzed_object_from_file.AnalysisSource_ColumnsNameInput[column] = True
            analyzed_object_from_file.AnalysisSource_ColumnsNameOutput[column] = False

        columns_type[column] = determine_column_data_type(column, analyzed_object_from_file, dataframe_from_file)

    # Save dataset properties to object
    analyzed_object_from_file.AnalysisSource_ColumnsType.update(columns_type)
    analyzed_object_from_file.AnalysisSource_ColumnType_GroupCountDataType = CountGroupDictValues(DictToGroupCount=columns_type,
                                                                                                  ListOfGroups=all_possible_column_types)
    analyzed_object_from_file.dataset = dataframe_from_file

    return analyzed_object_from_file


if __name__ == '__main__':
    from CreateConnectionToDB import get_db_connection
    data_from_file = pd.read_excel("DataSets/test-2.xls")

    cn = get_db_connection(AI_CURSOR=True)




    A = analyse_source_data_find_input_output(data_from_file)
    print('-------------------INPUT COLUMNS----------------------')
    print(A.AnalysisSource_ColumnsNameInput)
    print('-------------------OUTPUT COLUMNS----------------------')
    print(A.AnalysisSource_ColumnsNameOutput)
    print('-------------------Missed values in columns------------')
    print(A.AnalysisSource_ColumnsMissingPercentage)
    print('-------------------COLUMN TYPES------------------------')
    print(A.AnalysisSource_ColumnsType)
    print('-------------------WARNINGS--------------------------')
    print(A.AnalysisSource_Warnings)
    print('-------------------ERRORS---------------------------')
    print(A.AnalysisSource_Errors)
    print(A.AnalysisSource_ColumnsListMaxSize)

    # cn.execute(f"INSERT INTO ai.brains (AnalysisSource_ColumnsNameInput, AnalysisSource_ColumnsNameOutput, "
    #            f"AnalysisSource_ColumnType_GroupCountDataType, AnalysisSource_ColumnsMissingPercentage, AnalysisSource_ColumnType,"
    #            f"AnalysisSource_ListsSize, AnalysisSource_Errors, AnalysisSource_Warnings, Brain_ModeRNN, Brain_ModeLSTM, "
    #            f"ParameterNN_ShapeAuto, ParameterNN_Loss, ParameterNN_Optimizer, ParameterNN_Shape, ParameterNN_BatchEpochAuto)"
    #            f"VALUES ('{json.dumps(A.column_names_input)}', '{json.dumps(A.column_names_output)}', '{json.dumps(A.count_group_dict_values)}',"
    #            f"'{json.dumps(A.percentage_of_missing_value_for_column)}', '{json.dumps(A.column_types)}', '{json.dumps(A.lists_size)}', "
    #            f"'{json.dumps(A.errors_info)}', '{json.dumps(A.warning_info)}', '0', '1', '0', 'mean_squared_error', "
    #            f"""'rmsprop', '[[200, "LSTM-tanh", 0, 0], [3, "Dense-linear", 0, 0]]', '1');""")