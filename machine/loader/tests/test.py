import os

from django.test import TestCase
from django.db import connection
from machine.loader.loader import load

TESTDIR = os.path.dirname(__file__)

class LoaderTestCase(TestCase):
    def setUp(self):
        pass

    def test_1_csv_loader(self):
        "ProductC.csv"
        table = "loader_test"
        url = os.path.join( TESTDIR, 'ProductC.csv' )
        load( url, table, connection )

# Usage
# ./manage.py test machine/loader/
