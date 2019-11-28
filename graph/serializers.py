from rest_framework import serializers

from graph import graphs
from graph.models import Graph
from machine.models import Machine

class GraphSerializer(serializers.ModelSerializer):
    class Meta:
        model = Graph
        fields = ("Machine", "GraphType", "X", "Y", "Z", "Color", "ColorScales", "div")
        depth = 1

    div = serializers.SerializerMethodField()


    def validate_Machine(self, value):
        Machine_ID = int( value )
        machine = Machine.objects.get( pk=Machine_ID )
        value = machine
        return value

    def get_div( self, graph ):
        machine = graph.Machine
        GraphType = graph.GraphType
        x = graph.X
        y = graph.Y
        z = graph.Z
        color = None
        colorset = graph.ColorScales

        try:
            if GraphType == "1":
                graph_div = graphs.g1(machine, x, y, color, colorset)
            elif GraphType == "2":
                graph_div = graphs.g2(machine, x, y, color, colorset)
            elif GraphType == "3":
                graph_div = graphs.g3(machine, x, y, color, colorset)
            elif GraphType == "4":
                graph_div = graphs.g4(machine, x, y, z, color, colorset)
            elif GraphType == "5":
                graph_div = graphs.g5(machine, color, colorset)
            elif GraphType == "6":
                graph_div = graphs.g6(machine, x, y, color, z, colorset)
            elif GraphType == "7":
                graph_div = graphs.g7(machine, x, y, colorset)
            elif GraphType == "8":
                graph_div = graphs.g8(machine, x, y, colorset)
            elif GraphType == "9":
                graph_div = graphs.g9(machine, x, y, color, colorset)
            elif GraphType == "10":
                graph_div = graphs.g10(machine, x, y, z, color, colorset)
            else:
                graph_div = ''

        except Exception as e:
            graph_div = """<div class="card-panel yellow lighten-5">
                            {}
                           </div>
                        """.format(repr(e))

        return graph_div
