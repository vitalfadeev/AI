import os
from functools import wraps

from django.http import HttpResponseRedirect, HttpResponse, FileResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from graph import graphs
from graph.models import Graph
from machine.datainput import datatable
from machine.models import Machine
from machine.forms import MachineAddForm, MachineDescribeForm, MachineMainForm, MachineNNParametersForm, \
    MachineNNShapeForm, MachineInputGraphForm, MachineImportationFromFileForm
from machine.renderers import CSVRenderer, XLSRenderer, XMLRenderer, XLSXRenderer
from machine.serializers import MachineSerializer

from rest_framework import generics, viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework import renderers


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
    from machine.exportation.formats import FORMAT_CSV, FORMAT_XLS, FORMAT_XLSX, FORMAT_JSON, FORMAT_XML

    context = {}
    machine = get_object_or_404( Machine, pk=Machine_ID )

    model = machine.get_machine_data_input_lines_model()
    table = model._meta.db_table

    if "format" in request.GET:
        from_id = request.GET.get("from_id", None)
        format  = request.GET.get("format", FORMAT_CSV)

        # read data from DB to [[],[],]
        from machine.exportation.exportation import ProcessRead

        data = ProcessRead( 'MachineData', table, ExportLinesAfterPrimaryKey=from_id, FormatOutput=format, index_col="LineInput_ID" )

        if format == FORMAT_CSV:
            response = HttpResponse( data, content_type="text/csv" )
            response['Content-Disposition'] = f"attachment; filename={table}.csv"

        elif format == FORMAT_XLS:
            response = HttpResponse( data, content_type="application/xls" )
            response['Content-Disposition'] = f"attachment; filename={table}.xls"

        elif format == FORMAT_XLSX:
            response = HttpResponse( data, content_type="application/xlsx" )
            response['Content-Disposition'] = f"attachment; filename={table}.xlsx"

        elif format == FORMAT_JSON:
            response = HttpResponse( data, content_type="application/json" )
            response['Content-Disposition'] = f"attachment; filename={table}.json"

        elif format == FORMAT_XML:
            response = HttpResponse( data, content_type="application/xml" )
            response['Content-Disposition'] = f"attachment; filename={table}.xml"

        else:
            raise Exception( f"unsupported format: {format}" )

    else:
        context.update( locals() )
        return render(request, 'machine/MachineExportationToFile.html', context)

    return response


@login_required
def MachineExportationWithAPI( request, Machine_ID ):
    context = {}
    machine = get_object_or_404( Machine, pk=Machine_ID )

    context.update( locals() )
    return render(request, 'machine/MachineExportationWithAPI.html', context)


@csrf_exempt
@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer, CSVRenderer, XLSRenderer, XLSXRenderer, JSONRenderer, XMLRenderer])
def ApiMachineInputLines( request, Machine_ID, format=None ):
    return MachineExportationToFile( request, Machine_ID )


##############################################################################3
# Importation
##############################################################################3
def handle_uploaded_file( f, Machine_ID ):
    os.makedirs( f'/tmp/{Machine_ID}/importation', exist_ok=True )
    local_file = f'/tmp/{Machine_ID}/importation/{f.name}'

    with open( local_file, 'wb+' ) as destination:
        for chunk in f.chunks():
            destination.write( chunk )

    return  local_file


@login_required
def ImportationFromFile( request, Machine_ID ):
    context = {}
    machine = get_object_or_404( Machine, pk=Machine_ID )

    if request.POST:
        form = MachineImportationFromFileForm( request.POST, request.FILES )
        if form.is_valid():
            from machine.importation.importation import import_from_file

            local_path = handle_uploaded_file( request.FILES[ 'file' ], Machine_ID )

            if form.cleaned_data['clear_or_append'] == "DELETE":
                import_from_file( machine, local_path, delete_old=True )
            else:
                import_from_file( machine, local_path, delete_old=False )

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

    if request.POST:
        if "file" in request.FILES:
            from machine.importation.importation import import_from_file
            local_path = handle_uploaded_file( request.FILES[ 'file' ], Machine_ID )
            import_from_file( machine, local_path, delete_old=False )
        else:
            from machine.importation.importation import with_api_post
            with_api_post( request, machine )

    else:
        columns = machine.get_machine_data_input_lines_columns()
        context.update( locals() )
        return render(request, 'machine/MachineImportationWithAPI.html', context)


class ImportationWithAPI2( APIView ):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def ImportationWithAPI3(request, format=None):
    content = {
        'user': str(request.user),  # `django.contrib.auth.User` instance.
        'auth': str(request.auth),  # None
    }
    return Response(content)


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
