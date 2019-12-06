#!/bin/bash

python manage.py migrate
python manage.py migrate globallogger  --database=GlobalLogger
