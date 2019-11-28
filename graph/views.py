from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.generic import FormView
from rest_framework.permissions import IsAuthenticated

from graph.models import Graph
from graph.serializers import GraphSerializer
from rest_framework import generics, viewsets
from rest_framework import mixins


class GraphViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    #permission_classes = ( IsAuthenticated, )
    serializer_class = GraphSerializer
    queryset = Graph.objects.all()
    # + graph.render_div()


#
# @method_decorator(login_required, name='dispatch')
# class GraphView(FormView):
#     model = Graph
#     pk_url_kwarg = 'batch_id'
#     form_class = GraphForm
#     template_name = 'view_graph.html'
#
#     def get(self, request, machine_ID, *args, **kwargs):
#         from . import graphs
#         from machine.models import Machine
#
#         self.machine_ID = machine_ID
#         machine = Machine.objects.get(pk=machine_ID, User_ID=request.user)
#
#         try:
#             instance = Graph.objects.get(pk=machine_ID)
#             form = self.form_class(batch, instance=instance)
#             GraphType = instance.GraphType
#             x = instance.X
#             y = instance.Y
#             z = instance.Z
#             color = instance.color
#             colorset = instance.ColorScales
#
#         except Graph.DoesNotExist:
#             form = self.form_class(batch, initial=self.initial)
#             GraphType = form.initial['GraphType']
#             x = form.initial['X']
#             y = form.initial['Y']
#             z = form.initial['Z']
#             color = None
#             colorset = form.initial['ColorScales']
#
#         try:
#             if GraphType == "1":
#                 graph_div = graphs.g1(machine_ID, x, y, color, colorset)
#             elif GraphType == "2":
#                 graph_div = graphs.g2(machine_ID, x, y, color, colorset)
#             elif GraphType == "3":
#                 graph_div = graphs.g3(machine_ID, x, y, color, colorset)
#             elif GraphType == "4":
#                 graph_div = graphs.g4(machine_ID, x, y, z, color, colorset)
#             elif GraphType == "5":
#                 graph_div = graphs.g5(machine_ID, color, colorset)
#             elif GraphType == "6":
#                 graph_div = graphs.g6(machine_ID, x, y, color, z, colorset)
#             elif GraphType == "7":
#                 graph_div = graphs.g7(machine_ID, x, y, colorset)
#             elif GraphType == "8":
#                 graph_div = graphs.g8(machine_ID, x, y, colorset)
#             elif GraphType == "9":
#                 graph_div = graphs.g9(machine_ID, x, y, color, colorset)
#             elif GraphType == "10":
#                 graph_div = graphs.g10(machine_ID, x, y, z, color, colorset)
#             else:
#                 graph_div = ''
#
#         except Exception as e:
#             graph_div = """<div class="card-panel yellow lighten-5">
#                             {}
#                            </div>
#                         """.format(repr(e))
#
#         context = {
#             'form': form,
#             'batch_id': machine_ID,
#             'graph_div': graph_div,
#             'url_name': resolve(request.path_info).url_name,
#         }
#         return render(request, self.template_name, context)
#
#     def post(self, request, machine_ID, *args, **kwargs):
#         self.machine_ID = machine_ID
#         batch = Machine.objects.get(pk=machine_ID, User_ID=request.user)
#
#         try:
#             instance = Graph.objects.get(pk=machine_ID)
#             form = self.form_class(batch, request.POST)
#
#         except Graph.DoesNotExist:
#             form = self.form_class(batch, request.POST)
#
#
#         if form.is_valid():
#             instance = form.save(commit=False)
#             instance.Batch_Id = batch
#             instance.save()
#             url = self.get_success_url()
#             return HttpResponseRedirect(url)
#         else:
#             return self.form_invalid(form)
#
#     def get_form(self, form_class=None):
#         return self.form_class(self.batch_id, **self.get_form_kwargs())
#
#     def get_success_url(self):
#         return reverse('view_id_graph', kwargs={'batch_id': self.batch_id})
