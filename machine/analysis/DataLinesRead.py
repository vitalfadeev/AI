from machine.analysis.CreateConnectionToDB import get_db_connection
from machine.analysis import DatabaseConnectionSettings
import pandas
import json


def GetBrainObjectByBrainID(Brain_ID):
    # Get brain object
    AI_cursor = get_db_connection(AI_CURSOR=True)
    column_properties_from_db = ['AnalysisSource_ColumnsNameInput', 'AnalysisSource_ColumnsNameOutput']
    properties_to_get_from_braindata = ', '.join(column_properties_from_db)
    sql = f"""SELECT {properties_to_get_from_braindata}
              FROM brains b
              WHERE b.Brain_ID = {Brain_ID};"""
    brain_object = AI_cursor.execute(sql)
    return [{column: value for column, value in rowproxy.items()} for rowproxy in brain_object][0]


def DataLinesInputRead(Brain_ID, **kwargs):

    """

    :param Brain_ID: int number
    :param kwargs: dict of other properties from db with their values to add in WHERE clause
                   Example: {'IsForLearning': 1,
                             'IsWithMissingValues': 0,
                             'DataLineToProcess_LastLineID': 500,
                             'DataLineToProcess_FirstLineID': 300}
           !!!NOTE!!! All properties from kwargs are added in WHERE clause with AND statement
           So make sure you add correct properties:
           If {'IsForLearning': 1, 'IsForSolving': 1} are both in one request, you get nothing.
    :return:
    """

    brain_object = GetBrainObjectByBrainID(Brain_ID=Brain_ID)

    ColumnsNameInput = json.loads(brain_object['AnalysisSource_ColumnsNameInput'])
    ColumnsNameOutput = json.loads(brain_object['AnalysisSource_ColumnsNameOutput'])
    TableName = DatabaseConnectionSettings.TABLE_DataInputLines_NAME.format(Brain_ID)

    return DataLinesReadFromTable(TableName=TableName,
                                  properties_to_read=ColumnsNameInput+ColumnsNameOutput,
                                  **kwargs)


def DataLinesOutputRead(Brain_ID, **kwargs):
    """

    :param Brain_ID: int number
    :param kwargs:
    :return:
    """

    brain_object = GetBrainObjectByBrainID(Brain_ID=Brain_ID)

    ColumnsNameOutput = json.loads(brain_object['AnalysisSource_ColumnsNameOutput'])
    TableName = DatabaseConnectionSettings.TABLE_DataOutputLines_NAME.format(Brain_ID)

    return DataLinesReadFromTable(TableName=TableName,
                                  properties_to_read=ColumnsNameOutput,
                                  **kwargs)


def DataLinesReadFromTable(TableName, properties_to_read, **kwargs):

    # Create cursor for brain data DB
    BRAINDATA_cursor = get_db_connection(BRAINDATA_CURSOR=True)

    # Create sql for getting content
    # from database with flags
    to_select_sql = ', '.join(properties_to_read)
    sql = f"SELECT {to_select_sql} FROM {TableName} "

    if kwargs:
        where_clause = []
        for column, value in kwargs.items():
            if column == 'DataLineToProcess_FirstLineID':
                where_clause.append(f'LineInput_ID>={value}')
            elif column == 'DataLineToProcess_LastLineID':
                where_clause.append(f'LineInput_ID<={value}')
            else:
                where_clause.append(f'{column}={value}')

        sql += 'WHERE ' + ' AND '.join(where_clause)

    try:
        data_frame_from_DB = pandas.read_sql(sql, BRAINDATA_cursor)
    except Exception as error:
        return error

    return data_frame_from_DB


if __name__ == '__main__':

    print(DataLinesInputRead(Brain_ID=2,
                             IsForSolving=1,
                             DataLineToProcess_LastLineID=700,
                             DataLineToProcess_FirstLineID=400
                             ))

    print(DataLinesOutputRead(Brain_ID=2,
                              DataLineToProcess_LastLineID=700,
                              DataLineToProcess_FirstLineID=400
                              ))
