#!/bin/bash

#
DOMAIN=local.ixioo.com

SITE_FOLDER=/home/vital/src/AI
SITE_CONFIG=/etc/apache2/sites-available/${DOMAIN}.conf
SITE_VENV_PACKAGES_PATH=${SITE_FOLDER}/venv/lib/python3.6/site-packages

DB_NAME=AI
DB_USER=${DB_NAME}_dbu
DB_PASS=******
DB_NAME_MachineData=MachineData
DB_NAME_GlobalLogger=GlobalLogger

SMTP_SERVER=srv6.wahooart.com
SMTP_USER=******
SMTP_PASS=


#
_message() {
    MESSAGE=$*
    echo -e "\e[32m${MESSAGE}\e[0m"
}

_python() {
    _message "Installing Python"
    sudo apt install python3
    sudo apt install apache2 libapache2-mod-wsgi-py3
}


_hosts() {
    _message "Updating hosts"
    # /etc/hosts
    # for developer only
    cat > /etc/hosts <<EOF
127.0.0.1       $DOMAIN
EOF
}


_apache_config() {
    _message "Creating Apache config"
    APACHE_USER=www-data
    APACHE_GROUP=www-data

    sudo touch ${SITE_CONFIG}
    sudo chmod a+rw ${SITE_CONFIG}
    cat > ${SITE_CONFIG} <<EOF
<VirtualHost *:80>
    ServerName ${DOMAIN}

    DocumentRoot ${SITE_FOLDER}

    CustomLog /var/log/apache2/ai_access.log common
    ErrorLog /var/log/apache2/ai_error.log

    WSGIDaemonProcess ${DOMAIN} user=${APACHE_USER} group=${APACHE_GROUP} python-path=${SITE_FOLDER}:${SITE_VENV_PACKAGES_PATH}
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

    sudo chmod a-w ${SITE_CONFIG}
}


_site() {
    _message "Coping site files"
    mkdir ${SITE_FOLDER}
    SELF_PATH="`dirname \"$0\"`"
    cd ${SELF_PATH}
    cp -a . ${SITE_FOLDER}/
}


_site_permissions() {
    _message "Setting site permissiona"
    chmod -R a+r ${SITE_FOLDER}
    cd ${SITE_FOLDER}
    mkdir ${SITE_FOLDER}/media
    chmod -R a+rw ${SITE_FOLDER}/media
}


_python_venv() {
    _message "Creating Python venv"
    cd ${SITE_FOLDER}
    python3 -m venv venv
}


_python_requirements() {
    _message "Instlling requiremtns"
    cd ${SITE_FOLDER}
    source venv/bin/activate
    pip install pip --upgrade
    pip install -r requirements.txt
}


_mysql() {
    _message "Instlling MySQL server"
    sudo apt install mysql-server
}


_mysql_drop_old_db() {
    _message "Dropping old MySQL databases"
    mysql -u root -p <<EOF
    DROP DATABASE IF EXISTS ${DB_NAME};
    DROP DATABASE IF EXISTS ${DB_NAME_MachineData};
    DROP DATABASE IF EXISTS ${DB_NAME_GlobalLogger};
EOF
}


_mysql_db() {
    _message "Creating MySQL DB"
    mysql -u root -p <<EOF
    CREATE DATABASE IF NOT EXISTS ${DB_NAME} DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
    GRANT ALL PRIVILEGES ON ${DB_NAME}.* TO ${DB_USER}@'%' IDENTIFIED BY '${DB_PASS}';
    CREATE DATABASE IF NOT EXISTS ${DB_NAME_MachineData} DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
    GRANT ALL PRIVILEGES ON ${DB_NAME_MachineData}.* TO ${DB_USER}@'%' IDENTIFIED BY '${DB_PASS}';
    CREATE DATABASE IF NOT EXISTS ${DB_NAME_GlobalLogger} DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
    GRANT ALL PRIVILEGES ON ${DB_NAME_GlobalLogger}.* TO ${DB_USER}@'%' IDENTIFIED BY '${DB_PASS}';
    FLUSH PRIVILEGES;
EOF
}


_django_local_settings() {
    _message "Creaing Django local settigns"
    # local_settings
    cat > ${SITE_FOLDER}/core/local_setting.py <<EOF
EMAIL_USE_TLS = False
EMAIL_HOST = '${SMTP_SERVER}'
EMAIL_HOST_USER = '${SMTP_USER}'
EMAIL_HOST_PASSWORD = '${SMTP_PASS}'
EMAIL_PORT = 25

DATABASE_ENGINE = 'django.db.backends.mysql'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '${DB_NAME}',
        'USER': '${DB_USER}',
        'PASSWORD': '${DB_PASS}',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
EOF
}


_django_tables() {
    _message "Creaing Django tables"
    cd ${SITE_FOLDER}
    for folder in ./*
    do
        [ -d $folder/migrations  ] && rm -rf $folder/migrations
    done

    source venv/bin/activate
    ./manage.py makemigrations
    ./manage.py migrate
}


_django_superuser() {
    _message "Creating Django superuser"
    source venv/bin/activate
    ./manage.py createsuperuser
}


_restart_apache() {
    _message "Restarting Apache"
    sudo a2ensite ${DOMAIN}
    sudo systemctl restart apache2
}


_final_message() {
    _message "Site available at: http://${DOMAIN}"
}


_python
_apache_config
_site
_site_permissions
_python_venv
_python_requirements
_mysql
_mysql_db
_django_local_settings
_django_tables
_django_superuser
_restart_apache
_final_message

## _gunicorn


