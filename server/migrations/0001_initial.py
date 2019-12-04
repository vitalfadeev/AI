# Generated by Django 2.2.4 on 2019-12-03 16:17

from django.db import migrations, models
import jsonfield.fields


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
                ('ServerInfoDateTime', models.DateTimeField(auto_now=True)),
                ('ServerInfoReady', models.BooleanField(blank=True, null=True)),
                ('ServerTypeMachineHardware', jsonfield.fields.JSONField(default=[])),
            ],
            options={
                'db_table': 'Server',
            },
        ),
    ]
