
import os
from lisa.settings.common import *

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
