# DEBUG = True
import os
from pay.settings import BASE_DIR
ALLOWED_HOSTS = [
        '127.0.0.1',
        'localhost',
        '0.0.0.0'
    ]

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
DOMAIN = 'http://127.0.0.1:8000'
