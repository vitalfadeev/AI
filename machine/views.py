import os

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings

from graph import graphs
from graph.models import Graph
from machine.datainput import datatable
from machine.models import Machine
from machine.forms import MachineAddForm, MachineDescribeForm, MachineMainForm, MachineNNParametersForm, \
    MachineNNShapeForm, MachineInputGraphForm
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
            return HttpResponseRedirect(f"/Machine/{entry.pk}/NN/Parameters")
        else:
            context.update( locals() )
            return render(request, 'machine/MachineDescribe.html', context)
    else:
        form = MachineDescribeForm( instance=machine )
        context.update(locals())
        return render(request, 'machine/MachineDescribe.html', context)


@method_decorator(login_required, name='dispatch')
class MachineDatatableAjax(datatable.DTView):
    """ Return Input data. Using with jquery.datatables """
    def get(self, request, Machine_ID):
        # Query from table BATCH_INPUT_NNN
        # without pk 'index'
        # return JSON
        machine = get_object_or_404( Machine, pk=Machine_ID )

        self.model = machine.get_machine_data_input_lines_model()
        self.columns = list( machine.AnalysisSource_ColumnType.keys() )
        self.order_columns = self.columns
        return super().get(request)


@login_required
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


# # import matplotlib.pyplot as plt
# # import numpy as np
# # from matplotlib.backends.backend_agg import FigureCanvasAgg
# # from django.http import HttpResponse
#
# # def MachineInputCorrelation1(request, Machine_ID):
# #     # Data for plotting
# #     t = np.arange(0.0, 2.0, 0.01)
# #     s = 1 + np.sin(2 * np.pi * t)
# #
# #     fig, ax = plt.subplots()
# #     ax.plot(t, s)
# #
# #     ax.set(xlabel='time (s)', ylabel='voltage (mV)',
# #            title='About as simple as it gets, folks')
# #     ax.grid()
# #
# #     response = HttpResponse(content_type = 'image/png')
# #     canvas = FigureCanvasAgg(fig)
# #     canvas.print_png(response)
# #     return response
# #
# #
# @login_required
# def MachineInputCorrelation( request, Machine_ID ):
#     import random
#     import django
#     import datetime
#     import plotly
#
#     from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
#     from matplotlib.figure import Figure
#     from matplotlib.dates import DateFormatter
#     # import seaborn as sns
#
#     fig=Figure()
#     ax=fig.add_subplot(111)
#     x=[]
#     y=[]
#     now=datetime.datetime.now()
#     delta=datetime.timedelta(days=1)
#     for i in range(10):
#         x.append(now)
#         now+=delta
#         y.append(random.randint(0, 1000))
#     ax.plot_date(x, y, '-')
#     ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
#     fig.autofmt_xdate()
#
#     canvas=FigureCanvas(fig)
#
#     figure_dir = f"/media/machine/{Machine_ID}"
#     os.makedirs( f"{settings.BASE_DIR}/{figure_dir}", exist_ok=True )
#
#     cfile = f"{settings.BASE_DIR}/{figure_dir}/InputCorrelations.png"
#     figure_url = f"{figure_dir}/InputCorrelations.png"
#
#     with open( cfile, 'wb' ) as f:
#         canvas.print_png(f)
#
#     context = {}
#     context.update( locals() )
#     return render(request, 'machine/MachineInputCorrelation.html', context)
#
#
#
# def MachineInputCorrelation0( request, Machine_ID ):
#     context = {}
#     machine = get_object_or_404( Machine, pk=Machine_ID )
#
#     import seaborn as sns
#     import matplotlib.pyplot as plt
#     from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
#     # import mpld3
#
#     # Data
#     # model = machine.get_machine_data_input_lines_model()
#     # df = model.as_pandas_dataframe()
#
#     # Figure
#     # sns.set(context='talk', style='white')
#     # fig = Figure()
#     # fig, ax = plt.subplots()
#     #
#     # def create_figure():
#     #     from matplotlib.figure import Figure
#     #     import random
#     #
#     #     fig = Figure()
#     #     axis = fig.add_subplot( 1, 1, 1 )
#     #     xs = range( 100 )
#     #     ys = [ random.randint( 1, 50 ) for x in xs ]
#     #     axis.plot( xs, ys )
#     #     return fig
#
#
#     # sns.set(context='talk', style='white')
#     # fig = create_figure()
#     # correlation_matrix = df.corr()
#     # heat_map = sns.heatmap( correlation_matrix, annot=True )
#     # output = io.BytesIO()
#     # FigureCanvas(fig).print_png(output)
#     # return HttpResponse(output.getvalue(), content_type="image/png")
#     context.update( locals() )
#     return render(request, 'machine/MachineInputCorrelation.html', context)
#
#     #
#     # # fig = plt.figure()
#     # # ax = fig.gca()
#     # # ax.plot( [ 1, 2, 3, 4 ] )
#     # plt.plot( [ 0, 1, 2, 3, 4 ], [ 0, 3, 5, 9, 11 ] )
#     #
#     # # mpld3.show( fig )
#     #
#     # # Correlation
#     # # correlation_matrix = df.corr()
#     # heat_map = sns.heatmap( correlation_matrix, annot=True )
#     # # heat_map = sns.heatmap( correlation_matrix, ax=ax, annot=True )
#     #
#     # # Render
#     # # html = mpld3.fig_to_html( fig )
#     #
#     # #plt.tight_layout()
#     # # figure_dir = f"/media/machine/{Machine_ID}"
#     # # os.makedirs( figure_dir, exist_ok=True )
#     # #
#     # # cfile = f"{settings.BASE_DIR}/{figure_dir}/InputCorrelations.png"
#     # # figure_url = f"{settings.BASE_DIR}/InputCorrelations.png"
#     # #
#     # # output = io.BytesIO()
#     # # FigureCanvas(fig).print_png(output)
#     # #
#     # # with open( cfile, 'wb' ) as f:
#     #     # FigureCanvas( fig ).print_png( f )
#     #
#     # cfile = "/tmp/books_read2.png"
#     # plt.savefig( cfile )
#     #
#     # #
#     # context.update( locals() )
#     #
#     # return render(request, 'machine/MachineInputCorrelation.html', context)
#     # # return HttpResponse(output.getvalue(), content_type="image/png")



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
