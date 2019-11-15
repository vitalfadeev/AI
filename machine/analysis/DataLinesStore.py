from machine.analysis.CreateConnectionToDB import get_db_connection
from machine.analysis import DatabaseConnectionSettings
import pandas
import json


def GetBrainObjectByBrainID(Brain_ID):
    # Get brain object
    AI_cursor = get_db_connection(AI_CURSOR=True)
    column_properties_from_db = ['AnalysisSource_ColumnsNameInput', 'AnalysisSource_ColumnsNameOutput',
                                 'Data_ColumnsInputFilterLines']
    properties_to_get_from_braindata = ', '.join(column_properties_from_db)
    sql = f"""SELECT {properties_to_get_from_braindata}
              FROM brains b
              WHERE b.ID = {Brain_ID};"""
    brain_object = AI_cursor.execute(sql)
    return [{column: value for column, value in rowproxy.items()} for rowproxy in brain_object][0]


def DataLinesInputStore(Brain_ID, DataArray):
    """
    Function to store pandas data frame to DataBase
    by checking if user id belong to target brain id

    :param Brain_ID: int number
    :param DataArray: pandas DataFrame
    :return: last inserted line id from sql
    """

    brain_object = GetBrainObjectByBrainID(Brain_ID=Brain_ID)

    ColumnsNameInput = json.loads(brain_object['AnalysisSource_ColumnsNameInput'])
    ColumnsNameOutput = json.loads(brain_object['AnalysisSource_ColumnsNameOutput'])
    try:
        ColumnsInputFilterLines = json.loads(brain_object['Data_ColumnsInputFilterLines'])
    except:
        ColumnsInputFilterLines = None

    columns_from_file = list(DataArray.columns)

    TableName = DatabaseConnectionSettings.TABLE_DataInputLines_NAME.format(Brain_ID)
    try:
        columns_from_database = ColumnsNameInput + ColumnsNameOutput
    except TypeError :
        columns_from_database = ColumnsNameInput.update(ColumnsNameOutput) 

    SameColumns = GetSameColumns(columns_from_file, columns_from_database)

    if SameColumns:
        last_inserted_line_id = DataLinesStoreInTable(TableName=TableName,
                                                      DataArray=DataArray,
                                                      ColumnsToStore=SameColumns,
                                                      ColumnsInputFilterLines=ColumnsInputFilterLines)

        # post insert service script
        UpdateInfoAboutInsertedRow(last_inserted_line_id - DataArray.shape[0],
                                   ColumnsNameInput,
                                   ColumnsNameOutput,
                                   Brain_ID)

        return last_inserted_line_id
    else:
        # warning if no same columns
        return Exception("No same columns")


def DataLinesOutputStore(Brain_ID, DataArray):
    """
    Function to store pandas data frame to DataBase
    by checking if user id belong to target brain id

    :param Brain_ID: int number
    :param DataArray: pandas DataFrame
    :return: last inserted line id from sql
    """
    brain_object = GetBrainObjectByBrainID(Brain_ID=Brain_ID)

    ColumnsNameOutput = json.loads(brain_object['AnalysisSource_ColumnsNameOutput'])
    try:
        ColumnsInputFilterLines = json.loads(brain_object['Data_ColumnsInputFilterLines'])
    except:
        ColumnsInputFilterLines = None

    columns_from_file = list(DataArray.columns)

    TableName = DatabaseConnectionSettings.TABLE_DataOutputLines_NAME.format(Brain_ID)
    SameColumns = GetSameColumns(ColumnsNameOutput, columns_from_file)

    if SameColumns:
        # reduce data size: keep only required columns
    
        SameColumns += ['LineInput_ID']
        return DataLinesStoreInTable(TableName=TableName,
                                     DataArray=DataArray,
                                     ColumnsToStore=SameColumns,
                                     ColumnsInputFilterLines=ColumnsInputFilterLines)

    else:
        # warning if no same columns
        return Exception("No same columns")


def DataLinesStoreInTable(TableName, DataArray, ColumnsToStore, ColumnsInputFilterLines):

    # reduce data size: keep only required columns
    DataArrayToWrite = DataArray[ColumnsToStore]

    if ColumnsInputFilterLines:
        for column_name, value in ColumnsInputFilterLines.items():
            DataArrayToWrite = DataArrayToWrite[DataArrayToWrite[column_name] != value]

    # main function for store data to DB
    last_inserted_line_id = DataStoreInSql(TableName=TableName,
                                           DataArrayToWrite=DataArrayToWrite)

    return last_inserted_line_id


def GetSameColumns(db_cols, file_cols):
    """
    Return names from first list if matched in second list
    :param db_cols:     [""]
    :param file_cols:   [""]
    :return:            [""] Same columns. ex: [a b c] & [a b d] = [a b]
    """
    if db_cols and file_cols:
        common = set(db_cols) & set(file_cols)
        return list(common)


def DataStoreInSql(TableName, DataArrayToWrite):
    """
    Insert data into DB
    :param TableName:        ""
    :param DataArrayToWrite: [[],[]]
    :return:
    """
    # get connection
    BRAINDATA_cursor = get_db_connection(BRAINDATA_CURSOR=True)
    # insert into DB. if table not exists - create, if exists - append
    DataArrayToWrite.to_sql(TableName,
                            BRAINDATA_cursor,
                            if_exists='append',
                            method='multi',
                            index_label='LineInput_ID',
                            index=False)

    # Get last inserted line ID
    result = BRAINDATA_cursor.execute("SELECT max(`LineInput_ID`) FROM {};".format(TableName))
    row = result.fetchone()
    LastLineIDWritten = row[0]

    # close
    BRAINDATA_cursor.close()

    return LastLineIDWritten


def UpdateInfoAboutInsertedRow(first_inserted_id, cols_in, cols_out, brainid):
    """ Post Insert service script.
        Update predefined columns: 'IsForLearning' and other
        :param brainid:
        :param cols_out:
        :param cols_in:
        :param first_inserted_id int  Row in data packet
    """
    TableName = DatabaseConnectionSettings.TABLE_DataInputLines_NAME.format(brainid)  # DB table name

    # get DB connection
    BRAINDATA_cursor = get_db_connection(BRAINDATA_CURSOR=True)

    # Fill IsForLearning column
    sql_all_lines_not_null = [f'`{column}` IS NOT NULL' for column in cols_in + cols_out]
    is_for_learning_sql = f'UPDATE {TableName} ' \
                          f'SET IsForLearning=1 ' \
                          f'WHERE LineInput_ID > {first_inserted_id} AND ' + \
                          ' AND '.join(sql_all_lines_not_null)
    BRAINDATA_cursor.execute(is_for_learning_sql)

    # Fill IsForSolving column
    sql_input_not_null = [f'`{column}` IS NOT NULL' for column in cols_in]
    sql_output_null = [f'`{column}` IS NULL' for column in cols_out]
    is_for_solving_sql = f'UPDATE {TableName} ' \
                         f'SET IsForSolving = 1 ' \
                         f'WHERE LineInput_ID > {first_inserted_id} AND ' + \
                         ' AND '.join(sql_input_not_null) + \
                         ' AND (' + ' OR '.join(sql_output_null) + ');'
    BRAINDATA_cursor.execute(is_for_solving_sql)

    # Fill IsWithMissingValues column
    sql_input_null = [f'`{column}` IS NULL' for column in cols_in]
    is_missing_sql = f'UPDATE `{TableName}` ' \
                     f'SET IsWithMissingValues=1 ' \
                     f'WHERE LineInput_ID > {first_inserted_id} AND (' + ' OR '.join(sql_input_null) + ');'
    BRAINDATA_cursor.execute(is_missing_sql)

    # Fill IsForEvaluation column
    is_for_evaluation_sql = f'UPDATE {TableName} ' \
        f'SET IsForEvaluation=1 ' \
        f'WHERE LineInput_ID > {first_inserted_id} ' \
        f'AND RAND() < 0.25 ' \
        f'AND IsForLearning=1'
    BRAINDATA_cursor.execute(is_for_evaluation_sql)


if __name__ == '__main__':
    dataset = pandas.read_csv('1.csv').head(20)
    print(DataLinesInputStore(Brain_ID=1,
                              DataArray=dataset))
