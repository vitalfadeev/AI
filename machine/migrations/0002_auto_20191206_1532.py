# Generated by Django 2.2.4 on 2019-12-06 15:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('machine', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('team', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='machinemessage',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='machinemessage',
            name='machine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='machine.Machine', verbose_name='machine'),
        ),
        migrations.AddField(
            model_name='machine',
            name='Machine_ID_Original',
            field=models.ForeignKey(help_text='If this machine is a copy of another machine, then this is the source machine ID', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='OriginalChilds', to='machine.Machine'),
        ),
        migrations.AddField(
            model_name='machine',
            name='MultipleMachine_Aggregator_Machine_ID',
            field=models.ForeignKey(blank=True, help_text='Machine_ID of the Machine aggregator', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='AggregatorChilds', to='machine.Machine'),
        ),
        migrations.AddField(
            model_name='machine',
            name='MultipleMachine_Elements_Machine_ID',
            field=models.ManyToManyField(blank=True, help_text='List of Machine_ID of the Machine elements', related_name='_machine_MultipleMachine_Elements_Machine_ID_+', to='machine.Machine'),
        ),
        migrations.AddField(
            model_name='machine',
            name='MultipleMachine_Front_Machine_ID',
            field=models.ForeignKey(blank=True, help_text='Machine_ID of the Front Machine', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='FrontChilds', to='machine.Machine'),
        ),
        migrations.AddField(
            model_name='machine',
            name='Owner_Team_ID',
            field=models.ForeignKey(blank=True, help_text='Team_ID owner ', null=True, on_delete=django.db.models.deletion.CASCADE, to='team.Team', verbose_name='Team'),
        ),
        migrations.AddField(
            model_name='machine',
            name='Owner_User_ID',
            field=models.ForeignKey(help_text='Owner of this machine', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AddIndex(
            model_name='machine',
            index=models.Index(fields=['Machine_ID'], name='Machine_Machine_dd71c1_idx'),
        ),
        migrations.AddIndex(
            model_name='machine',
            index=models.Index(fields=['DateTimeCreation'], name='Machine_DateTim_817b12_idx'),
        ),
        migrations.AddIndex(
            model_name='machine',
            index=models.Index(fields=['Owner_User_ID'], name='Machine_Owner_U_29aa3d_idx'),
        ),
        migrations.AddIndex(
            model_name='machine',
            index=models.Index(fields=['Owner_Team_ID'], name='Machine_Owner_T_c241dc_idx'),
        ),
    ]
