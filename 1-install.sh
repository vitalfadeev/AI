#!/bin/bash

#
DOMAIN=local.ixioo.com
SITE_CONFIG=/etc/apache2/sites-available/${DOMAIN}.conf
SITE_FOLDER=/home/vital/src/AI
SITE_GIT=https://github.com/vitalfadeev/AI.git
DB_NAME=ai
DB_USER=${DB_NAME}_dbu
DB_PASS=ixioo777
DB_NAME_MachineData=MachineData
DB_NAME_GlobalLogger=GlobalLogger
SMTP_SERVER=srv6.wahooart.com
SMTP_USER=info@ixioo.com
SMTP_PASS=


#
_python() {
    sudo apt install python3
    sudo apt install apache2 libapache2-mod-wsgi-py3
}


_hosts() {
    # /etc/hosts
    # for developer only
    cat > /etc/hosts <<EOF
127.0.0.1       $DOMAIN
EOF
}


_apache_config() {
    APACHE_USER=www-data
    APACHE_GROUP=www-data

    cat > $SITE_CONFIG <<EOF
    <VirtualHost *:80>
    ServerName ${DOMAIN}

    DocumentRoot ${SITE_FOLDER}

    CustomLog /var/log/apache2/ai_access.log common
    ErrorLog /var/log/apache2/ai_error.log

    WSGIDaemonProcess ${DOMAIN} user=${APACHE_USER} group${APACHE_GROUP} python-path=${SITE_FOLDER}
    WSGIProcessGroup ${DOMAIN}
    WSGIScriptAlias / ${SITE_FOLDER}/core/wsgi.py

    Alias /static/ ${SITE_FOLDER}/static/

    <Directory ${SITE_FOLDER}/static>
        Require all granted
    </Directory>

    <Directory ${SITE_FOLDER}/core>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>
    </VirtualHost>
EOF
}


_site() {
    cd `dirname ${SITE_FOLDER}`
    git clone ${SITE_GIT} ${SITE_FOLDER}
}


_site_permissions() {
    cd ${SITE_FOLDER}
    chmod -R a+rw ${SITE_FOLDER}/media
}


_python_venv() {
    cd ${SITE_FOLDER}
    python3 -m venv venv
}


_python_requirements() {
    cd ${SITE_FOLDER}
    source venv/bin/activate
    pip install pip --upgrade
    pip install -r requirements.txt
}


_mysql_db() {
    sudo apt install mysql-server
}


_mysql_db() {
    mysql -u root -p
    CREATE DATABASE ${DB_NAME} DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
    GRANT ALL PRIVILEGES ON `${DB_NAME}`.* TO `${DB_USER}`@`%` IDENTIFIED BY '${DB_PASS}';
    CREATE DATABASE ${DB_NAME_MachineData} DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
    GRANT ALL PRIVILEGES ON `${DB_NAME_MachineData}`.* TO `${DB_USER}`@`%` IDENTIFIED BY '${DB_PASS}';
    CREATE DATABASE ${DB_NAME_GlobalLogger} DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
    GRANT ALL PRIVILEGES ON `${DB_NAME_GlobalLogger}`.* TO `${DB_USER}`@`%` IDENTIFIED BY '${DB_PASS}';
    FLUSH PRIVILEGES;
}


_django_db_settings() {
    # local_settings
}


_django_tables() {
    cd ${SITE_FOLDER}
    find . -path "*/migrations/*.py" -not -name "__init__.py" -path ./venv -prune -delete
    find . -path "*/migrations/*.pyc"  -delete

    ./manage.py makemigrations
    ./manage.py migrate
    ./manage.py createsuperuser
}


_restart_apache() {
    a2ensite ${DOMAIN}
    systemctl restart apache2
}


_python
#_hosts
_apache_config
_site
_site_permissions
_python_venv
_python_requirements
_mysql
_mysql_db
_django_db_settings
_django_tables
_restart_apache
# _gunicorn


