#!/bin/bash

# Login via ssh
ssh root@94.23.192.197

# cd site
cd /home/www/htdocs/AI/

# get fresh sources
git pull

# reload Apache
systemctl reload apache2


# in future just run: ssh root@94.23.192.197 /home/www/htdocs/AI/deploy.sh