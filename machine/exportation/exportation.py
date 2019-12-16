from machine.datalistener import DataReadFromSql
from machine.exportation.formats import FORMAT_CSV, DMY


def ProcessRead( DatabaseName, TableName, ExportLinesAfterPrimaryKey=None, FormatOutput=FORMAT_CSV, SettingFormatDate=DMY, index_col="ID" ):
    """ Wrapper around main exporter function
        :param ExportLinesAfterPrimaryKey:
        :param FormatOutput:
        :param SettingFormatDate:
        :return:
    """
    from django.db import connections

    connection = connections[ DatabaseName ]

    # main function for read from DB & return to user as file
    DataArrayExported = DataReadFromSql( DatabaseName, TableName, ExportLinesAfterPrimaryKey, FormatOutput, connection=connection, index_col=index_col )

    return DataArrayExported
