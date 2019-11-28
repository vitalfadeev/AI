import os

DATABASE_NAME = "braindata"  # DATABASE
TABLE_NAME = "brain_{}_datainputlines"  # DB TABLE
SECRET_KEY = '35DhHpbsFFdRhIj0lCETSUm7syKwfEeG'

# base dir. path to app root folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')

# DB connection string in SQLAlchemy format for MySQL
DB_CONNECTION_STRING = 'mysql://admin:ixioo999@192.168.1.144/{}?charset=utf8'.format(DATABASE_NAME)

# allowed extensions. supported extension used in receive http form validation
ALLOWED_EXTENSIONS = {'json', 'csv', 'xls', 'xlsx', 'xml'}

# Credentials for AI database
port = 3306
host = '192.168.1.144'
user = 'admin'
password = 'ixioo999'
