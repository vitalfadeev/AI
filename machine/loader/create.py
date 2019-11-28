from django.db import models
from django_extensions.db.fields.json import JSONField

def create_model_table( model ):
    # 1. Create model
    #    - class
    #    - fields
    # 2. Create DB table
    # 3. Load data
    from django.db import connections

    with connections['MachineData'].schema_editor() as schema_editor:
        schema_editor.create_model( model )
