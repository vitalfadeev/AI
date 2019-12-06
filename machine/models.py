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
    Machine_ID_Original                         =  models.ForeignKey('self', related_name="OriginalChilds", on_delete=models.SET_NULL, null=True, help_text="If this machine is a copy of another machine, then this is the source machine ID")

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

    Project_APISolving_IsPublic                 =  models.BooleanField(default=False, help_text="Allow everyone to request solving to the API _ Machine Owner receive credits")
    Project_APISolving_PriceUSD                 =  models.DecimalField(null=True, blank=True, max_digits=12, decimal_places=3, help_text="Price asked by Owner for each line solved")

    Project_MachineIsDuplicatable               =  models.BooleanField(default=False, help_text="Allow or not to copy the Machine model")
    Project_MachineCopyCostUSD                  =  models.DecimalField(null=True, blank=True, max_digits=12, decimal_places=3, help_text="Cost asked by owner for the duplication")
    Project_MachineCopyUpdateCostUSD            =  models.DecimalField(null=True, blank=True, max_digits=12, decimal_places=3, help_text="Cost asked by owner for updating the duplicate")

    Project_MachineIsExportable                 =  models.BooleanField(default=False, help_text="Allow or not to export the Machine model in Python code")
    Project_MachineExportCostUSD                =  models.DecimalField (null=True, blank=True, max_digits=12, decimal_places=3, help_text="Cost asked by owner for exporting to python")

    Project_ColumnsDescription                  =  JSONField(default=list, blank=True, help_text="possibility to put some special keywords : (  __Keep_Only_Values__) (__ONLY_LINES_WITH_OPTIONS__  : list of values) ")

    AnalysisSource_ColumnsNameInput             =  JSONField(default=dict, blank=True)
    AnalysisSource_ColumnsNameOutput            =  JSONField(default=dict, blank=True)
    AnalysisSource_ColumnType                   =  JSONField(default=dict, help_text="ColumnType[] : [EMPTY, Numerical, Date, Tags, boolean, Options,DateTime,Time] ")
    AnalysisSource_Errors                       =  JSONField(default=dict, blank=True, help_text="TextError : Errors ")
    AnalysisSource_Warnings                     =  JSONField(default=dict, blank=True, help_text="TextWarning: warning")
    AnalysisSource_ColumnsMissingPercentage     =  JSONField(default=dict, help_text="Indicate percentage of missing values in the column (for training line)")
    AnalysisSource_ListMaxSize                  =  JSONField(default=dict, help_text="For JSON columns it indicate the maximum count of values // for Text-Words and Text-Sentence Text-Paragraphs datatype, it indicate the maximum count of Words // for JSON_Array_Of_Array it indicate the listmaxsize of 2 axes")

    Machine_IsDataMissingTolerant               =  models.BooleanField(default=False)
    Machine_IsLevelTrainingNormal               =  models.BooleanField(default=False)
    Machine_IsLevelTrainingMaximum              =  models.BooleanField(default=False)
    Machine_IsMultipleMachine                   =  models.BooleanField(default=False)
    Machine_IsReRunTraining                     =  models.BooleanField(default=False, help_text="If 1 WorkProcessor will start Training")
    Machine_IsToRunAFP                          =  models.BooleanField(default=False, help_text="If 1 WorkProcessor will start AFP ")
    Machine_IsToRunARUC                         =  models.BooleanField(default=False, help_text="If 1 WorkProcessor will do ARUC after trainning   (ARUC = Auto Remove Useless Columns)")
    Machine_IsModeLSTM                          =  models.BooleanField(default=False, help_text="If 1 model with have one or more LSTM layer")
    Machine_IsModeRNN                           =  models.BooleanField(default=False, help_text="If 1 model with have only DENSE layer and no LSTM layer")

    MultipleMachine_IsFront                     =  models.BooleanField(default=False, help_text="True if the Machine is Front of MultipleMachine")
    MultipleMachine_IsAgregator                 =  models.BooleanField(default=False, help_text="True if the Machine is agregator of MultipleMachine")
    MultipleMachine_IsElement                   =  models.BooleanField(default=False, help_text="True if the Machine is elelement of MultipleMachine")

    MultipleMachine_Front_Machine_ID            = models.ForeignKey( 'self', related_name="FrontChilds", on_delete=models.CASCADE, blank=True, null=True , help_text="Machine_ID of the Front Machine")
    MultipleMachine_Aggregator_Machine_ID       = models.ForeignKey( 'self', related_name="AggregatorChilds", on_delete=models.CASCADE, blank=True, null=True , help_text="Machine_ID of the Machine aggregator")
    MultipleMachine_Elements_Machine_ID         = models.ManyToManyField( 'self', related_name="Elements5Childs", blank=True , help_text="List of Machine_ID of the Machine elements")

    EncDec_ColumnsInNumericMode                 =  JSONField(default=dict, help_text="By default  (AnalysisSource_ColumnsNameInput)=true and AnalysisSource_ColumnsNameOutput=false  --- (AnalysisSource_ColumnsNameOutput cannot be both numeric and multiplexed)")
    EncDec_ColumnsInMultiplexedMode             =  JSONField(default=dict, help_text="By default  (AnalysisSource_ColumnsNameInput)=true and AnalysisSource_ColumnsNameOutput=true --- (AnalysisSource_ColumnsNameOutput cannot be both numeric and multiplexed)")
    EncDec_ColumnsFLOATFrequ3Mode               =  JSONField(default=dict, help_text="Create 3 columns Rare/Occasional/Normal for FLOAT columns")
    EncDec_ColumnsFloatMostFrequMode            =  JSONField(default=dict, help_text="for FLOAT columns will Create 10 columns boolean for the 10 most frequents FLOAT values ")
    EncDec_ColumnsInputInformations             =  models.BinaryField(null=True, help_text="Note : contains : InfoForEncodeDecodeColumns")
    EncDec_ColumnsOutputInformations            =  models.BinaryField(null=True, help_text="Note : contains : InfoForDecodeOutputColumns")
    EncDec_ColumnsInputEncodedCount             =  models.IntegerField(null=True, help_text="Count of encoded inputs columns ")
    EncDec_ColumnsOutputEncodedCount            =  models.IntegerField(null=True, help_text="Count of encoded output columns ")
    EncDec_ColumnsMissingPercentage             =  JSONField( default=dict, help_text="Indicate percentage of missing values in the column (for training line)")
    EncDec_Errors                               =  JSONField( default=dict, help_text="Dict of ColumnSourceName(not encoded column name) contains one string with all warnings" )
    EncDec_Warnings                             =  JSONField( default=dict, help_text="Dict of ColumnSourceName(not encoded column name) contains one string with all errors" )

    ParameterCNN_ShapeAuto                      = models.BooleanField(default=True)
    ParameterCNN_Loss                           = models.CharField(_('Loss'), max_length=100, null=True, blank=True)
    ParameterCNN_Optimizer                      = models.CharField(_('Optimizer'), max_length=150, null=True, blank=True)
    ParameterCNN_Shape                          =  JSONField( default=list, help_text="One string contains json array[10] of array[4]" )
    ParameterCNN_BatchEpochAuto                 =  models.BooleanField(_('Batch Epoch Auto'), default=True)
    ParameterCNN_BatchSize                      =  models.PositiveIntegerField(_('Batch Size'), default=1, null=True, blank=True, help_text="user can set this value manually, they will be used only if ParameterCNN_BatchEpochAuto=0")
    ParameterCNN_Epoch                          =  models.PositiveIntegerField(_('Epoch'), default=1, null=True, blank=True, help_text="user can set this value manually, they will be used only if ParameterCNN_BatchEpochAuto=0")

    Training_AcuracyAverage                    =  models.DecimalField(null=True, max_digits=12, decimal_places=3, help_text="Average of acuracy of all columns")
    Training_LossAverage                       =  models.DecimalField(null=True, max_digits=12, decimal_places=3, help_text="Average of loss of all columns")
    Training_MachineModel                      =  models.BinaryField(null=True, blank=True, help_text="to save now in SQL the model ")
    Training_MachineWeights                    =  models.BinaryField(null=True, blank=True, help_text="to save now in SQL the weight")
    Training_FindParametersDelaySec            =  models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)
    Training_TrainingTotalDelaySec             =  models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True, help_text="Total training time  ")
    Training_TrainingCellDelaySec              =  models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True, help_text="Total training time / ( LEN( AnalysisSource_ColumnsNameInput ) + LEN( AnalysisSource_ColumnsNameOutput ) ) / Training_TotalTrainingLineCount")
    Training_DateTimeMachineModel              =  models.DateTimeField(null=True, help_text="DateTime of last update of this Machine model (updated after each training)")
    Training_FileTensorBoardLog                =  models.BinaryField(null=True)
    Training_TrainingEpochCount                =  models.IntegerField(null=True, help_text="How many Epoch was done for training")
    Training_TrainingBatchSize                 =  models.IntegerField(null=True, help_text="what was the batch size used during training")
    Training_TotalTrainingLineCount            =  models.IntegerField(null=True, help_text="How many line was in the training data")
    Training_TypeMachineHardware               =  models.TextField(null=True, help_text="Type of hardware like 'I9700_GTX1060'")
    Training_DecisionTreeImage                 =  models.BinaryField(null=True, help_text="Image file PNG of the decision tree of the DatInput")

    TrainingEval_LossSampleTraining            =  models.DecimalField(max_digits=12, decimal_places=3, null=True, help_text="loss on training lines")
    TrainingEval_LossSampleEvaluation          =  models.DecimalField(max_digits=12, decimal_places=3, null=True, help_text="loss on evaluation lines")
    TrainingEval_LossSampleTrainingNoise       =  models.DecimalField(max_digits=12, decimal_places=3, null=True, help_text="loss on training when we add 5% noise ")
    TrainingEval_LossSampleEvaluationNoise     =  models.DecimalField(max_digits=12, decimal_places=3, null=True, help_text="loss on evaluation when we add 5% noise ")
    TrainingEval_AcuracySampleTraining         =  models.DecimalField(max_digits=12, decimal_places=3, null=True, help_text="acuracy on training lines")
    TrainingEval_AcuracySampleEvaluation       =  models.DecimalField(max_digits=12, decimal_places=3, null=True, help_text="acuracy on evaluation lines")
    TrainingEval_AcuracySampleTrainingNoise    =  models.DecimalField(max_digits=12, decimal_places=3, null=True, help_text="acuracy on training when we add 5% noise ")
    TrainingEval_AcuracySampleEvaluationNoise  =  models.DecimalField(max_digits=12, decimal_places=3, null=True, help_text="acuracy on evaluation when we add 5% noise")


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

