from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save
from django.dispatch import receiver
from machine.models import Machine, Column
from team.models import Team
from machine.forms import MachineForm, ParameterForm
from machine.decorators import user_can_view_machine, user_can_edit_machine

from machine.analysis.DataPreAnalyser import analyse_source_data_find_input_output
from machine.analysis.ReadInputLinesFileUploaded import GetDataFrameFromFileData
from machine.analysis.DataLinesStore import DataLinesInputStore
from machine.analysis.DataLinesRead import DataLinesInputRead
import pandas as pd

# from machine.analysis.DataLinesInputStore import DataLinesInputStore
from rest_framework import viewsets
from machine.serializers import ColumnSerializer

from machine.models import MachineMessage

from django.db import connection

# Create your views here.
def machine_public_list(request):
    current_page = "public"
    current_subpage = "public"
    machines = Machine.objects.filter(is_public=True).order_by('-created_date')
    return render(request, 'machine/public_list.html',
                        {"current_page": current_page, "machines": machines, "current_subpage": current_subpage})


def machine_private_list(request):
    current_page = "private"
    current_subpage = "private"
    machines = Machine.objects.filter(created_by=request.user).order_by('-created_date')
    return render(request, 'machine/private_list.html',
                        {"current_page": current_page, "machines": machines, "current_subpage": current_subpage})


@login_required
def machine_add_step1(request):
    context = {}
    current_page = "private"
    current_subpage = "add"
    
    if request.POST:
        form = MachineForm(request.POST, request.FILES)
        form.fields['team'].queryset = Team.objects.filter(members=request.user)
        context.update(locals())
        if form.is_valid():
            entry = form.save()
            entry.created_by = request.user
            entry.save()
            return HttpResponseRedirect('/machine/add/%s/' % entry.id)
        else:
            return render(request, 'machine/add_step1.html', context)
    else:
        form = MachineForm()
        form.fields['team'].queryset = Team.objects.filter(members=request.user)
        context.update(locals())
        return render(request, 'machine/add_step1.html', context)


@receiver(post_save, sender=Machine)
def machine_save_step1(sender, instance, **kwargs):
    # Processing the data:
    data_from_file = pd.read_excel(instance.input_file.path)
    pre_analysis = analyse_source_data_find_input_output(data_from_file)
    print('-------------------INPUT COLUMNS----------------------')
    print(pre_analysis.column_names_input)
    print('-------------------OUTPUT COLUMNS----------------------')
    print(pre_analysis.column_names_output)
    print('-------------------COLUMN TYPES------------------------')
    print(pre_analysis.column_types)
    print('-------------------WARNINGS--------------------------')
    print(pre_analysis.warning_info)
    print('-------------------ERRORS---------------------------')
    print(pre_analysis.errors_info)
    
    data_frame = GetDataFrameFromFileData(instance.input_file.path)
    
    last_inserted_line_id = DataLinesInputStore(instance.id, 
                                                data_frame)

    machine_input = []
    machine_output = []
    machine_ignore = []
 
    for col in data_frame:
        if col in pre_analysis.column_names_input:
            instance.analysis_source_columns.create(
                                            column_type="IN",
                                            name=col, desc=" "
                                        )
            machine_input.append(col.replace('_',' ')) 
        elif col in pre_analysis.column_names_output:
            instance.analysis_source_columns.create(
                                            column_type="OUT",
                                            name=col, desc=" "
                                        )
            machine_output.append(col.replace('_',' '))

        else:
            instance.analysis_source_columns.create(
                                            column_type="IGN",
                                            name=col, desc=" "
                                        )
            machine_ignore.append(col.replace('_',' '))

    instance.analysissource_columnnameinput = machine_input
    instance.analysissource_columnnameoutput = machine_output
    instance.analysissource_columnnameignore = machine_ignore

    # DataLinesInputStore(instance.id, instance.created_by.id,
    #                     data_frame, output=False)


def machine_add_step2(request, machine_ID):
    current_page = "private"
    current_subpage = "machine_add_step2"
    machine = get_object_or_404(Machine, pk=machine_ID)
    num_cols = len(machine.analysis_source_columns.all())
    machine_input = machine.analysissource_columnnameinput
    machine_output = machine.analysissource_columnnameoutput
    machine_ignore = machine.analysissource_columnnameignore
    machine_data = {'IN':machine_input, 'OUT':machine_output, 'IGN':machine_ignore}

    return render(request, 'machine/add_step2.html', {
                            "current_page": current_page,
                            "current_subpage": current_subpage,
                            "machine": machine,
                            "num_cols": num_cols,
                            "machine_input": machine_input,
                            "machine_output": machine_output,
                            "machine_data" : machine_data,
                        })


@receiver(post_save, sender=Machine)
def machine_save_step2(sender, instance, **kwargs):
    pass

@login_required
def machine_edit(request, machine_ID):
    context = {}
    current_page = "private"
    current_subpage = "machine_edit"
    
    machine = get_object_or_404(Machine, pk=machine_ID)
    if request.POST:
        form = MachineForm(request.POST, request.FILES)
        context.update(locals())
        if form.is_valid():
            entry = form.save()
            entry.created_by = request.user
            entry.save()
            return HttpResponseRedirect('/machine/%s/' % entry.id)
        else:
            return render(request, 'machine/add_step1.html', context)
    else:
        form = MachineForm()
        context.update(locals())
        return render(request, 'machine/add_step1.html', context)


@user_can_view_machine
def machine_project(request, machine_ID):
    current_page = "private"
    current_subpage = "machine_project"
    machine = get_object_or_404(Machine, pk=machine_ID)
    return render(request, 'machine/project.html', {
                        "current_page": current_page,
                        "current_subpage": current_subpage,
                        "machine": machine,
                    })


def machine_input(request, machine_ID):
    current_page = "private"
    current_subpage = "machine_input"
    machine = get_object_or_404(Machine, pk=machine_ID)
    num_cols = len(machine.analysis_source_columns.all())
    machine_input = machine.analysissource_columnnameinput
    machine_output = machine.analysissource_columnnameoutput
    machine_ignore = machine.analysissource_columnnameignore
    machine_data = {'IN':machine_input, 'OUT':machine_output, 'IGN':machine_ignore}
    error_present = True
    warning_present = True

    table_name = "brain_"+ str(machine_ID) + "_datainputlines" 
    sql = "select * from braindata."+table_name+" "+"limit 5"
    cursor = connection.cursor()
    query = cursor.execute(sql)
    row = cursor.fetchall()
    sql_for_col = "show columns from braindata."+table_name+""
    query2 = cursor.execute(sql_for_col)
    col = cursor.fetchall()

    return render(request, 'machine/input.html', {
                        "current_page": current_page,
                        "current_subpage": current_subpage,
                        "machine": machine,
                        "num_cols": num_cols,
                        "error_present": error_present,
                        "warning_present": warning_present,
                        "machine_input" : machine_input,
                        "machine_output" : machine_output,
                        "machine_data":machine_data,
                        "row":row,
                        "col":col,
                    })


def machine_output(request, machine_ID):
    current_page = "private"
    current_subpage = "machine_output"
    machine = get_object_or_404(Machine, pk=machine_ID)
    num_cols = len(machine.analysis_source_columns.all())
    error_present = True
    warning_present = True
    machine_input = machine.analysissource_columnnameinput
    machine_output = machine.analysissource_columnnameoutput
    
    table_name = "brain_"+ str(machine_ID) + "_datainputlines" 
    sql = "select * from braindata."+table_name+" "+"limit 5"
    cursor = connection.cursor()
    query = cursor.execute(sql)
    row = cursor.fetchall()
    sql_for_col = "show columns from braindata."+table_name+""
    query2 = cursor.execute(sql_for_col)
    col = cursor.fetchall()

    return render(request, 'machine/output.html', {
                        "current_page": current_page, 
                        "current_subpage": current_subpage,
                        "machine": machine,
                        "num_cols": num_cols,
                        "error_present": error_present,
                        "warning_present": warning_present,
                        "machine_input": machine_input,
                        "machine_output": machine_output,
                        "row":row,
                        "col":col,
                    })


def machine_nn_parameters(request, machine_ID):
    context = {}
    current_page = "private"
    current_subpage = "machine_nn_parameters"
    machine = get_object_or_404(Machine, pk=machine_ID)
    if request.POST:
        form = ParameterForm(request.POST, instance=machine)
        context.update(locals())
        if form.is_valid():
            entry = form.save()
            entry.created_by = request.user
            entry.save()
            return HttpResponseRedirect('/machine/%s/parameters/' % entry.id)
        else:
            return render(request, 'machine/nn_parameters.html', context)
    else:
        form = ParameterForm(instance=machine)
        context.update(locals())
        return render(request, 'machine/nn_parameters.html', context)


def machine_tensorboard(request, machine_ID):
    current_page = "private"
    current_subpage = "machine_tensorboard"
    machine = get_object_or_404(Machine, pk=machine_ID)
    return render(request, 'machine/tensorboard.html', {
                        "current_page": current_page,
                        "current_subpage": current_subpage,
                        "machine": machine,
                    })


def machine_graph(request, machine_ID):
    current_page = "private"
    current_subpage = "machine_graph"
    machine = get_object_or_404(Machine, pk=machine_ID)
    return render(request, 'machine/graph.html', {
                        "current_page": current_page,
                        "current_subpage": current_subpage,
                        "machine": machine,
                        })                        


def work(request, machine_ID):
    current_page = "private"
    current_subpage = "work"
    return render(request, 'machine/work.html',
                        {"current_page": current_page, "current_subpage": current_subpage})


def generate(request):
    current_page = "private"
    current_subpage = "generate"
    return render(request, 'machine/generate.html',
                        {"current_page": current_page, "current_subpage": current_subpage})


def messages(request, machine_ID):
    current_page = "private"
    current_subpage = "messages"
    machine = get_object_or_404(Machine, pk=machine_ID)
    messages = MachineMessage.objects.filter(machine=machine)
    return render(request, 'machine/messages.html', locals())


# ViewSets define the view behavior for API.
class ColumnViewSet(viewsets.ModelViewSet):
    queryset = Column.objects.all()
    serializer_class = ColumnSerializer
