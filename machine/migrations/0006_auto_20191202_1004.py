# Generated by Django 2.2.4 on 2019-12-02 10:04

from django.db import migrations, models
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ('machine', '0005_auto_20191128_1551'),
    ]

    operations = [
        migrations.AddField(
            model_name='machine',
            name='Training_FileTensorBoardLog',
            field=models.BinaryField(null=True),
        ),
        migrations.AlterField(
            model_name='machine',
            name='AnalysisSource_Errors',
            field=django_mysql.models.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name='machine',
            name='AnalysisSource_Warnings',
            field=django_mysql.models.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name='machine',
            name='ParameterCNN_Shape',
            field=models.CharField(blank=True, default='[]', max_length=400, null=True, verbose_name='Shape'),
        ),
    ]