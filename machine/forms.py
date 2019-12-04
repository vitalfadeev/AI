from django import forms
from django.forms import ModelForm
from django_mysql.forms import JSONField

from graph.models import Graph
from machine.models import Machine


class MachineAddForm( ModelForm ):
    class Meta:
        model = Machine
        fields = [
            'Project_Name',
            'Project_Description',
            'Project_DataSourceIsPublic',
            'Project_DataSourceSampleOnlyPublic',
            'Project_DataSource_PriceUSD',
            'Project_DataSourceIsPrivate',
            'input_file',
        ]


class MachineMainForm( ModelForm ):
    class Meta:
        model = Machine
        fields = [
            'Project_Name',
            'Project_Description',
            'Project_DataSourceIsPublic',
            'Project_DataSourceSampleOnlyPublic',
            'Project_DataSource_PriceUSD',
            'Project_DataSourceIsPrivate',
        ]


class MachineDescribeForm( ModelForm ):
    class Meta:
        model = Machine
        fields = [
            'Project_ColumnsDescription',
            'AnalysisSource_ColumnsNameInput',
            'AnalysisSource_ColumnsNameOutput',
            'AnalysisSource_ColumnType',
            'AnalysisSource_Errors',
            'AnalysisSource_Warnings',
        ]


class MachineNNParametersForm( ModelForm ):
    class Meta:
        model = Machine
        fields = [
            'ParameterCNN_ShapeAuto',
            'ParameterCNN_Loss',
            'ParameterCNN_Optimizer',
        ]



class MachineNNShapeForm( ModelForm ):
    class Meta:
        model = Machine
        fields = [
            'ParameterCNN_Shape',
            # 'ParameterCNN_BatchEpochAuto',
            # 'ParameterCNN_BatchSize',
            # 'ParameterCNN_Epoch',
        ]


class MachineInputGraphForm( ModelForm ):
    class Meta:
        model = Graph
        fields = [
            "GraphType",
            "ColorScaleSet",
            "X",
            "Y",
            "Z",
            "Color",
            # "Animation_Frame",
        ]


class MachineImportationFromFileForm( forms.Form ):
    from_file = forms.FileField()
    clear_or_append = forms.HiddenInput()


