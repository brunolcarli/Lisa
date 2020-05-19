import os
from lisa.settings.common import *


SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '')
DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('MYSQL_DATABASE', ''),
        'USER': os.environ.get('MYSQL_USER', ''),
        'PASSWORD': os.environ.get('MYSQL_PASSWORD', ''),
        'HOST': os.environ.get('MYSQL_HOST', ''),
        'PORT': 3306,
    }
}