from django.test import TestCase
from globallogger.models import GlobalLogger

class GlobalLoggerTestCase(TestCase):
    def setUp(self):
        pass

    def test_animals_can_speak(self):
        GlobalLogger.objects.create()

