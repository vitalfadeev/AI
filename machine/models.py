from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from team.models import Team
from django_mysql.models import JSONField
from datetime import datetime

DEFAULT_MACHINE_ID = 1
DEFAULT_MACHINE_ORIGINAL_ID = 1

# Create your models here.
class Column(models.Model):
    COLUMN_TYPE_CHOICES = [
        ('IGN', 'Ignore'),
        ('IN', 'Input'),
        ('OUT', 'Output'),
    ]
    column_type = models.CharField(_('column type'), max_length=3,
                                    choices=COLUMN_TYPE_CHOICES)
    name = models.CharField(_('Name'), max_length=200)
    desc = models.TextField(_('Description'), null=True, blank=True)
    
    is_for_learning = models.NullBooleanField(_('Is For Learning'))
    is_for_solving = models.NullBooleanField(_('Is For Solving'))
    is_with_missing_values = models.NullBooleanField(_('Is With Missing Values'))
    is_for_evaluation = models.NullBooleanField(_('Is For Evaluation'))

    is_learned = models.NullBooleanField(_('Is Learned'))
    is_solved = models.NullBooleanField(_('Is Solved'))

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = _('Column')
        verbose_name_plural = _('Columns')


class Machine(models.Model):
    datetimecreation = models.DateTimeField(blank = True, db_column='DateTimeCreation',
                                            default=datetime.now)
    brain_id_original = models.ForeignKey("self",on_delete=models.CASCADE,
                                                 db_column='Brain_ID_Original',
                                                 default=DEFAULT_MACHINE_ORIGINAL_ID,null=True, blank=True)
    datausage = models.TextField(_('DataUsage'),null=False,blank=True,db_column='Project_DataUsage')

    name = models.CharField(_('Name'), max_length=200, db_column='Project_Name')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, 
                                verbose_name=_('team'),
                                null=True, blank=True,db_column='Group_ID')
    desc = models.TextField(_('Description'), db_column='Project_Description')
    analysis_source_columns = models.ManyToManyField(Column,
                    verbose_name=_('Analysis Source Columns'))

    is_public = models.NullBooleanField(db_column='Project_IsPublic')
    datasource_is_public = models.NullBooleanField(db_column='Project_DataSourceIsPublic')
    datasource_sample_only_public = models.NullBooleanField(db_column='Project_DataSourceSampleOnlyPublic')
    datasource_is_private = models.NullBooleanField(db_column='Project_DataSourceIsPrivate')
    
    brain_is_duplicatable = models.NullBooleanField(db_column='Project_BrainIsDuplicatable')
    brain_copy_costUSD = models.FloatField(null=True,blank=True, db_column='Project_BrainCopyCostUSD')
    brain_is_exportable = models.NullBooleanField(db_column='Project_BrainIsExportable')
    brain_export_costUSD = models.FloatField (null=True,blank=True, db_column='Project_BrainExportCostUSD')

    api_resolving_is_public = models.NullBooleanField(default=False,db_column='Project_APISolving_IsPublic')
    api_resolving_priceUSD = models.FloatField(null=True,blank=True,db_column='Project_APISolving_PriceUSD')
    
    column_description = JSONField(db_column='Project_ColumnsDescription')

    analysissource_columnnameinput = JSONField(db_column='AnalysisSource_ColumnsNameInput')
    analysissource_columnnameoutput = JSONField(db_column='AnalysisSource_ColumnsNameOutput')
    analysissource_columnnameignore = JSONField(db_column='AnalysisSource_ColumnsNameIgnore',
                                                default=dict)
    analysissource_columntype = JSONField(db_column='AnalysisSource_ColumnType')
    analysissource_errors = JSONField(db_column='AnalysisSource_Errors')
    analysissource_warnings = JSONField(db_column='AnalysisSource_Warnings')

    data_columnsInputFilterLines = JSONField(db_column='Data_ColumnsInputFilterLines')


    input_file = models.FileField(_('file'), upload_to='machine/%Y-%m-%d/%H-%M')

    parameterCNN_ShapeAuto = models.BooleanField(default=True)
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
    parameterCNN_Loss = models.CharField(_('Loss'),
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
    parameterCNN_Optimizer = models.CharField(_('Optimizer'),
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
    parameterCNN_Shape = models.CharField(_('Shape'),
                        choices=SHAPE_CHOICES, max_length=50,
                        default='softmax', null=True, blank=True)
    
    parameterCNN_BatchEpochAuto = models.BooleanField(_('Batch Epoch Auto'), default=True)
    parameterCNN_BatchSize = models.PositiveIntegerField(_('Batch Size'), default=1,
                                                        null=True, blank=True)
    parameterCNN_Epoch = models.PositiveIntegerField(_('Epoch'), default=1,
                                                        null=True, blank=True)

    solving_accuracy = JSONField(db_column='Solving_Acuracy')
    solving_loss = JSONField(db_column='Solving_Loss')
    solving_brain_model = JSONField(db_column='Solving_BrainModel')
    solving_datetime_brain_model = models.DateTimeField(blank=True,db_column='Solving_DateTimeBrainModel',
                                                        default=datetime.now)
    solving_path_log_tensorboard=models.TextField(blank=True,null=True,db_column='Solving_PathLogTensorBoard')
    solving_training_epoch_count=models.PositiveIntegerField(null=True,blank=True,db_column='Solving_TrainingEpochCount')
   
    modified_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(_('Received DateTime'),
                                        auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                        null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'brains'
        verbose_name = _('Machine')
        verbose_name_plural = _('Machines')


class MachineMessage(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE,
                                verbose_name=_('machine'))
    message = models.TextField(_('Message'))
    message_file = models.FileField(_('file'), null=True, blank=True,
                                upload_to='machinemessage/%Y-%m-%d/%H-%M')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                        null=True, blank=True)

    def __str__(self):
        return self.message
    class Meta:
        verbose_name = _('Machine Message')
        verbose_name_plural = _('Machine Message')
