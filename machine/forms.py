from django import forms
from django.forms import ModelForm
from django_mysql.forms import JSONField

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



#
# class ParameterForm(ModelForm):
#     LOSS_CHOICES = [
#         ('BinaryCrossentropy', 'Binary Crossentropy'),
#         ('SquaredHinge', 'Squared Hinge'),
#         ('Poisson', 'Poisson'),
#         ('MeanSquaredError', 'Mean Squared Error'),
#         ('MeanAbsoluteError', 'Mean Absolute Error'),
#         ('Huber', 'Huber'),
#         ('Hinge', 'Hinge'),
#         ('CosineSimilarity', 'Cosine Similarity'),
#     ]
#     parameterCNN_Loss = forms.ChoiceField(choices=LOSS_CHOICES,
#                             widget=forms.RadioSelect(attrs={'class': 'with-gap','name':'group_los'}))
#
#     OPTIMIZER_CHOICES = [
#         ('SGD', 'SGD'),
#         ('RMSprop', 'RMSprop'),
#         ('Adadelta', 'Adadelta'),
#         ('Adam', 'Adam'),
#         ('Adamax', 'Adamax'),
#         ('Nadam', 'Nadam'),
#     ]
#     parameterCNN_Optimizer = forms.ChoiceField(choices=OPTIMIZER_CHOICES,
#                             widget=forms.RadioSelect(attrs={'class': 'with-gap','name':'group_optimizer'}))
#
#     class Meta:
#         model = Machine
#         exclude = ('name', 'team', 'desc', 'analysis_source_columns',
#                 'analysissource_columnnameinput', 'analysissource_columnnameoutput',
#                 'analysissource_columntype', 'analysissource_columnnameignore',
#                 'analysissource_errors', 'analysissource_warnings', 'data_columnsInputFilterLines',
#                 'LineInput_ID' ,'is_public', 'datasource_is_public', 'datasource_sample_only_public',
#                 'datasource_is_private', 'created_by','datetimecreation',
#                 'brain_id_original', 'datausage', 'brain_is_duplicatable', 'brain_copy_costUSD',
#                 'brain_is_exportable', 'brain_export_costUSD', 'api_resolving_is_public',
#                 'api_resolving_priceUSD', 'column_description', 'solving_accuracy',
#                 'solving_loss', 'solving_brain_model', 'solving_datetime_brain_model',
#                 'solving_path_log_tensorboard', 'solving_training_epoch_count',)
