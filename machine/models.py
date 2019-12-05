import json
import os

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from machine.dynamic_model.dymo import DynamicModel, DymoMixin
from team.models import Team
from django_mysql.models import JSONField


class MachineMixin:
    # in_out_ignore.name1=IN -> AnalysisSource_ColumnsNameInput += [name1]
    # in_out_ignore.name2=OUT -> AnalysisSource_ColumnsNameOutput += [name2]
    # in_out_ignore.name3=IGN -> AnalysisSource_ColumnsNameOutput -= [name3]
    #                            AnalysisSource_ColumnsNameInput -= [name3]
    @property
    def in_out_ignore( self ):
        """ Read AnalysisSource_ColumnsNameInput, AnalysisSource_ColumnsNameOutput
            return in_out_ignore = {
                in_out_ignore.name1: IN,
                in_out_ignore.name2: OUT,
                in_out_ignore.name2: IGN
            } """
        ins = dict.fromkeys( self.AnalysisSource_ColumnsNameInput, "IN" )
        outs = dict.fromkeys( self.AnalysisSource_ColumnsNameOutput, "OUT" )
        ignores = { name:"IGN" for name in self.AnalysisSource_ColumnType if name not in ins and name not in outs }

        # return DotSeparatedNameDict( "in_out_ignore", dict( **ins, **outs, **ignores ) )
        return dict( **ins, **outs, **ignores )

    @in_out_ignore.setter
    def in_out_ignore( self, value ):
        """ value:
                value = {
                    in_out_ignore.name1: IN,
                    in_out_ignore.name2: OUT,
                    in_out_ignore.name3: IGN
                }

                Save into properties: AnalysisSource_ColumnsNameInput, AnalysisSource_ColumnsNameOutput
        """
        ins = []
        outs = []

        for name, v in value:
            if v == "IN":
                ins.append( name )
            elif v == "OUT":
                outs.append( name )

        self.AnalysisSource_ColumnsNameInput = ins
        self.AnalysisSource_ColumnsNameOutput = outs

    @property
    def input_columns_names( self ):
        """ Read AnalysisSource_ColumnType
            return [name1, anme2, name3]
            } """
        return list( self.AnalysisSource_ColumnType.keys() )



type_mapping = {
    "OPTION"               : (models.TextField, {}),
    "NUMERIC"              : (models.TextField, {}),
    "FLOAT"                : (models.TextField, {}),
    "TAGS"                 : (models.TextField, {}),
    "TAGS_WEIGHT"          : (models.TextField, {}),
    "LABEL"                : (models.TextField, {}),
    "LABEL_LARGE"          : (models.TextField, {}),
    "TEXT"                 : (models.TextField, {}),
    "TEXT_WORDS_PKN_SMALL" : (models.TextField, {}),
    "TEXT_WORDS_PKN_LARGE" : (models.TextField, {}),
    "TEXT_SENTENCE"        : (models.TextField, {}),
    "TEXT_PARAGRAPH"       : (models.TextField, {}),
    "DATE"                 : (models.TextField, {}),
    "DATE_LARGE"           : (models.TextField, {}),
    "TIME"                 : (models.TextField, {}),
    "DATETIME"             : (models.TextField, {}),
    "DATETIME_LARGE"       : (models.TextField, {}),
    "JSON"                 : (models.TextField, {}),
    "EMPTY"                : (models.TextField, {}),
}
# type_mapping = {
#     "OPTION"               : (models.CharField, {"max_length":400}),
#     "NUMERIC"              : (models.DecimalField, {"max_digits":12, "decimal_places":3}),
#     "FLOAT"                : (models.DecimalField, {"max_digits":12, "decimal_places":3}),
#     "TAGS"                 : (models.CharField, {"max_length":400}),
#     "TAGS_WEIGHT"          : (models.CharField, {"max_length":400}),
#     "LABEL"                : (models.CharField, {"max_length":400}),
#     "LABEL_LARGE"          : (models.CharField, {"max_length":400}),
#     "TEXT"                 : (models.TextField, {}),
#     "TEXT_WORDS_PKN_SMALL" : (models.TextField, {}),
#     "TEXT_WORDS_PKN_LARGE" : (models.TextField, {}),
#     "TEXT_SENTENCE"        : (models.TextField, {}),
#     "TEXT_PARAGRAPH"       : (models.TextField, {}),
#     "DATE"                 : (models.DateField, {}),
#     "DATE_LARGE"           : (models.DateField, {}),
#     "TIME"                 : (models.TimeField, {}),
#     "DATETIME"             : (models.DateTimeField, {}),
#     "DATETIME_LARGE"       : (models.DateTimeField, {}),
#     "JSON"                 : (JSONField, {}),
#     "EMPTY"                : (models.CharField, {"max_length":400}),
# }


def _get_fields( columns, types ):
    fields = {}

    for column in columns:
        (field_callable, field_args) = type_mapping[ types[ column ] ]
        fields[ column ] = field_callable( **field_args )

    return fields


def MachineDataInputLinesModelFactory( machine_id, columns: list, types: dict, additional_columns: dict ):

    fields = _get_fields( columns, types )
    fields.update( additional_columns )

    cls = DynamicModel( (models.Model, DymoMixin),
                         f"Machine_{machine_id}_DataInputLines",
                         table=f"Machine_{machine_id}_DataInputLines",
                         fields=fields,
                         app_label="machine",
                         module_name="",
                         primary_key_column="LineInput_ID",
                         db_scheme="MachineData")

    cls._meta.Machine_ID = machine_id

    return cls


def MachineDataOutputLinesModelFactory( machine_id, columns: list, types: dict, additional_columns: dict ):
    cls = DynamicModel( (models.Model, DymoMixin),
                         f"Machine_{machine_id}_DataOutputLines",
                         table=f"Machine_{machine_id}_DataOutputLines",
                         fields=[],
                         app_label="machine",
                         module_name="",
                         primary_key_column="LineInput_ID",
                         db_scheme="MachineData" )

    cls._meta.Machine_ID = machine_id

    return cls


def get_upload_path( instance, filename ):
    """'machine/{user_id}/{YYYY-MM-DD}/{timestamp}/filename.ext' """
    return os.path.join(
        "machine",
        str(instance.Machine_ID),
        instance.DateTimeCreation.strftime("%Y-%m-%d"),
        str(instance.DateTimeCreation.timestamp()),
        filename
    )


class Machine(models.Model, MachineMixin):
    Machine_ID                                  =  models.AutoField(primary_key=True, help_text="Generated auto")
    DateTimeCreation                            =  models.DateTimeField(auto_now_add=True)
    Machine_ID_Original                         =  models.IntegerField(null=True, help_text="If this machine is a copy of another machine, then this is the source machine ID")

    Owner_User_ID                               =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('User'), help_text="Owner of this machine")
    Owner_Team_ID                               =  models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('Team'), help_text="Team_ID owner ")

    Project_Name                                =  models.CharField(_('Name'), max_length=200, blank=True, help_text="One line entered by user owner")
    Project_Description                         =  models.TextField(_('Description'), blank=True, help_text="Several lines entered by user owner")
    Project_DataUsage                           =  models.TextField(_('DataUsage'), null=False, blank=True, help_text="Description how to use Machine, data explaination, API usage, etc…")

    input_file                                  =  models.FileField(_('file'), upload_to=get_upload_path, null=True )

    Project_DataSourceIsPublic                  =  models.BooleanField(default=False, help_text="It is possible to view and download All Source data")
    Project_DataSourceSampleOnlyPublic          =  models.BooleanField(default=False, help_text="It is possible to view only first 25 lines of Source data and download only 25 first lines of Source data - it is possible to buy full data set (download) ")
    Project_DataSource_PriceUSD                 =  models.BooleanField(default=False, help_text="If price is paid then the dataset is available for download")
    Project_DataSourceIsPrivate                 =  models.BooleanField(default=False, help_text="It is not possible to view source data or to download source data")

    Project_APISolving_IsPublic                 =  models.BooleanField(default=False)
    Project_APISolving_PriceUSD                 =  models.DecimalField(null=True, blank=True, max_digits=12, decimal_places=3)

    Project_MachineIsDuplicatable               =  models.BooleanField(default=False)
    Project_MachineCopyCostUSD                  =  models.DecimalField(null=True, blank=True, max_digits=12, decimal_places=3)
    Project_MachineCopyUpdateCostUSD            =  models.DecimalField(null=True, blank=True, max_digits=12, decimal_places=3)

    Project_MachineIsExportable                 =  models.BooleanField(default=False)
    Project_MachineExportCostUSD                =  models.DecimalField (null=True, blank=True, max_digits=12, decimal_places=3)

    Project_ColumnsDescription                  =  JSONField(default=dict, blank=True)

    AnalysisSource_ColumnsNameInput             =  JSONField(default=dict, blank=True)
    AnalysisSource_ColumnsNameOutput            =  JSONField(default=dict, blank=True)
    AnalysisSource_ColumnType                   =  JSONField(default=dict)
    AnalysisSource_Errors                       =  JSONField(default=dict, blank=True)
    AnalysisSource_Warnings                     =  JSONField(default=dict, blank=True)
    AnalysisSource_ColumnsMissingPercentage     =  JSONField(default=dict)
    AnalysisSource_ListMaxSize                  =  JSONField(default=dict)

    Machine_IsDataMissingTolerant               =  models.BooleanField(default=False)
    Machine_IsLevelTrainingNormal               =  models.BooleanField(default=False)
    Machine_IsLevelTrainingMaximum              =  models.BooleanField(default=False)
    Machine_IsMultipleMachine                   =  models.BooleanField(default=False)
    Machine_IsReRunTraining                     =  models.BooleanField(default=False)
    Machine_IsToRunAFP                          =  models.BooleanField(default=False)
    Machine_IsToRunARUC                         =  models.BooleanField(default=False)
    Machine_IsModeLSTM                          =  models.BooleanField(default=False)
    Machine_IsModeRNN                           =  models.BooleanField(default=False)

    MultipleMachine_IsFront                     =  models.BooleanField(default=False)
    MultipleMachine_IsAgregator                 =  models.BooleanField(default=False)
    MultipleMachine_IsElement                   =  models.BooleanField(default=False)

    MultipleMachine_Front_Machine_ID            = models.OneToOneField( 'Machine', related_name='MachinesFront', on_delete=models.CASCADE, blank=True, null=True )
    MultipleMachine_Aggregator_Machine_ID       = models.OneToOneField( 'Machine', related_name='MachineAggregator',  on_delete=models.CASCADE, blank=True, null=True )
    MultipleMachine_Elements_Machine_ID         = models.ManyToManyField( 'Machine', related_name='Machines', blank=True )

    EncDec_ColumnsInNumericMode                 =  JSONField(default=dict)
    EncDec_ColumnsInMultiplexedMode             =  JSONField(default=dict)
    EncDec_ColumnsFLOATFrequ3Mode               =  JSONField(default=dict)
    EncDec_ColumnsFloatMostFrequMode            =  models.BinaryField(null=True)
    EncDec_ColumnsOutputInformations            =  models.BinaryField(null=True)
    EncDec_ColumnsInputEncodedCount             =  models.IntegerField(null=True)
    EncDec_ColumnsOutputEncodedCount            =  models.IntegerField(null=True)
    EncDec_ColumnsMissingPercentage             =  models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    EncDec_Errors                               =  JSONField( default=dict )
    EncDec_Warnings                             =  JSONField( default=dict )

    ParameterCNN_ShapeAuto                      = models.BooleanField(default=True)

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
    ParameterCNN_Loss               = models.CharField(_('Loss'),
                                        choices=LOSS_CHOICES, max_length=50,
                                        default='BinaryCrossentropy',
                                        null=True, blank=True)
    OPTIMIZER_CHOICES = [
        ('SGD', 'SGD'),
        ('RMSprop', 'RMSprop'),
        ('Adadelta', 'Adadelta'),
        ('Adam', 'Adam'),
        ('Adamax', 'Adamax'),
        ('Nadam', 'Nadam'),
    ]
    ParameterCNN_Optimizer          = models.CharField(_('Optimizer'),
                                        choices=OPTIMIZER_CHOICES, max_length=50,
                                        default='SGD', null=True, blank=True)

    SHAPE_CHOICES = [
        ('softmax', 'softmax'),
        ('elu', 'elu'),
        ('selu', 'selu'),
        ('softplus', 'softplus'),
        ('softsign', 'softsign'),
        ('relu', 'relu'),
        ('tanh', 'tanh'),
        ('hard_sigmoid', 'hard_sigmoid'),
        ('exponential', 'exponential'),
        ('linear', 'linear'),
        ('dropout','dropout'),
        ('batchnormalization','batchnormalization'),
    ]
    
    ParameterCNN_Shape                         =  models.CharField(_('Shape'), max_length=400, default=str([]), null=True, blank=True)

    ParameterCNN_BatchEpochAuto                =  models.BooleanField(_('Batch Epoch Auto'), default=True)
    ParameterCNN_BatchSize                     =  models.PositiveIntegerField(_('Batch Size'), default=1, null=True, blank=True)
    ParameterCNN_Epoch                         =  models.PositiveIntegerField(_('Epoch'), default=1, null=True, blank=True)

    Training_AcuracyAverage                    =  models.DecimalField(null=True, max_digits=12, decimal_places=3)
    Training_LossAverage                       =  models.DecimalField(null=True, max_digits=12, decimal_places=3)
    Training_MachineModel                      =  JSONField()
    Training_MachineWeights                    =  models.BinaryField(null=True, blank=True)
    Training_FindParametersDelaySec            =  models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    Training_TrainingTotalDelaySec             =  models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    Training_TrainingCellDelaySec              =  models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    Training_DateTimeMachineModel              =  models.DateTimeField(null=True)
    # Training_PathLogTensorBoard                =  models.CharField(max_length=400, null=True)
    Training_FileTensorBoardLog                =  models.BinaryField(null=True)
    Training_TrainingEpochCount                =  models.IntegerField(null=True)
    Training_TrainingBatchSize                 =  models.IntegerField(null=True)
    Training_TotalTrainingLineCount            =  models.IntegerField(null=True)
    Training_TypeMachineHardware               =  models.TextField(null=True)
    Training_DecisionTreeImage                 =  models.BinaryField(null=True)

    TrainingEval_LossSampleTraining            =  models.DecimalField(max_digits=12, decimal_places=3, null=True)
    TrainingEval_LossSampleEvaluation          =  models.DecimalField(max_digits=12, decimal_places=3, null=True)
    TrainingEval_LossSampleTrainingNoise       =  models.DecimalField(max_digits=12, decimal_places=3, null=True)
    TrainingEval_LossSampleEvaluationNoise     =  models.DecimalField(max_digits=12, decimal_places=3, null=True)
    TrainingEval_AcuracySampleTraining         =  models.DecimalField(max_digits=12, decimal_places=3, null=True)
    TrainingEval_AcuracySampleEvaluation       =  models.DecimalField(max_digits=12, decimal_places=3, null=True)
    TrainingEval_AcuracySampleTrainingNoise    =  models.DecimalField(max_digits=12, decimal_places=3, null=True)
    TrainingEval_AcuracySampleEvaluationNoise  =  models.DecimalField(max_digits=12, decimal_places=3, null=True)



    def get_machine_data_input_lines_columns( self, include_predefined=False ):
        columns = list( self.AnalysisSource_ColumnType.keys() )

        if include_predefined:
            columns.extend( self.get_machine_data_input_lines_predefined_columns() )

        return columns


    def get_machine_data_input_lines_predefined_columns( self ):
        predefined_columns = {
            "LineInput_ID"        : models.AutoField(primary_key=True),
            "IsForLearning"       : models.BooleanField(default=False),
            "IsForSolving"        : models.BooleanField(default=False),
            "IsWithMissingValues" : models.BooleanField(default=False),
            "IsForEvaluation"     : models.BooleanField(default=False),
            "IsLearned"           : models.BooleanField(default=False),
            "IsSolved"            : models.BooleanField(default=False),
        }
        return predefined_columns


    def get_machine_data_input_lines_model( self ):
        # return instance of the Machine_<Machine_ID>_DataInputLines
        # columns = list( self.analysissource_columnnameinput ) + list( self.analysissource_columnnameoutput )
        types = dict(self.AnalysisSource_ColumnType)

        columns = list(types.keys())

        predefined_columns = self.get_machine_data_input_lines_predefined_columns()

        return MachineDataInputLinesModelFactory( self.Machine_ID, columns, types, predefined_columns )


    def get_machine_data_output_lines_model( self ):
        # return instance of the Machine_<Machine_ID>_DataOutputLines
        # columns = list( self.analysissource_columnnameinput ) + list( self.analysissource_columnnameoutput )
        types = dict( self.AnalysisSource_ColumnType )
        columns = list(types.keys())
        additional_columns = {
            "LineOutput_ID"       : models.AutoField(primary_key=True),
            "Confidence"          : models.BooleanField(),
        }
        return MachineDataOutputLinesModelFactory( self.Machine_ID, columns, types, additional_columns )


    def get_machine_data_input_columns( self ):
        types = self.AnalysisSource_ColumnType
        return list( types.keys() )


    class Meta:
        db_table = 'Machine'
        verbose_name = _('Machine')
        verbose_name_plural = _('Machines')
        indexes = [
            models.Index(fields=['Machine_ID']),
            models.Index(fields=['DateTimeCreation']),
            models.Index(fields=['Owner_User_ID']),
            models.Index(fields=['Owner_Team_ID']),
        ]


    def __str__( self ):
        return f'{self.Project_Name} ({self.Machine_ID})'


class MachineMessage(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE,
                                verbose_name=_('machine'))
    message = models.TextField(_('Message'))
    message_file = models.FileField(_('file'), null=True, blank=True,
                                upload_to='machinemessage/%Y-%m-%d/%H-%M')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                        null=True, blank=True)

    def __str__(self):
        return self.message
    class Meta:
        verbose_name = _('Machine Message')
        verbose_name_plural = _('Machine Message')



@receiver(pre_save, sender=Machine)
def machine_pre_save( sender, instance, **kwargs ):
    """
    Analyze data-file

    :param sender:      Machine
    :param instance:    Machine instance
    :return:

    :see: https://docs.djangoproject.com/en/2.2/ref/signals/#pre-save
    """
    from machine.loader import django_loader

    # Load data on creation only
    if instance.pk is None:
        # Pre-analyze data and load
        url = instance.input_file.path
        file_handle = instance.input_file # because small file in memory.
        django_loader.prenanlyze( instance, url, file_handle )


@receiver(post_save, sender=Machine)
def machine_post_save( sender, instance, created=False, **kwargs ):
    """
    Create <Machine_<ID>_InputData table and load data

    :param sender:      Machine
    :param instance:    Machine instance
    :param created:     True - if creating,  False - if updating
    :return:

    :see: https://docs.djangoproject.com/en/2.2/ref/signals/#post-save
    """
    from machine.loader import django_loader

    # Load data on creation only
    if created:
        url = instance.input_file.path
        # Pre-analyze data and load
        django_loader.load( url, instance )

