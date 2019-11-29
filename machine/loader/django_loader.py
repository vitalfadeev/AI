import io
import os
from collections import defaultdict
from django.apps import apps


# export
# df = pd.DataFrame(list(BlogPost.objects.all().values()))

# export
# from django_pandas.io import read_frame
# qs = model.objects.all()
# df = read_frame( qs )
# from django.core.exceptions import ValidationError
from pandas.tests.io.json.test_ujson import orient
from rest_framework.exceptions import ValidationError

from machine.analyzer.DataPreAnalyser import analyse_source_data_find_input_output
from machine.loader.create import create_model_table


class BulkCreateManager(object):
    """
    This helper class keeps track of ORM objects to be created for multiple
    model classes, and automatically creates those objects with `bulk_create`
    when the number of objects accumulated for a given model class exceeds
    `chunk_size`.
    Upon completion of the loop that's `add()`ing objects, the developer must
    call `done()` to ensure the final set of objects is created for all models.
    """

    def __init__(self, chunk_size=100):
        self._create_queues = defaultdict(list)
        self.chunk_size = chunk_size

    def _commit(self, model_class):
        model_key = model_class._meta.label
        model_class.objects.bulk_create(self._create_queues[model_key])
        self._create_queues[model_key] = []

    def add(self, obj):
        """
        Add an object to the queue to be created, and call bulk_create if we
        have enough objs.
        """
        model_class = type(obj)
        model_key = model_class._meta.label
        self._create_queues[model_key].append(obj)
        if len(self._create_queues[model_key]) >= self.chunk_size:
            self._commit(model_class)

    def done(self):
        """
        Always call this upon completion to make sure the final partial chunk
        is saved.
        """
        for model_name, objs in self._create_queues.items():
            if len(objs) > 0:
                self._commit(apps.get_model(model_name))


def load_csv_to_model( url, model, columns, types ):
    # table = model_instance._meta.db_table
    # loader.load( url, table, columns, types, connection )

    # import
    import pandas as pd
    df = pd.read_csv()
    entries = df.to_dict( 'records' )
    model.objects.bulk_create( entries )


def load_pandas_dataframe( dataframe, model ):
    fields = model._meta.get_fields()

    instances = [
        model( **row ) for row in dataframe.to_dict( orient="records" )
    ]

    model.objects.bulk_create( instances )


def load_to_dataframe( url: str, file_handle: io.FileIO = None ):
    import pandas as pd

    # Get extension
    filename, file_extension = os.path.splitext( url )
    ext_lower = file_extension.lower().strip()

    # Data source: url or file_handle
    src = file_handle if file_handle is not None else url

    # Read
    if ext_lower == ".xls":
        dataframe = pd.read_excel( src )

    elif ext_lower == ".xlsx":
        dataframe = pd.read_excel( src )

    elif ext_lower == ".csv":
        dataframe = pd.read_csv( src )

    else:
        raise ValidationError( f".xls, .xlsx, .csv only! Unsupported extensoin: {ext_lower}: (in file '{filename}')" )

    return dataframe


def prenanlyze( machine, url, file_handle ):
    # Load file. Get pandas DataFrame
    dataframe = load_to_dataframe( url, file_handle )

    # Processing the data:
    A = analyse_source_data_find_input_output( dataframe )

    # Validation
    # if A.errors_info:
    #     # discard file
    #     raise ValidationError( f"errors: '{url}': {A.errors_info}")

    # Save analyzer result
    machine.AnalysisSource_ColumnsNameInput = A.column_names_input
    machine.AnalysisSource_ColumnsNameOutput = A.column_names_output
    machine.AnalysisSource_ColumnType = A.column_types
    machine.AnalysisSource_Errors = A.errors_info
    machine.AnalysisSource_Warnings = A.warning_info
    machine.AnalysisSource_ColumnsMissingPercentage = A.percentage_of_missing_value_for_column
    machine.AnalysisSource_ListMaxSize = A.lists_size

    machine._dataframe = dataframe


def load( url, machine ):
    # Input data Dynamic model
    MachineDataInputLines = machine.get_machine_data_input_lines_model()

    # Create Input data tabe
    create_model_table( MachineDataInputLines )

    # Load data
    if hasattr(machine, "_dataframe"):
        # get dataset from pre-analyzer
        load_pandas_dataframe( machine._dataframe, MachineDataInputLines )
    else:
        # load dataset from file
        dataframe = load_to_dataframe( url, file_handle=None )

    # # Create Columns
    # machine_input = []
    # machine_output = []
    # machine_ignore = []
    #
    # for col in dataframe:
    #     if col in pre_analysis.column_names_input:
    #         machine.analysis_source_columns.create(
    #                                         column_type="IN",
    #                                         name=col, desc=" "
    #                                     )
    #         machine_input.append(col.replace('_',' '))
    #     elif col in pre_analysis.column_names_output:
    #         machine.analysis_source_columns.create(
    #                                         column_type="OUT",
    #                                         name=col, desc=" "
    #                                     )
    #         machine_output.append(col.replace('_',' '))
    #
    #     else:
    #         machine.analysis_source_columns.create(
    #                                         column_type="IGN",
    #                                         name=col, desc=" "
    #                                     )
    #         machine_ignore.append(col.replace('_',' '))
    #
    # machine.analysissource_columnnameinput = machine_input
    # machine.analysissource_columnnameoutput = machine_output
    # machine.analysissource_columnnameignore = machine_ignore
    #
