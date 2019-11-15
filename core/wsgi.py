import os 
import time 
import traceback 
import signal 
import sys 
 
from django.core.wsgi import get_wsgi_application 
 
#sys.path.append('/srv/www/htdocs/AI') 
# adjust the Python version in the line below as needed 
#sys.path.append('/srv/www/htdocs/AI/venv/lib/python3.6/site-packages') 
 
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings") 
 
try: 
    application = get_wsgi_application() 
except Exception: 
    # Error loading applications 
    if 'mod_wsgi' in sys.modules: 
        traceback.print_exc() 
        os.kill(os.getpid(), signal.SIGINT) 
        time.sleep(2.5) 
