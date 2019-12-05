from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from machine.datainput import datatable
from machine.models import Machine


class MachineAdmin(admin.ModelAdmin):
    list_display = ['Project_Name', 'DateTimeCreation', 'Project_Description', 'AnalysisSource_ColumnsNameInput', 'MachineInputLines']

    def MachineInputLines( self, request ):
        machine = Machine.objects.get( Machine_ID=request.pk )
        return mark_safe( f"<a href='/admin/Machine/{machine.Machine_ID}/DataInputLines'>Machine_{machine.Machine_ID}_DataInputLines</a>" )

    MachineInputLines.short_description = 'MachineInputLines'



# Register your models here.
admin.site.register(Machine, MachineAdmin)


@login_required
def AdminDataInputLines( request, Machine_ID ):
    machine = get_object_or_404( Machine, pk=Machine_ID )
    context = { }
    model = machine.get_machine_data_input_lines_model()
    columns = machine.get_machine_data_input_lines_columns( include_predefined=True )
    context.update( locals() )
    return render( request, 'admin/AdminDataInputLines.html', context )


@method_decorator(login_required, name='dispatch')
class MachineDatatableAjax(datatable.DTView):
    """ Return Input data. Using with jquery.datatables """
    def get(self, request, Machine_ID):
        # Query from table BATCH_INPUT_NNN
        # without pk 'index'
        # return JSON
        machine = get_object_or_404( Machine, pk=Machine_ID )

        self.model = machine.get_machine_data_input_lines_model()
        self.columns = machine.get_machine_data_input_lines_columns( include_predefined=True )
        self.order_columns = self.columns
        return super().get(request)
