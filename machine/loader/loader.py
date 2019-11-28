import os
import importlib


def load( url:str, table:str, columns:list, types:dict, connection ):
    #loader = get_loader( url )
    #loader.load( url, table, columns, types, connection )
    import machine.loader.csv
    machine.loader.csv.load( url, table, columns, types, connection )


def get_loader( url ):
    filename, file_extension = os.path.splitext( url )

    module_name = file_extension.lower().strip().lstrip('.').lstrip()
    module_file = f"{module_name}.py"
    self_dir = os.path.dirname(__file__)

    if module_file in os.listdir( self_dir ):
        package = 'machine.loader'
        module_name = module_name
        module = importlib.import_module( f"{package}.{module_name}" )

    else:
        raise Exception(f"No loader for: {file_extension}")


