import os
from functools import wraps

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings

from graph import graphs
from graph.models import Graph
from machine.datainput import datatable
from machine.decorators import file_import_required
from machine.models import Machine
from machine.forms import MachineAddForm, MachineDescribeForm, MachineMainForm, MachineNNParametersForm, \
    MachineNNShapeForm, MachineInputGraphForm, MachineImportationFromFileForm
from machine.serializers import MachineSerializer

from rest_framework import generics, viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated


##############################################################################3
# Tools
##############################################################################3
def serve_html(filename):
    image_data = open(filename, "rb").read()
    return HttpResponse(image_data, content_type="text/html")

def serve_image(filename):
    image_data = open(filename, "rb").read()
    return HttpResponse(image_data, content_type="image/png")


##############################################################################3
# Machines
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
# Input
##############################################################################3
@login_required
def MachineMain( request, Machine_ID ):
    context = {}
    machine = get_object_or_404( Machine, pk=Machine_ID )

    if request.POST:
        form = MachineMainForm( request.POST, instance=machine )

        if form.is_valid():
            entry = form.save(commit=False)
            entry.save()
            return HttpResponseRedirect(f"/Machines")
        else:
            context.update( locals() )
            return render(request, 'machine/MachineMain.html', context)
    else:
        form = MachineMainForm( instance=machine )
        context.update( locals() )
        return render(request, 'machine/MachineMain.html', context)


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
            from machine.loader import django_loader
            django_loader.load( entry )
            return HttpResponseRedirect(f"/Machine/{entry.pk}/NN/Parameters")
        else:
            context.update( locals() )
            return render(request, 'machine/MachineDescribe.html', context)
    else:
        form = MachineDescribeForm( instance=machine )
        context.update(locals())
        return render(request, 'machine/MachineDescribe.html', context)


@login_required
def MachineDatatableAjax( request, Machine_ID ):
    """ Return Input data. Using with jquery.datatables """
    import json
    from django_datatables_view.mixins import LazyEncoder
    from machine.datalistener import GetFileData

    # Query from table BATCH_INPUT_NNN
    # without pk 'index'
    # return JSON
    machine = get_object_or_404( Machine, pk=Machine_ID )

    url = os.path.join( settings.MEDIA_ROOT, machine.input_file.name )
    df = GetFileData( url )
    columns = machine.AnalysisSource_ColumnType.keys()

    # "draw"
    # "start"
    # "length"
    # "search[value]"
    # "order[i]"
    # "columns[i]"

    draw = int( request.POST["draw"] )
    start = int( request.POST["start"] )
    length = int( request.POST["length"] )

    # get block
    data = df.head().values.tolist()
    data = df.iloc[start:start+length]
    total = len(df.index)

    # replace NaN to ''
    import numpy as np
    data = data.replace( np.nan, '', regex=True )

    # reorder
    data = data[columns]

    # to list
    data = data.values.tolist()

    response = {
        "draw": draw,
        "recordsTotal": total,
        "recordsFiltered": total,
        "data": data,
        # "error": False,
        "result": "ok"
    }

    dump = json.dumps(response, cls=LazyEncoder)

    return HttpResponse( dump, content_type='application/json' )


@login_required
#@file_import_required
def MachineInputCorrelation( request, Machine_ID ):
    import plotly.graph_objects as go
    import plotly.offline as opy

    context = {}
    machine = get_object_or_404( Machine, pk=Machine_ID )

    # Data
    model = machine.get_machine_data_input_lines_model()
    inout_cols = machine.AnalysisSource_ColumnsNameInput + machine.AnalysisSource_ColumnsNameOutput
    df = model.as_pandas_dataframe( inout_cols )

    import pandas as pd
    for c, t in machine.AnalysisSource_ColumnType.items():
        if c in inout_cols:
            if t == "FLOAT" or t == "NUMERIC":
                df[ c ] = pd.to_numeric( df[ c ], errors='coerce' )

    # Corr
    correlation_matrix = df.corr() # .values.tolist()

    # Render
    fig = go.Figure( data=go.Heatmap( x=correlation_matrix.columns, y=correlation_matrix.columns, z=correlation_matrix ) )

    div = opy.plot(fig, auto_open=False, output_type='div')

    context.update( locals() )
    return render(request, 'machine/MachineInputCorrelation.html', context)


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
    shapes = range(10)

    if request.POST:
        form = MachineNNShapeForm( request.POST, instance=machine )

        if form.is_valid():
            entry = form.save(commit=False)
            entry.save()
            return HttpResponseRedirect(f"/Machine/{Machine_ID}/NN/Shape")
            # return HttpResponseRedirect(f"/Machines")
        else:
            context.update( locals() )
            return render(request, 'machine/MachineNNShape.html', context)
    else:
        form = MachineNNShapeForm( instance=machine )
        context.update( locals() )
        return render(request, 'machine/MachineNNShape.html', context)


@login_required
def MachineNNTensorboard( request, Machine_ID ):
    context = {}
    context.update( locals() )
    return render(request, 'machine/MachineNNTensorboard.html', context)


@login_required
def MachineNNTensorboardEngine( request, Machine_ID ):
    return serve_html(settings.BASE_DIR + '/static/tensorboard/index.html')

@login_required
def MachineNNTensorboardEngineStatic( request, Machine_ID, ResourceFile ):
    return serve_image( settings.BASE_DIR + '/static/tensorboard/tf-interactive-inference-dashboard/' + ResourceFile )



##############################################################################3
# Graph
##############################################################################3
@login_required
def MachineInputGraph( request, Machine_ID ):
    context = {}

    #
    machine = get_object_or_404( Machine, pk=Machine_ID )

    #
    try: graph = Graph.objects.get( Machine_ID=machine )
    except Graph.DoesNotExist: graph = Graph( Machine_ID=machine )

    #
    if request.POST:
        form = MachineInputGraphForm( request.POST, instance=graph )

        if form.is_valid():
            entry = form.save(commit=False)
            entry.save()
            return HttpResponseRedirect(f"/Machine/{Machine_ID}/InputGraph")
        else:
            pass
    else:
        form = MachineInputGraphForm( instance=graph )

    #
    GraphType = graph.GraphType

    try:
        if GraphType == "1":
            graph_div = graphs.g1(machine, graph.X, graph.Y, graph.Color, graph.ColorScaleSet)
        elif GraphType == "2":
            graph_div = graphs.g2(machine, graph.X, graph.Y, graph.Color, graph.ColorScaleSet)
        elif GraphType == "3":
            graph_div = graphs.g3(machine, graph.X, graph.Y, graph.Color, graph.ColorScaleSet)
        elif GraphType == "4":
            graph_div = graphs.g4(machine, graph.X, graph.Y, graph.Z, graph.Color, graph.ColorScaleSet)
        elif GraphType == "5":
            graph_div = graphs.g5(machine, graph.Color, graph.ColorScaleSet)
        elif GraphType == "6":
            graph_div = graphs.g6(machine, graph.X, graph.Y, graph.Color, graph.Z, graph.ColorScaleSet)
        elif GraphType == "7":
            graph_div = graphs.g7(machine, graph.X, graph.Y, graph.ColorScaleSet)
        elif GraphType == "8":
            graph_div = graphs.g8(machine, graph.X, graph.Y, graph.ColorScaleSet)
        elif GraphType == "9":
            graph_div = graphs.g9(machine, graph.X, graph.Y, graph.Color, graph.ColorScaleSet)
        elif GraphType == "10":
            graph_div = graphs.g10(machine, graph.X, graph.Y, graph.Z, graph.Color, graph.ColorScaleSet)
        else:
            graph_div = ''

    except Exception as e:
        graph_div = """<div class="card-panel yellow lighten-5">
                        {}
                       </div>
                    """.format(repr(e))

    #
    columns = machine.get_machine_data_input_columns()

    context.update( locals() )
    return render(request, 'machine/MachineInputGraph.html', context)


##############################################################################3
# Export
##############################################################################3
@login_required
def MachineExportationToFile( request, Machine_ID ):
    context = {}
    machine = get_object_or_404( Machine, pk=Machine_ID )

    context.update( locals() )
    return render(request, 'machine/MachineExportationToFile.html', context)


@login_required
def MachineExportationWithAPI( request, Machine_ID ):
    context = {}
    machine = get_object_or_404( Machine, pk=Machine_ID )

    context.update( locals() )
    return render(request, 'machine/MachineExportationWithAPI.html', context)




##############################################################################3
# Importation
##############################################################################3
@login_required
def ImportationFromFile( request, Machine_ID ):
    context = {}
    machine = get_object_or_404( Machine, pk=Machine_ID )

    if request.POST:
        form = MachineImportationFromFileForm( request.POST, request.FILES )
        if form.is_valid():
            from machine.importation.importation import import_from_file

            if form.cleaned_data['clear_or_append'] == "DELETE":
                import_from_file( machine, form.from_file.path, delete_old=True )
            else:
                import_from_file( machine, form.from_file.path, delete_old=False )

            return HttpResponseRedirect(f"/Machine/{Machine_ID}/Describe")
        else:
            context.update( locals() )
            return render(request, 'machine/MachineImportationFromFile.html', context)
    else:
        form = MachineImportationFromFileForm()
        context.update(locals())
        return render(request, 'machine/MachineImportationFromFile.html', context)


@login_required
def ImportationWithAPI( request, Machine_ID ):
    context = {}
    machine = get_object_or_404( Machine, pk=Machine_ID )

    context.update( locals() )
    return render(request, 'machine/MachineImportationWithAPI.html', context)


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
