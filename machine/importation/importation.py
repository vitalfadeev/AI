#####################################################################################################################
# Store helper
#####################################################################################################################
from machine.datalistener import GetFileData
from machine.loader import django_loader
from django.db import connections


def import_from_file( machine, fname, delete_old=False ):
    model = machine.get_machine_data_input_lines_model()

    if delete_old:
        delete_old_records( machine )

    df = GetFileData( fname )

    django_loader.load_pandas_dataframe( df, model )

    set_IsForLearning( machine, model )
    set_IsForSolving( machine, model )
    set_IsWithMissingValues( machine, model )
    set_IsForEvaluation( machine, model, df )


def delete_old_records( machine ):
    model = machine.get_machine_data_input_lines_model()
    model.objects.all().delete()


def set_IsForLearning( machine, model ):
    # After all lines stored, it is possible to execute a sql command to update IsForLearning=1 for all lines with no values empty in all (columnsInput+columnsOutPut)
    # make SQL condition: LENGTH(Col1) > 0 AND Col1 IS NOT NULL ...
    table = model._meta.db_table

    cols_in      = machine.get_machine_data_input_columns()    # input columns
    cols_out     = machine.get_machine_data_output_columns()   # output columns

    conds = []
    for col in cols_in + cols_out:
        conds.append( "LENGTH(`{}`) > 0 AND `{}` IS NOT NULL".format(col, col) )
    cond = " AND ".join( conds )

    # execute sql
    with connections['MachineData'].cursor() as cursor:
        cursor.execute(f"""
            UPDATE `{table}` 
               SET IsForLearning = 1 
             WHERE {cond}
        """)


def set_IsForSolving( machine, model ):
    # After all lines stored, it is possible to execute a sql command to update IsForSolving=1 for all lines with all values in (columnsInput) and none or some values in columnsOutPut
    # make SQL condition: LENGTH(Col1) > 0 AND Col1 IS NOT NULL ...
    table = model._meta.db_table

    cols_in      = machine.get_machine_data_input_columns()    # input columns

    conds = []
    for col in cols_in:
        conds.append( "LENGTH(`{}`) > 0 AND `{}` IS NOT NULL".format(col, col) )
    cond = " AND ".join( conds )

    # execute sql
    with connections['MachineData'].cursor() as cursor:
        cursor.execute(f"""
            UPDATE `{table}` 
               SET IsForSolving = 1 
             WHERE {cond}
        """)


def set_IsWithMissingValues( machine, model ):
    # After all lines stored, it is possible to execute a sql command to update IsWithMissingValues=1 for all lines with some values missing in columnsInput
    table = model._meta.db_table

    cols_in      = machine.get_machine_data_input_columns()    # input columns

    conds = []
    for col in cols_in:
        conds.append( "( LENGTH(`{}`) = 0 OR `{}` IS NULL )".format(col, col) )
    cond = " AND ".join( conds )

    # execute sql
    with connections['MachineData'].cursor() as cursor:
        cursor.execute(f"""
            UPDATE `{table}` 
               SET IsWithMissingValues = 1 
             WHERE {cond}
        """)


def set_IsForEvaluation( machine, model, df ):
    # After all lines stored, it is possible to execute a sql command to update IsForEvluation=1  on 10% lines (Max 100 lines) where  IsForLearning=1
    table = model._meta.db_table

    rows_count = len(df.index)
    lastid = model.get_last_id()

    # get chunk id
    chunk_size = int(rows_count / 10)  # 10%
    if chunk_size > 100:
        chunk_size = 100

    chunk_id = lastid - chunk_size
    if chunk_id < 0:
        chunk_id = 0

    # execute sql
    with connections['MachineData'].cursor() as cursor:
        cursor.execute(f"""
            UPDATE `{table}` 
               SET IsForEvaluation = 1 
             WHERE IsForLearning = 1 
               AND LineInput_ID > {chunk_id}
        """)
