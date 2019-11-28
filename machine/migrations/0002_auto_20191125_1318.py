# Generated by Django 2.2.4 on 2019-11-25 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('machine', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machine',
            name='Machine_IsDataMissingTolerant',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='machine',
            name='Machine_IsLevelTrainingMaximum',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='machine',
            name='Machine_IsLevelTrainingNormal',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='machine',
            name='Machine_IsModeLSTM',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='machine',
            name='Machine_IsModeRNN',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='machine',
            name='Machine_IsMultipleMachine',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='machine',
            name='Machine_IsReRunTraining',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='machine',
            name='Machine_IsToRunAFP',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='machine',
            name='Machine_IsToRunARUC',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='machine',
            name='MultipleMachine_IsAgregator',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='machine',
            name='MultipleMachine_IsElement',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='machine',
            name='MultipleMachine_IsFront',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='machine',
            name='Project_APISolving_IsPublic',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='machine',
            name='Project_DataSourceIsPrivate',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='machine',
            name='Project_DataSourceIsPublic',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='machine',
            name='Project_DataSourceSampleOnlyPublic',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='machine',
            name='Project_DataSource_PriceUSD',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='machine',
            name='Project_MachineIsDuplicatable',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='machine',
            name='Project_MachineIsExportable',
            field=models.BooleanField(default=False),
        ),
    ]