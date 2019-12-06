# Generated by Django 2.2.4 on 2019-12-06 15:32

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('team', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='AdminUser_ID',
            field=models.ManyToManyField(help_text='The user_Id of the Admin of this team, Admin can add/remove users in the team, and rename the team-name', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddIndex(
            model_name='team',
            index=models.Index(fields=['Team_ID'], name='Team_Team_ID_b46d89_idx'),
        ),
        migrations.AddIndex(
            model_name='team',
            index=models.Index(fields=['TeamName'], name='Team_TeamNam_c3242d_idx'),
        ),
    ]