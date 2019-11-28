from django.contrib.auth.models import User as DjangoUser
from django.db import models

# Create your models here.

class User(models.Model):
    User_ID = models.OneToOneField(DjangoUser, unique=True, on_delete=models.CASCADE )

    Email = models.EmailField(null=True)
    FirstName = models.CharField(max_length=140, null=True)
    LastName = models.CharField(max_length=140, null=True)

    UserProfile = models.TextField()

    IsConsultant = models.BooleanField(default=False)
    ConsultantProfile = models.TextField()

    APIKey = models.CharField(max_length=140, null=True)

    IsSuperAdmin = models.BooleanField(default=False)

    AccessPending = models.BooleanField(default=False)
    AccessRevoked = models.BooleanField(default=False)
