def create_model_table( model ):
    # 1. Create model
    #    - class
    #    - fields
    # 2. Create DB table
    # 3. Load data
    from django.db import connections

    with connections['MachineData'].schema_editor() as schema_editor:
        schema_editor.create_model( model )


def crete_input_table( machine ):
    # Get Output data Dynamic model
    MachineDataInputLines = machine.get_machine_data_input_lines_model()

    # Create Input data table
    create_model_table( MachineDataInputLines )


def crete_output_table( machine ):
    # Get Output data Dynamic model
    MachineDataOutputLines = machine.get_machine_data_output_lines_model()

    # Create Output data table
    create_model_table( MachineDataOutputLines )


def create_data_tables( machine ):
    crete_input_table( machine )
    crete_output_table( machine )

