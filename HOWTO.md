# Setup

## Create and Activate Environment:
A folder called 'venv' will be created with the next command content of this folder will be ignored from git repository and kept locally.

```
python -m venv venv
source venv/bin/activate
```

## Install Requirements
```
pip install pip --upgrade
pip install -r requirements.txt
```

## Add Local Settings File

Create 'core/local_setting.py' file with content:
```
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

EMAIL_HOST_USER=''
EMAIL_HOST_PASSWORD=''

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

DATABASE_ENGINE = ''

```

## Migrate Database
The virtual environment should be enabled before running any migration. If not, re-activate it.

```
python manage.py migrate
```

## Deactivate
```
deactivate
```

## Re-activate
```
source venv/bin/activate
```