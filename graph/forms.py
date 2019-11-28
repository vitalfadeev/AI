from django.forms import ModelForm, ChoiceField, CharField

#
# class GraphForm(ModelForm):
#     class Meta:
#         from .models import Graph
#         model = Graph
#
#         fields = (
#             'GraphType',
#             'X',
#             'Y',
#             'Z',
#             'color',
#             #'Animation_Frame',
#             'ColorScales',
#         )
#         fields_required = []
#         labels = {
#             'GraphType'         :'Graph Type',
#             'X'                 :'X',
#             'Y'                 :'Y',
#             'Z'                 :'Z',
#             'color'             :'color',
#             #'Animation_Frame'   :'Animation Frame',
#             'ColorScales'       :'Color Scales',
#         }
#
#     def __init__(self, batch, *args, **kwargs):
#         super(GraphForm, self).__init__(*args, **kwargs)
#
#         columns = [(col, col) for col in batch.titles]
#         color_columns = [(col, col) for (col, typ) in zip(batch.titles, batch.types) if typ in ['OPTION', 'BINARY'] ]
#
#         self.fields['X'] = ChoiceField(choices = columns)
#         self.fields['Y'] = ChoiceField(choices = columns)
#         self.fields['Z'] = ChoiceField(choices = columns)
#
#         if color_columns:
#             self.fields['color'] = ChoiceField(choices = color_columns)
#         else:
#             self.fields['color'] = CharField(max_length=255)
#
#         if 'instance' not in kwargs:
#             if len(columns) >= 1:
#                 self.initial['X'] = columns[0][0]
#             if len(columns) >= 2:
#                 self.initial['Y'] = columns[1][0]
#             if len(columns) >= 3:
#                 self.initial['Z'] = columns[2][0]
#             if len(color_columns) >= 1:
#                 self.initial['color'] = color_columns[0][0]
#             self.initial['GraphType'] = "1"
#             self.initial['ColorScales'] = "1"
