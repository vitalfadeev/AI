# Generated by Django 2.2.4 on 2019-12-06 15:32

from django.db import migrations, models
import django_mysql.models
import machine.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('Machine_ID', models.AutoField(help_text='Generated auto', primary_key=True, serialize=False)),
                ('DateTimeCreation', models.DateTimeField(auto_now_add=True)),
                ('Project_Name', models.CharField(blank=True, help_text='One line entered by user owner', max_length=200, verbose_name='Name')),
                ('Project_Description', models.TextField(blank=True, help_text='Several lines entered by user owner', verbose_name='Description')),
                ('Project_DataUsage', models.TextField(blank=True, help_text='Description how to use Machine, data explaination, API usage, etc…', verbose_name='DataUsage')),
                ('input_file', models.FileField(null=True, upload_to=machine.models.get_upload_path, verbose_name='file')),
                ('Project_DataSourceIsPublic', models.BooleanField(default=False, help_text='It is possible to view and download All Source data')),
                ('Project_DataSourceSampleOnlyPublic', models.BooleanField(default=False, help_text='It is possible to view only first 25 lines of Source data and download only 25 first lines of Source data - it is possible to buy full data set (download) ')),
                ('Project_DataSource_PriceUSD', models.BooleanField(default=False, help_text='If price is paid then the dataset is available for download')),
                ('Project_DataSourceIsPrivate', models.BooleanField(default=False, help_text='It is not possible to view source data or to download source data')),
                ('Project_APISolving_IsPublic', models.BooleanField(default=False, help_text='Allow everyone to request solving to the API _ Machine Owner receive credits')),
                ('Project_APISolving_PriceUSD', models.DecimalField(blank=True, decimal_places=3, help_text='Price asked by Owner for each line solved', max_digits=12, null=True)),
                ('Project_MachineIsDuplicatable', models.BooleanField(default=False, help_text='Allow or not to copy the Machine model')),
                ('Project_MachineCopyCostUSD', models.DecimalField(blank=True, decimal_places=3, help_text='Cost asked by owner for the duplication', max_digits=12, null=True)),
                ('Project_MachineCopyUpdateCostUSD', models.DecimalField(blank=True, decimal_places=3, help_text='Cost asked by owner for updating the duplicate', max_digits=12, null=True)),
                ('Project_MachineIsExportable', models.BooleanField(default=False, help_text='Allow or not to export the Machine model in Python code')),
                ('Project_MachineExportCostUSD', models.DecimalField(blank=True, decimal_places=3, help_text='Cost asked by owner for exporting to python', max_digits=12, null=True)),
                ('Project_ColumnsDescription', django_mysql.models.JSONField(blank=True, default=list, help_text='possibility to put some special keywords : (  __Keep_Only_Values__) (__ONLY_LINES_WITH_OPTIONS__  : list of values) ')),
                ('AnalysisSource_ColumnsNameInput', django_mysql.models.JSONField(blank=True, default=dict)),
                ('AnalysisSource_ColumnsNameOutput', django_mysql.models.JSONField(blank=True, default=dict)),
                ('AnalysisSource_ColumnType', django_mysql.models.JSONField(default=dict, help_text='ColumnType[] : [EMPTY, Numerical, Date, Tags, boolean, Options,DateTime,Time] ')),
                ('AnalysisSource_Errors', django_mysql.models.JSONField(blank=True, default=dict, help_text='TextError : Errors ')),
                ('AnalysisSource_Warnings', django_mysql.models.JSONField(blank=True, default=dict, help_text='TextWarning: warning')),
                ('AnalysisSource_ColumnsMissingPercentage', django_mysql.models.JSONField(default=dict, help_text='Indicate percentage of missing values in the column (for training line)')),
                ('AnalysisSource_ListMaxSize', django_mysql.models.JSONField(default=dict, help_text='For JSON columns it indicate the maximum count of values // for Text-Words and Text-Sentence Text-Paragraphs datatype, it indicate the maximum count of Words // for JSON_Array_Of_Array it indicate the listmaxsize of 2 axes')),
                ('Machine_IsDataMissingTolerant', models.BooleanField(default=False)),
                ('Machine_IsLevelTrainingNormal', models.BooleanField(default=False)),
                ('Machine_IsLevelTrainingMaximum', models.BooleanField(default=False)),
                ('Machine_IsMultipleMachine', models.BooleanField(default=False)),
                ('Machine_IsReRunTraining', models.BooleanField(default=False, help_text='If 1 WorkProcessor will start Training')),
                ('Machine_IsToRunAFP', models.BooleanField(default=False, help_text='If 1 WorkProcessor will start AFP ')),
                ('Machine_IsToRunARUC', models.BooleanField(default=False, help_text='If 1 WorkProcessor will do ARUC after trainning   (ARUC = Auto Remove Useless Columns)')),
                ('Machine_IsModeLSTM', models.BooleanField(default=False, help_text='If 1 model with have one or more LSTM layer')),
                ('Machine_IsModeRNN', models.BooleanField(default=False, help_text='If 1 model with have only DENSE layer and no LSTM layer')),
                ('MultipleMachine_IsFront', models.BooleanField(default=False, help_text='True if the Machine is Front of MultipleMachine')),
                ('MultipleMachine_IsAgregator', models.BooleanField(default=False, help_text='True if the Machine is agregator of MultipleMachine')),
                ('MultipleMachine_IsElement', models.BooleanField(default=False, help_text='True if the Machine is elelement of MultipleMachine')),
                ('EncDec_ColumnsInNumericMode', django_mysql.models.JSONField(default=dict, help_text='By default  (AnalysisSource_ColumnsNameInput)=true and AnalysisSource_ColumnsNameOutput=false  --- (AnalysisSource_ColumnsNameOutput cannot be both numeric and multiplexed)')),
                ('EncDec_ColumnsInMultiplexedMode', django_mysql.models.JSONField(default=dict, help_text='By default  (AnalysisSource_ColumnsNameInput)=true and AnalysisSource_ColumnsNameOutput=true --- (AnalysisSource_ColumnsNameOutput cannot be both numeric and multiplexed)')),
                ('EncDec_ColumnsFLOATFrequ3Mode', django_mysql.models.JSONField(default=dict, help_text='Create 3 columns Rare/Occasional/Normal for FLOAT columns')),
                ('EncDec_ColumnsFloatMostFrequMode', django_mysql.models.JSONField(default=dict, help_text='for FLOAT columns will Create 10 columns boolean for the 10 most frequents FLOAT values ')),
                ('EncDec_ColumnsInputInformations', models.BinaryField(help_text='Note : contains : InfoForEncodeDecodeColumns', null=True)),
                ('EncDec_ColumnsOutputInformations', models.BinaryField(help_text='Note : contains : InfoForDecodeOutputColumns', null=True)),
                ('EncDec_ColumnsInputEncodedCount', models.IntegerField(help_text='Count of encoded inputs columns ', null=True)),
                ('EncDec_ColumnsOutputEncodedCount', models.IntegerField(help_text='Count of encoded output columns ', null=True)),
                ('EncDec_ColumnsMissingPercentage', django_mysql.models.JSONField(default=dict, help_text='Indicate percentage of missing values in the column (for training line)')),
                ('EncDec_Errors', django_mysql.models.JSONField(default=dict, help_text='Dict of ColumnSourceName(not encoded column name) contains one string with all warnings')),
                ('EncDec_Warnings', django_mysql.models.JSONField(default=dict, help_text='Dict of ColumnSourceName(not encoded column name) contains one string with all errors')),
                ('ParameterCNN_ShapeAuto', models.BooleanField(default=True)),
                ('ParameterCNN_Loss', models.CharField(blank=True, max_length=100, null=True, verbose_name='Loss')),
                ('ParameterCNN_Optimizer', models.CharField(blank=True, max_length=150, null=True, verbose_name='Optimizer')),
                ('ParameterCNN_Shape', django_mysql.models.JSONField(default=list, help_text='One string contains json array[10] of array[4]')),
                ('ParameterCNN_BatchEpochAuto', models.BooleanField(default=True, verbose_name='Batch Epoch Auto')),
                ('ParameterCNN_BatchSize', models.PositiveIntegerField(blank=True, default=1, help_text='user can set this value manually, they will be used only if ParameterCNN_BatchEpochAuto=0', null=True, verbose_name='Batch Size')),
                ('ParameterCNN_Epoch', models.PositiveIntegerField(blank=True, default=1, help_text='user can set this value manually, they will be used only if ParameterCNN_BatchEpochAuto=0', null=True, verbose_name='Epoch')),
                ('Training_AcuracyAverage', models.DecimalField(decimal_places=3, help_text='Average of acuracy of all columns', max_digits=12, null=True)),
                ('Training_LossAverage', models.DecimalField(decimal_places=3, help_text='Average of loss of all columns', max_digits=12, null=True)),
                ('Training_MachineModel', models.BinaryField(blank=True, help_text='to save now in SQL the model ', null=True)),
                ('Training_MachineWeights', models.BinaryField(blank=True, help_text='to save now in SQL the weight', null=True)),
                ('Training_FindParametersDelaySec', models.DecimalField(blank=True, decimal_places=3, max_digits=6, null=True)),
                ('Training_TrainingTotalDelaySec', models.DecimalField(blank=True, decimal_places=3, help_text='Total training time  ', max_digits=6, null=True)),
                ('Training_TrainingCellDelaySec', models.DecimalField(blank=True, decimal_places=3, help_text='Total training time / ( LEN( AnalysisSource_ColumnsNameInput ) + LEN( AnalysisSource_ColumnsNameOutput ) ) / Training_TotalTrainingLineCount', max_digits=6, null=True)),
                ('Training_DateTimeMachineModel', models.DateTimeField(help_text='DateTime of last update of this Machine model (updated after each training)', null=True)),
                ('Training_FileTensorBoardLog', models.BinaryField(null=True)),
                ('Training_TrainingEpochCount', models.IntegerField(help_text='How many Epoch was done for training', null=True)),
                ('Training_TrainingBatchSize', models.IntegerField(help_text='what was the batch size used during training', null=True)),
                ('Training_TotalTrainingLineCount', models.IntegerField(help_text='How many line was in the training data', null=True)),
                ('Training_TypeMachineHardware', models.TextField(help_text="Type of hardware like 'I9700_GTX1060'", null=True)),
                ('Training_DecisionTreeImage', models.BinaryField(help_text='Image file PNG of the decision tree of the DatInput', null=True)),
                ('TrainingEval_LossSampleTraining', models.DecimalField(decimal_places=3, help_text='loss on training lines', max_digits=12, null=True)),
                ('TrainingEval_LossSampleEvaluation', models.DecimalField(decimal_places=3, help_text='loss on evaluation lines', max_digits=12, null=True)),
                ('TrainingEval_LossSampleTrainingNoise', models.DecimalField(decimal_places=3, help_text='loss on training when we add 5% noise ', max_digits=12, null=True)),
                ('TrainingEval_LossSampleEvaluationNoise', models.DecimalField(decimal_places=3, help_text='loss on evaluation when we add 5% noise ', max_digits=12, null=True)),
                ('TrainingEval_AcuracySampleTraining', models.DecimalField(decimal_places=3, help_text='acuracy on training lines', max_digits=12, null=True)),
                ('TrainingEval_AcuracySampleEvaluation', models.DecimalField(decimal_places=3, help_text='acuracy on evaluation lines', max_digits=12, null=True)),
                ('TrainingEval_AcuracySampleTrainingNoise', models.DecimalField(decimal_places=3, help_text='acuracy on training when we add 5% noise ', max_digits=12, null=True)),
                ('TrainingEval_AcuracySampleEvaluationNoise', models.DecimalField(decimal_places=3, help_text='acuracy on evaluation when we add 5% noise', max_digits=12, null=True)),
            ],
            options={
                'verbose_name': 'Machine',
                'verbose_name_plural': 'Machines',
                'db_table': 'Machine',
            },
            bases=(models.Model, machine.models.MachineMixin),
        ),
        migrations.CreateModel(
            name='MachineMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(verbose_name='Message')),
                ('message_file', models.FileField(blank=True, null=True, upload_to='machinemessage/%Y-%m-%d/%H-%M', verbose_name='file')),
            ],
            options={
                'verbose_name': 'Machine Message',
                'verbose_name_plural': 'Machine Message',
            },
        ),
    ]
