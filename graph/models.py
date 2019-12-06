from django.db import models
from django.utils.translation import ugettext_lazy as _
from machine.models import Machine

class Graph(models.Model):
	Graph_ID         = models.AutoField(primary_key=True)

	Machine_ID       = models.ForeignKey(Machine, on_delete=models.CASCADE, help_text="The graph belong to this machine/Machine")
	DateTimeCreation = models.DateTimeField(auto_now_add=True, help_text="To order the list of graph by most recent first")

	GraphType        = models.CharField(max_length=255, default="1", help_text="Type Of Graph")
	ColorScaleSet    = models.CharField(max_length=255, default='1', help_text="Name Of Color Set")
	X                = models.CharField(max_length=255, default='', help_text="The Column Name")
	Y                = models.CharField(max_length=255, default='', help_text="The Column Name")
	Z                = models.CharField(max_length=255, default='', help_text="The Column Name")
	Color            = models.CharField(max_length=255, default='', help_text="The Column Name")
	Animation_Frame  = models.CharField(max_length=255, default='', null=True, help_text="The Column Name")

	class Meta:
		db_table = 'Graph'
		verbose_name = _('Graph')
		verbose_name_plural = _('Graphs')

	def __str__(self):
		return  f"{self.Machine_ID} -{self.GraphType}"

