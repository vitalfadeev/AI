# Generated by Django 2.2.4 on 2019-12-06 15:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('machine', '0001_initial'),
        ('consulting', '0002_message_recipient_machine_id'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('team', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='Recipient_User_ID',
            field=models.ForeignKey(blank=True, help_text='Optional (only one destination simultanousely) _ Message sent to this user (only if it is sent to an user)', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Recipient_User_ID', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='message',
            name='User_ID',
            field=models.ForeignKey(help_text='Message sent by this user', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='consultingrequest',
            name='Consultant_User_ID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Consultant_User_ID', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='consultingrequest',
            name='Machine_ID',
            field=models.ForeignKey(blank=True, help_text='link to the machine or null if the request is not related to a machine', null=True, on_delete=django.db.models.deletion.CASCADE, to='machine.Machine'),
        ),
        migrations.AddField(
            model_name='consultingrequest',
            name='Team_ID',
            field=models.ForeignKey(help_text='Team of the ConsultingRequest or null if there is no team', on_delete=django.db.models.deletion.CASCADE, to='team.Team'),
        ),
        migrations.AddField(
            model_name='consultingrequest',
            name='User_ID',
            field=models.ForeignKey(help_text='creator of the ConsultingRequest', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='consultantapplication',
            name='ConsultingRequest_ID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='consulting.ConsultingRequest'),
        ),
        migrations.AddField(
            model_name='consultantapplication',
            name='User_ID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
