from django import forms
from django.forms import ModelForm
from machine.models import Machine


class MachineForm(ModelForm):
    is_public = forms.BooleanField()
    datasource_is_public = forms.BooleanField()
    datasource_sample_only_public = forms.BooleanField()
    datasource_is_private = forms.BooleanField()

    is_public = forms.BooleanField(required=False)
    datasource_is_public = forms.BooleanField(required=False)
    datasource_sample_only_public = forms.BooleanField(required=False)
    datasource_is_private = forms.BooleanField(required=False)

    desc = forms.CharField(widget=forms.Textarea(attrs={'class': 'materialize-textarea i-textarea-5'}))

    class Meta:
        model = Machine
        exclude = ('analysis_source_columns',
        'analysissource_columnnameinput', 'analysissource_columnnameoutput',
        'analysissource_columntype','analysissource_columnnameignore',
        'analysissource_errors', 'analysissource_warnings', 'data_columnsInputFilterLines',
        'parameterCNN_ShapeAuto', 'parameterCNN_Loss', 'LineInput_ID' ,
        'parameterCNN_Optimizer', 'parameterCNN_Shape',
        'parameterCNN_BatchEpochAuto', 'parameterCNN_BatchSize',
        'parameterCNN_Epoch', 'created_by', 'datetimecreation',
        'brain_id_original', 'datausage', 'brain_is_duplicatable', 'brain_copy_costUSD',
        'brain_is_exportable', 'brain_export_costUSD', 'api_resolving_is_public',
        'api_resolving_priceUSD', 'column_description', 'solving_accuracy',
        'solving_loss', 'solving_brain_model', 'solving_datetime_brain_model', 
        'solving_path_log_tensorboard', 'solving_training_epoch_count',)


class ParameterForm(ModelForm):
    LOSS_CHOICES = [
        ('BinaryCrossentropy', 'Binary Crossentropy'),
        ('SquaredHinge', 'Squared Hinge'),
        ('Poisson', 'Poisson'),
        ('MeanSquaredError', 'Mean Squared Error'),
        ('MeanAbsoluteError', 'Mean Absolute Error'),
        ('Huber', 'Huber'),
        ('Hinge', 'Hinge'),
        ('CosineSimilarity', 'Cosine Similarity'),
    ]
    parameterCNN_Loss = forms.ChoiceField(choices=LOSS_CHOICES,
                            widget=forms.RadioSelect(attrs={'class': 'with-gap','name':'group_los'}))

    OPTIMIZER_CHOICES = [
        ('SGD', 'SGD'),
        ('RMSprop', 'RMSprop'),
        ('Adadelta', 'Adadelta'),
        ('Adam', 'Adam'),
        ('Adamax', 'Adamax'),
        ('Nadam', 'Nadam'),
    ]
    parameterCNN_Optimizer = forms.ChoiceField(choices=OPTIMIZER_CHOICES,
                            widget=forms.RadioSelect(attrs={'class': 'with-gap','name':'group_optimizer'}))

    class Meta:
        model = Machine
        exclude = ('name', 'team', 'desc', 'analysis_source_columns',
                'analysissource_columnnameinput', 'analysissource_columnnameoutput',
                'analysissource_columntype', 'analysissource_columnnameignore',
                'analysissource_errors', 'analysissource_warnings', 'data_columnsInputFilterLines',
                'LineInput_ID' ,'is_public', 'datasource_is_public', 'datasource_sample_only_public',
                'datasource_is_private', 'created_by','datetimecreation',
                'brain_id_original', 'datausage', 'brain_is_duplicatable', 'brain_copy_costUSD',
                'brain_is_exportable', 'brain_export_costUSD', 'api_resolving_is_public',
                'api_resolving_priceUSD', 'column_description', 'solving_accuracy',
                'solving_loss', 'solving_brain_model', 'solving_datetime_brain_model', 
                'solving_path_log_tensorboard', 'solving_training_epoch_count',)
