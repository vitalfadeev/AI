import csv

def _detect_format( url:str ) -> csv.Dialect:
    with open( url ) as csvfile:
        dialect = csv.Sniffer().sniff( csvfile.read( 1024 ) )
        csvfile.seek( 0 )
        # reader = csv.reader( csvfile, dialect )
        return dialect


def _load_data_fast( url: str, dialect: csv.Dialect, table: str, connection, charset_name="UTF-8" ):
    sql = f"""
    LOAD DATA 
        INFILE `{url}`
        INTO TABLE `{table}`
        CHARACTER SET '{charset_name}'
    """

    # if dialect.escapechar:
    #
    # """
    #     FIELDS
    #         TERMINATED BY '{dialect.delimiter}'
    #         ENCLOSED BY '{dialect.doublequote}'
    #         ESCAPED BY '{escapechar}'
    #     LINES
    #         STARTING BY '{dialect.delimiter}'
    #         TERMINATED BY '{dialect.lineterminator}'
    # """

    print (sql)

    with connection.cursor() as cursor:
        cursor.execute( sql )


def _load_data( url: str, dialect: csv.Dialect, table: str, connection, charset_name = "UTF-8" ):
    pass


def load( url: str, table: str, columns:list, types: dict, connection ):
    # 1. detect format
    # 2. create table
    # 3. load data

    # 1. detect format
    dialect = _detect_format( url )

    # 2. create table
    _create_table( table, columns, types, connection )

    # 3. load data
    _load_data( url, dialect, table, columns, types, connection )

