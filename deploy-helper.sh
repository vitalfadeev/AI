#!/bin/bash

# This script runned on server
# via ssh root@94.23.192.197 /home/www/htdocs/AI/deploy-helper.sh
# (see: deploy.sh)
#
# it will be:
# - fetch website sources
# - reload Apache


SITE=/home/www/htdocs/AI


# Stop on eny error
set -e


_message() {
    MESSAGE=$*
    echo -e "\e[32m${MESSAGE}\e[0m"
}

# cd site
_message "cd ${SITE}"
cd ${SITE}


# Getting fresh sources
# Note: deploy was created by command: git remote add deploy ssh://git@github.com/vitalfadeev/AI.git
_message "Getting fresh sources"
git pull deploy master


# Activating Virtual environment
_message "Activating Virtual environment"
source venv/bin/activate


# Installing requirements
_message "Installing requirements"
pip install pip --upgrade
pip install -r requirements.txt


# Updating DB structure
_message "Updating DB structure"
python ./manage.py makemigrations
python ./manage.py migrate


# Reloading Apache
_message "Reloading Apache"
systemctl reload apache2


# All done!
_message "All done!"


# it runned like a: ssh root@94.23.192.197 /home/www/htdocs/AI/deploy-helper.sh
#
# or
# Login via ssh
# ssh root@94.23.192.197
# /home/www/htdocs/AI/deploy-helper.sh
