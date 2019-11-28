import json

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.decorators import method_decorator
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from machine.datainput import datatable
from machine.loader.create import create_model_table
from machine.models import Machine
from team.models import Team
from machine.forms import MachineAddForm, MachineDescribeForm, MachineMainForm, MachineNNParametersForm, \
    MachineNNShapeForm
from machine.decorators import user_can_view_machine, user_can_edit_machine

from machine.analysis.DataPreAnalyser import analyse_source_data_find_input_output

# from machine.analysis.DataLinesInputStore import DataLinesInputStore
from rest_framework import viewsets, parsers
from machine.serializers import MachineSerializer

from machine.models import MachineMessage

from django.db import connection

from rest_framework import generics, viewsets
from rest_framework import mixins



##############################################################################3
# Machine
##############################################################################3
@login_required
def MachineAdd( request ):
    context = {}

    if request.POST:
        form = MachineAddForm( request.POST, request.FILES )
        if form.is_valid():
            entry = form.save(commit=False)
            entry.Owner_User_ID = request.user
            entry.save()
            return HttpResponseRedirect(f"/Machine/{entry.pk}/Describe")
        else:
            context.update( locals() )
            return render(request, 'machine/MachineAdd.html', context)
    else:
        form = MachineAddForm()
        context.update(locals())
        return render(request, 'machine/MachineAdd.html', context)


@login_required
def MachineDescribe( request, Machine_ID ):
    context = {}
    machine = get_object_or_404( Machine, pk=Machine_ID )
    columns = machine.AnalysisSource_ColumnType.keys()

    if request.POST:
        form = MachineDescribeForm( request.POST, instance=machine )
        if form.is_valid():
            entry = form.save(commit=False)
            entry.save()
            return HttpResponseRedirect(f"/Machine/{entry.pk}/NN/Parameters")
        else:
            context.update( locals() )
            return render(request, 'machine/MachineDescribe.html', context)
    else:
        form = MachineDescribeForm( instance=machine )
        context.update(locals())
        return render(request, 'machine/MachineDescribe.html', context)


@login_required
def MachineMain( request, Machine_ID ):
    context = {}
    machine = get_object_or_404( Machine, pk=Machine_ID )

    if request.POST:
        form = MachineMainForm( request.POST, instance=machine )

        if form.is_valid():
            entry = form.save(commit=False)
            entry.save()
            return HttpResponseRedirect(f"/Machine/{entry.pk}/Main")
        else:
            context.update( locals() )
            return render(request, 'machine/MachineMain.html', context)
    else:
        form = MachineMainForm( instance=machine )
        context.update( locals() )
        return render(request, 'machine/MachineMain.html', context)


@method_decorator(login_required, name='dispatch')
class MachineDatatableAjax(datatable.DTView):
    """ Return Input data. Using with jquery.datatables """
    def get(self, request, Machine_ID):
        # Query from table BATCH_INPUT_NNN
        # without pk 'index'
        # return JSON
        machine = get_object_or_404( Machine, pk=Machine_ID )

        self.model = machine.get_machine_data_input_lines_model()
        self.columns = self.model.get_field_names(without_pk=True)
        self.order_columns = self.columns
        return super().get(request)


def Machines(request):
    machines = Machine.objects.filter(Owner_User_ID=request.user).order_by('-DateTimeCreation')
    context = {}
    context.update( locals() )
    return render(request, 'machine/Machines.html', context)


@method_decorator(login_required, name='dispatch')
class MachinesDatatableAjax(datatable.DTView):
    model = Machine
    columns = [
        'Machine_ID',
        'DateTimeCreation',
        'Owner_Team_ID',
        'Project_Name',
        'Project_Description',
        'AnalysisSource_ColumnsNameInput',
        'AnalysisSource_ColumnsNameOutput',
    ]
    order_columns = ['Machine_ID', 'DateTimeCreation', 'Project_Name']

    def get(self, request):
        self.request = request
        return super().get(request)


    def filter_queryset(self, qs):
        from django.db.models import Q

        # my only
        qs = qs.filter(Owner_User_ID=self.request.user)

        # search
        sSearch = self.request.GET.get('sSearch', None)

        if sSearch:
            qs = qs.filter(
                Q(Project_Name__istartswith=sSearch) |
                Q(Project_Description__istartswith=sSearch)
            )

        # last at top
        qs = qs.order_by('-DateTimeCreation')

        return qs


##############################################################################3
# NN
##############################################################################3
@login_required
def MachineNNMain( request, Machine_ID ):
    context = {}
    machine = get_object_or_404( Machine, pk=Machine_ID )

    if request.POST:
        form = MachineMainForm( request.POST, instance=machine )

        if form.is_valid():
            entry = form.save(commit=False)
            entry.save()
            return HttpResponseRedirect(f"/Machine/{entry.pk}/NN/Main")
        else:
            context.update( locals() )
            return render(request, 'machine/MachineNNMain.html', context)
    else:
        form = MachineMainForm( instance=machine )
        context.update( locals() )
        return render(request, 'machine/MachineNNMain.html', context)


@login_required
def MachineNNParameters( request, Machine_ID ):
    context = {}
    machine = get_object_or_404( Machine, pk=Machine_ID )

    if request.POST:
        form = MachineNNParametersForm( request.POST, instance=machine )

        if form.is_valid():
            entry = form.save(commit=False)
            entry.save()
            return HttpResponseRedirect(f"/Machine/{entry.pk}/NN/Shape")
        else:
            context.update( locals() )
            return render(request, 'machine/MachineNNParameters.html', context)
    else:
        form = MachineNNParametersForm( instance=machine )
        context.update( locals() )
        return render(request, 'machine/MachineNNParameters.html', context)



@login_required
def MachineNNShape( request, Machine_ID ):
    context = {}
    machine = get_object_or_404( Machine, pk=Machine_ID )
    shapes = json.loads(machine.ParameterCNN_Shape)

    if request.POST:
        form = MachineNNShapeForm( request.POST, instance=machine )

        if form.is_valid():
            entry = form.save(commit=False)
            entry.save()
            return HttpResponseRedirect(f"/Machine/{entry.pk}/NN/Shape")
        else:
            context.update( locals() )
            return render(request, 'machine/MachineNNShape.html', context)
    else:
        form = MachineNNShapeForm( instance=machine )
        context.update( locals() )
        return render(request, 'machine/MachineNNShape.html', context)








# # Create your views here.
# def machine_public_list(request):
#     current_page = "public"
#     current_subpage = "public"
#     machines = Machine.objects.filter(is_public=True).order_by('-created_date')
#     return render(request, 'machine/public_list.html',
#                         {"current_page": current_page, "machines": machines, "current_subpage": current_subpage})
#
#
# def machine_private_list(request):
#     current_page = "private"
#     current_subpage = "private"
#     machines = Machine.objects.filter(Owner_User_ID=request.user).order_by('-DateTimeCreation')
#     return render(request, 'machine/private_list.html', {
#         "current_page": current_page,
#         "machines": machines,
#         "current_subpage": current_subpage,
#     })
#
#
# @login_required
# def machine_add_step1(request):
#     context = {}
#     current_page = "private"
#     current_subpage = "add"
#
#     if request.POST:
#         form = MachineForm(request.POST, request.FILES)
#         form.fields['Owner_Team_ID'].queryset = Team.objects.filter(members=request.user)
#         context.update(locals())
#         if form.is_valid():
#             entry = form.save()
#             entry.created_by = request.user
#             entry.save()
#             return HttpResponseRedirect('/machine/add/%s/' % entry.id)
#         else:
#             return render(request, 'machine/add_step1.html', context)
#     else:
#         form = MachineForm()
#         form.fields['Owner_Team_ID'].queryset = Team.objects.filter(members=request.user)
#         context.update(locals())
#         return render(request, 'machine/add_step1.html', context)
#
#
# @login_required
# def machine_add_step2(request, machine_ID):
#     current_page = "private"
#     current_subpage = "machine_add_step2"
#     machine = get_object_or_404(Machine, pk=machine_ID)
#     num_cols = len(machine.analysis_source_columns.all())
#     machine_input = machine.analysissource_columnnameinput
#     machine_output = machine.analysissource_columnnameoutput
#     machine_ignore = machine.analysissource_columnnameignore
#     machine_data = {'IN':machine_input, 'OUT':machine_output, 'IGN':machine_ignore}
#
#     return render(request, 'machine/add_step2.html', {
#                             "current_page": current_page,
#                             "current_subpage": current_subpage,
#                             "machine": machine,
#                             "num_cols": num_cols,
#                             "machine_input": machine_input,
#                             "machine_output": machine_output,
#                             "machine_data" : machine_data,
#                         })
#
#
# @receiver(post_save, sender=Machine)
# def machine_save_step2(sender, instance, **kwargs):
#     pass
#
# @login_required
# def machine_edit(request, machine_ID):
#     context = {}
#     current_page = "private"
#     current_subpage = "machine_edit"
#
#     machine = get_object_or_404(Machine, pk=machine_ID)
#     if request.POST:
#         form = MachineForm(request.POST, request.FILES)
#         context.update(locals())
#         if form.is_valid():
#             entry = form.save()
#             entry.created_by = request.user
#             entry.save()
#             return HttpResponseRedirect('/machine/%s/' % entry.id)
#         else:
#             return render(request, 'machine/add_step1.html', context)
#     else:
#         form = MachineForm()
#         context.update(locals())
#         return render(request, 'machine/add_step1.html', context)
#
#
# @user_can_view_machine
# def machine_project(request, machine_ID):
#     current_page = "private"
#     current_subpage = "machine_project"
#     machine = get_object_or_404(Machine, pk=machine_ID)
#     return render(request, 'machine/project.html', {
#                         "current_page": current_page,
#                         "current_subpage": current_subpage,
#                         "machine": machine,
#                     })
#
#
# def machine_input(request, machine_ID):
#     current_page = "private"
#     current_subpage = "machine_input"
#     machine = get_object_or_404(Machine, pk=machine_ID)
#     num_cols = len(machine.analysis_source_columns.all())
#     machine_input = machine.analysissource_columnnameinput
#     machine_output = machine.analysissource_columnnameoutput
#     machine_ignore = machine.analysissource_columnnameignore
#     machine_data = {'IN':machine_input, 'OUT':machine_output, 'IGN':machine_ignore}
#     error_present = True
#     warning_present = True
#
#     table_name = "brain_"+ str(machine_ID) + "_datainputlines"
#     sql = "select * from braindata."+table_name+" "+"limit 5"
#     cursor = connection.cursor()
#     query = cursor.execute(sql)
#     row = cursor.fetchall()
#     sql_for_col = "show columns from braindata."+table_name+""
#     query2 = cursor.execute(sql_for_col)
#     col = cursor.fetchall()
#
#     return render(request, 'machine/input.html', {
#                         "current_page": current_page,
#                         "current_subpage": current_subpage,
#                         "machine": machine,
#                         "num_cols": num_cols,
#                         "error_present": error_present,
#                         "warning_present": warning_present,
#                         "machine_input" : machine_input,
#                         "machine_output" : machine_output,
#                         "machine_data":machine_data,
#                         "row":row,
#                         "col":col,
#                     })
#
#
# def machine_output(request, machine_ID):
#     current_page = "private"
#     current_subpage = "machine_output"
#     machine = get_object_or_404(Machine, pk=machine_ID)
#     num_cols = len(machine.analysis_source_columns.all())
#     error_present = True
#     warning_present = True
#     machine_input = machine.analysissource_columnnameinput
#     machine_output = machine.analysissource_columnnameoutput
#
#     table_name = "brain_"+ str(machine_ID) + "_datainputlines"
#     sql = "select * from braindata."+table_name+" "+"limit 5"
#     cursor = connection.cursor()
#     query = cursor.execute(sql)
#     row = cursor.fetchall()
#     sql_for_col = "show columns from braindata."+table_name+""
#     query2 = cursor.execute(sql_for_col)
#     col = cursor.fetchall()
#
#     return render(request, 'machine/output.html', {
#                         "current_page": current_page,
#                         "current_subpage": current_subpage,
#                         "machine": machine,
#                         "num_cols": num_cols,
#                         "error_present": error_present,
#                         "warning_present": warning_present,
#                         "machine_input": machine_input,
#                         "machine_output": machine_output,
#                         "row":row,
#                         "col":col,
#                     })
#
#
# def machine_nn_parameters(request, machine_ID):
#     context = {}
#     current_page = "private"
#     current_subpage = "machine_nn_parameters"
#     machine = get_object_or_404(Machine, pk=machine_ID)
#     if request.POST:
#         form = ParameterForm(request.POST, instance=machine)
#         context.update(locals())
#         if form.is_valid():
#             entry = form.save()
#             entry.created_by = request.user
#             entry.save()
#             return HttpResponseRedirect('/machine/%s/parameters/' % entry.id)
#         else:
#             return render(request, 'machine/nn_parameters.html', context)
#     else:
#         form = ParameterForm(instance=machine)
#         context.update(locals())
#         return render(request, 'machine/nn_parameters.html', context)
#
#
# def machine_tensorboard(request, machine_ID):
#     current_page = "private"
#     current_subpage = "machine_tensorboard"
#     machine = get_object_or_404(Machine, pk=machine_ID)
#     return render(request, 'machine/tensorboard.html', {
#                         "current_page": current_page,
#                         "current_subpage": current_subpage,
#                         "machine": machine,
#                     })
#
#
# def machine_graph(request, machine_ID):
#     current_page = "private"
#     current_subpage = "machine_graph"
#     machine = get_object_or_404(Machine, pk=machine_ID)
#     return render(request, 'machine/graph.html', {
#                         "current_page": current_page,
#                         "current_subpage": current_subpage,
#                         "machine": machine,
#                         })
#
#
# def work(request, machine_ID):
#     current_page = "private"
#     current_subpage = "work"
#     return render(request, 'machine/work.html',
#                         {"current_page": current_page, "current_subpage": current_subpage})
#
#
# def generate(request):
#     current_page = "private"
#     current_subpage = "generate"
#     return render(request, 'machine/generate.html',
#                         {"current_page": current_page, "current_subpage": current_subpage})
#
#
# def messages(request, machine_ID):
#     current_page = "private"
#     current_subpage = "messages"
#     machine = get_object_or_404(Machine, pk=machine_ID)
#     messages = MachineMessage.objects.filter(machine=machine)
#     return render(request, 'machine/messages.html', locals())


###############################################################################################
# REST commands
###############################################################################################
# Machine
class MachineViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create( self, serializer ):
        serializer.save( Owner_User_ID=self.request.user )
