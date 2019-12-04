from django.db import models
from django.utils.translation import ugettext_lazy as _
from machine.models import Machine

class Graph(models.Model):
	Graph_ID         = models.AutoField(primary_key=True)

	Machine_ID       = models.ForeignKey(Machine, on_delete=models.CASCADE)
	DateTimeCreation = models.DateTimeField(auto_now=True)

	GraphType        = models.CharField(max_length=255, default="1")
	ColorScaleSet    = models.CharField(max_length=255, default='1')
	X                = models.CharField(max_length=255, default='')
	Y                = models.CharField(max_length=255, default='')
	Z                = models.CharField(max_length=255, default='')
	Color            = models.CharField(max_length=255, default='')
	Animation_Frame  = models.CharField(max_length=255, default='', null=True)

	class Meta:
		db_table = 'Graph'
		verbose_name = _('Graph')
		verbose_name_plural = _('Graphs')
