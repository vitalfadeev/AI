# Generated by Django 2.2.4 on 2019-12-03 16:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Email', models.EmailField(max_length=254, null=True)),
                ('FirstName', models.CharField(max_length=140, null=True)),
                ('LastName', models.CharField(max_length=140, null=True)),
                ('UserProfile', models.TextField()),
                ('IsConsultant', models.BooleanField(default=False)),
                ('ConsultantProfile', models.TextField()),
                ('APIKey', models.CharField(max_length=140, null=True)),
                ('IsSuperAdmin', models.BooleanField(default=False)),
                ('AccessPending', models.BooleanField(default=False)),
                ('AccessRevoked', models.BooleanField(default=False)),
                ('User_ID', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'User',
            },
        ),
    ]
