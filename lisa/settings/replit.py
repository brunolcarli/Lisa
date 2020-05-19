"""
Settings para utilizar no repl.it
"""
from decouple import config
from lisa.settings.common import *


SECRET_KEY = config('DJANGO_SECRET_KEY', '')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': config(BASE_DIR, 'db.sqlite3'),
    }
}
