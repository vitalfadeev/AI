from django.db import models
from django.utils.translation import ugettext_lazy as _
from machine.models import Machine


# 10 possible Graph Type
GRAPH_CHOICES = (
    ('1',
        '1 (points)',
        'note : colors only can have columns of type OPTION or BINARY'
    ),
    ('2',
        '2 (points)',
        'note : colors only can have columns of type OPTION or BINARY'
    ),
    ('3',
        '3 (points)',
        'note : colors only can have columns of type OPTION or BINARY'
    ),
    ('4',
        '4 (grid)',
        'note : colors only can have columns of type OPTION or BINARY'
    ),
    ('5',
        '5 (lines)',
        ''
    ),
    ('6',
        '6',
        'note : colors only can have columns of type OPTION or BINARY'
    ),
    ('7',
        '7 (area)',
        ''
    ),
    ('8',
        '8 (points colored)',
        ''
    ),
    ('9',
        '9',
        'note : colors only can have columns of type OPTION or BINARY'
    ),
    ('10',
        '10 (3D)',
        'note : colors only can have columns of type OPTION or BINARY'
    ),
)

COLORSET_CHOICES = (
    ('1', 'light24'),
    ('2', 'pastel1'),
    ('3', 'bold'),
    ('4', 'inferno'),
    ('5', 'GnBu'),
    ('6', 'OrRd'),
    ('7', 'amp'),
    ('8', 'ice'),
    ('9', 'rdbu'),
    ('10', 'pubu'),
    ('11', 'red'),
)


def two_cols(data):
    return [row[:2] for row in data]


# Create your models here.
class Graph( models.Model ):
    Graph_ID         = models.AutoField(primary_key=True)

    Machine_ID       = models.ForeignKey(Machine, on_delete=models.CASCADE)
    DateTimeCreation = models.DateTimeField(auto_now=True)

    GraphType        = models.CharField(max_length=255, default=GRAPH_CHOICES[0][0], choices=two_cols(GRAPH_CHOICES))
    ColorScaleSet    = models.CharField(max_length=255, default='1', choices=COLORSET_CHOICES)
    X                = models.CharField(max_length=255, default='')
    Y                = models.CharField(max_length=255, default='')
    Z                = models.CharField(max_length=255, default='')
    Color            = models.CharField(max_length=255, default='')
    Animation_Frame  = models.CharField(max_length=255, default='', null=True)

    class Meta:
        db_table = 'Graph'
        verbose_name = _('Graph')
        verbose_name_plural = _('Graphs')
