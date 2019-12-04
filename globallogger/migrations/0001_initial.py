# Generated by Django 2.2.4 on 2019-12-03 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GlobalLogger',
            fields=[
                ('Log_ID', models.AutoField(primary_key=True, serialize=False)),
                ('Level', models.CharField(max_length=10)),
                ('DateTimeCreation', models.DateTimeField(auto_now=True)),
                ('TraceBack', models.TextField(blank=True)),
                ('MainModule', models.CharField(max_length=100)),
                ('MainFunction', models.CharField(max_length=100)),
                ('Message', models.TextField(blank=True)),
                ('HostName', models.CharField(max_length=45)),
                ('IP', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'GlobalLogger',
            },
        ),
    ]
