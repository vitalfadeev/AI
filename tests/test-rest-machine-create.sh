#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Test
#python manage.py test --keepdb --verbosity 2 machine/tests
python manage.py test --verbosity 2 machine/tests

