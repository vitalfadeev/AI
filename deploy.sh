#!/bin/bash

# cd site
cd /home/www/htdocs/AI/

# get fresh sources
git pull

# reload Apache
systemctl reload apache2


# it runned like a: ssh root@94.23.192.197 /home/www/htdocs/AI/deploy.sh
#
# or
# Login via ssh
# ssh root@94.23.192.197
# /home/www/htdocs/AI/deploy.sh
