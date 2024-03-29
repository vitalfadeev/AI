# Generated by Django 2.2.4 on 2019-12-06 15:32

from django.db import migrations, models
import django_mysql.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Server',
            fields=[
                ('Server_ID', models.AutoField(primary_key=True, serialize=False)),
                ('ServerName', models.CharField(max_length=50, unique=True)),
                ('ServerInfoDateTime', models.DateTimeField(auto_now_add=True, help_text='Date of creation')),
                ('ServerInfoReady', models.BooleanField(blank=True, help_text='=1 if ready or =0', null=True)),
                ('ServerTypeMachineHardware', django_mysql.models.JSONField(blank=True, default=list)),
            ],
            options={
                'db_table': 'Server',
            },
        ),
        migrations.AddIndex(
            model_name='server',
            index=models.Index(fields=['ServerName'], name='Server_ServerN_695435_idx'),
        ),
    ]
