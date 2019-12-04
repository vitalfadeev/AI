#####################################################################################################################
# Store helper
#####################################################################################################################
from machine.datalistener import GetFileData, DataStoreInSql


def GetSameColumns(db_cols, file_cols):
    """ Return names from first list if matched in second list
        :param db_cols:     [""]
        :param file_cols:   [""]
        :return:            [""] Same columns. ex: [a b c] & [a b d] = [a b]
    """
    common = set(db_cols) & set(file_cols)
    return list(common)


def ProcessFile(ffname, SettingFormatDate=DMY):
    """ Read uploaded file, parse, insert into DB. Ir wrapper around main importer function.
        :param ffname:
        :return:
    """
    # read file (csv, xls, json, xml). into pandas.DataFrame
    df = GetFileData(ffname)

    # get column names common.
    # 1. get table columns
    # 2. get file columns
    # 3. find same
    dbcols = settings.ColumnsNameInput + settings.ColumnsNameOutput
    dfcols = list(df.columns)
    SameColumns = GetSameColumns(dbcols, dfcols)

    if SameColumns:
        # reduce data size: keep only required columns
        DataArrayToWrite = df[SameColumns]

        # insert into DB
        DatabaseName     = settings.BrainID
        TableName        = settings.TABLENAME
        ColumNames       = SameColumns

        # main function for store data to DB
        lastid = DataStoreInSql(DatabaseName, TableName, ColumNames, DataArrayToWrite, SettingFormatDate=DMY)

        # post insert service script
        PostInsert(df.shape[0], lastid)

        return lastid

    else:
        # warning if no same columns
        warning = "Not all columns inserted. Expected: {}, Inserted: {}".format(dbcols, SameColumns)
        abort(500, warning)


def PostInsert(rows_count, lastid):
    """ Post Insert service script.
        Update predefined columns: 'IsForLearning' and other
        :param rows_count int  Row in data packet
        :param lastid     int  Last inserted ID
    """
    DatabaseName = settings.BrainID             # DB name
    TableName    = settings.TABLENAME           # DB table name
    cols_in      = settings.ColumnsNameInput    # input columns
    cols_out     = settings.ColumnsNameOutput   # output columns

    # get DB connection
    dbc = get_db_connection(DatabaseName)

    # After all lines stored, it is possible to execute a sql command to update IsForLearning=1 for all lines with no values empty in all (columnsInput+columnsOutPut)
    # make SQL condition: LENGTH(Col1) > 0 AND Col1 IS NOT NULL ...
    conds = []
    for col in cols_in + cols_out:
        conds.append( "LENGTH(`{}`) > 0 AND `{}` IS NOT NULL".format(col, col) )
    cond = " AND ".join( conds )

    # execute sql
    dbc.execute("""
        UPDATE `{}` 
           SET IsForLearning = 1 
         WHERE {}"""
        .format(
            TableName,
            cond
        )
    )

    # After all lines stored, it is possible to execute a sql command to update IsForSolving=1 for all lines with all values in (columnsInput) and none or some values in columnsOutPut
    # make SQL condition: LENGTH(Col1) > 0 AND Col1 IS NOT NULL ...
    conds = []
    for col in cols_in:
        conds.append( "LENGTH(`{}`) > 0 AND `{}` IS NOT NULL".format(col, col) )
    cond = " AND ".join( conds )

    # execute sql
    dbc.execute("""
        UPDATE `{}` 
           SET IsForSolving = 1 
         WHERE {}"""
        .format(
            TableName,
            cond
        )
    )

    # After all lines stored, it is possible to execute a sql command to update IsWithMissingValues=1 for all lines with some values missing in columnsInput
    conds = []
    for col in cols_in:
        conds.append( "( LENGTH(`{}`) = 0 OR `{}` IS NULL )".format(col, col) )
    cond = " AND ".join( conds )

    # execute sql
    dbc.execute("""
        UPDATE `{}` 
           SET IsWithMissingValues = 1 
         WHERE {}"""
        .format(
            TableName,
            cond
        )
    )


    # After all lines stored, it is possible to execute a sql command to update IsForEvluation=1  on 10% lines (Max 100 lines) where  IsForLearning=1
    conds = []
    # get chunk id
    chunk_size = int(rows_count / 10)  # 10%
    if chunk_size > 100:
        chunk_size = 100

    chunk_id = lastid - chunk_size
    if chunk_id < 0:
        chunk_id = 0

    # execute sql
    dbc.execute("""
        UPDATE `{}` 
           SET IsForEvaluation = 1 
         WHERE IsForLearning = 1 AND ID > {}"""
        .format(
            TableName,
            chunk_id
        )
    )


