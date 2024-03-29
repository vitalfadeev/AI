# Generated by Django 2.2.4 on 2019-12-06 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Graph',
            fields=[
                ('Graph_ID', models.AutoField(primary_key=True, serialize=False)),
                ('DateTimeCreation', models.DateTimeField(auto_now_add=True, help_text='To order the list of graph by most recent first')),
                ('GraphType', models.CharField(default='1', help_text='Type Of Graph', max_length=255)),
                ('ColorScaleSet', models.CharField(default='1', help_text='Name Of Color Set', max_length=255)),
                ('X', models.CharField(default='', help_text='The Column Name', max_length=255)),
                ('Y', models.CharField(default='', help_text='The Column Name', max_length=255)),
                ('Z', models.CharField(default='', help_text='The Column Name', max_length=255)),
                ('Color', models.CharField(default='', help_text='The Column Name', max_length=255)),
                ('Animation_Frame', models.CharField(default='', help_text='The Column Name', max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'Graph',
                'verbose_name_plural': 'Graphs',
                'db_table': 'Graph',
            },
        ),
    ]
