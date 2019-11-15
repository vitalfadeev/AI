from sqlalchemy import create_engine
from machine.analysis import settings
import pandas
import json


def DataLinesInputStore(Brain_ID, DataArray, User_ID):
    """
    Function to store pandas data frame to DataBase
    by checking if user id belong to target brain id

    :param Brain_ID: int number
    :param DataArray: pandas DataFrame
    :param User_ID: int number
    :return: last inserted line id from sql
    """

    ColumnsNameInput = json.loads(brain_object['AnalysisSource_ColumnsNameInput'])
    ColumnsNameOutput = json.loads(brain_object['AnalysisSource_ColumnsNameOutput'])
    TableName = settings.TABLE_NAME.format(Brain_ID)

    columns_from_file = ColumnsNameInput + ColumnsNameOutput
    columns_from_database = list(DataArray.columns)
    SameColumns = GetSameColumns(columns_from_file, columns_from_database)

    if SameColumns:
        # reduce data size: keep only required columns
        DataArrayToWrite = DataArray[SameColumns]

        # main function for store data to DB
        last_inserted_line_id = DataStoreInSql(TableName=TableName,
                                               DataArrayToWrite=DataArrayToWrite)

        # post insert service script
        UpdateInfoAboutInsertedRow(last_inserted_line_id - DataArray.shape[0],
                                   ColumnsNameInput,
                                   ColumnsNameOutput,
                                   Brain_ID)

        return last_inserted_line_id

    else:
        # warning if no same columns
        return Exception("No same columns")


def GetSameColumns(db_cols, file_cols):
    """
    Return names from first list if matched in second list
    :param db_cols:     [""]
    :param file_cols:   [""]
    :return:            [""] Same columns. ex: [a b c] & [a b d] = [a b]
    """
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
    BRAINDATA_cursor = get_db_connection()

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
    TableName = settings.TABLE_NAME.format(brainid)  # DB table name

    # get DB connection
    BRAINDATA_cursor = get_db_connection()

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


def get_db_connection():
    """ Return DB connection for insert data to SQLite/MySQL. default: sqlite
        :return: SqlAlchemy connection object
        See also: settings.DB_CONNECTION_STRING
    """

    # connect
    engine = create_engine(settings.DB_CONNECTION_STRING)
    connection = engine.connect()

    # setup UTF-8 support
    setup_utf8_support(connection)

    return connection


def setup_utf8_support(dbc):
    """ Setup UTF-8 support
    :param dbc DBConnection
    """
    # dbc.set_character_set('utf8')
    dbc.execute('SET NAMES utf8;')
    dbc.execute('SET CHARACTER SET utf8;')
    dbc.execute('SET character_set_connection=utf8;')


if __name__ == '__main__':
    dataset = pandas.read_csv('1.csv').head(5)
    print(DataLinesInputStore(1, dataset, 2))
