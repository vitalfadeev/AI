from django.db import models

# Create your models here.
from machine.models import Machine


class Work(models.Model):
    Work_ID                              =  models.AutoField(primary_key=True )

    CreationDateTime                     =  models.DateTimeField(auto_now=True)
    Machine_ID                           =  models.ForeignKey( Machine, on_delete=models.CASCADE )
    ServerName                           =  models.CharField( max_length=255, null=True )

    IsWorkTraining                       =  models.BooleanField(default=False)
    IsWorkSolving                        =  models.BooleanField(default=False)

    IsWorkStatusWaitForServerStart       =  models.BooleanField(default=False)
    IsWorkStatusServerProcessing         =  models.BooleanField(default=False)
    IsWorkStatusServerFinished           =  models.BooleanField(default=False)

    DataLineToProcess_FirstLineID        =  models.IntegerField(null=True)
    DataLineToProcess_LastLineID         =  models.IntegerField(null=True)

    WorkStartedAtDateTime                =  models.DateTimeField(null=True)
    WorkStartedByServerName              =  models.CharField( max_length=255 )
    WorkStartedCountOfLineToProcess      =  models.IntegerField( null=True )
    WorkDurationEstimationSeconds        =  models.IntegerField( null=True )

    WorkFinishedAtDateTime               =  models.DateTimeField(null=True)
    WorkFinishedByServerName             =  models.CharField( max_length=255 )
    WorkFinishedCountOfLineToProcess     =  models.IntegerField( null=True )
    WorkFinishedDurationSeconds          =  models.IntegerField( null=True )

    Learning_DelayElapsedSeconds         =  models.IntegerField( null=True )
    Solving_DelayElapsedSeconds          =  models.IntegerField( null=True )

    TextError                            =  models.TextField(null=True)
    TextWarning                          =  models.TextField(null=True)


