import io
import os
from collections import defaultdict
from django.apps import apps
from rest_framework.exceptions import ValidationError
from machine.analyzer.DataPreAnalyser import analyse_source_data_find_input_output
from machine.loader.create import  create_data_tables


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
    machine.AnalysisSource_ColumnsNameInput = A.AnalysisSource_ColumnsNameInput
    machine.AnalysisSource_ColumnsNameOutput = A.AnalysisSource_ColumnsNameOutput
    machine.AnalysisSource_ColumnType = A.AnalysisSource_ColumnsType
    machine.AnalysisSource_Errors = A.AnalysisSource_Errors
    machine.AnalysisSource_Warnings = A.AnalysisSource_Warnings
    machine.AnalysisSource_ColumnsMissingPercentage = A.AnalysisSource_ColumnsMissingPercentage
    machine.AnalysisSource_ListMaxSize = A.AnalysisSource_ColumnsListMaxSize

    machine._dataframe = dataframe


def load( machine ):
    # Create Input and Output tables
    create_data_tables( machine )

    # Load data
    from machine.importation import importation
    importation.import_from_file( machine, machine.input_file.path, delete_old=False )

