#!/bin/bash

# cd site
cd /home/www/htdocs/AI/

# Getting fresh sources
# Note: deploy was created by command: git remote add deploy ssh://git@github.com/vitalfadeev/AI.git
git pull deploy master

# Reloading Apache
systemctl reload apache2


# it runned like a: ssh root@94.23.192.197 /home/www/htdocs/AI/deploy.sh
#
# or
# Login via ssh
# ssh root@94.23.192.197
# /home/www/htdocs/AI/deploy.sh
