from config.common_settings import *

DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'zax(g63n3yb4m5&gfp4&6&7ie@h^3-n$fjol7hq%c&jv7u!av6'

INSTALLED_APPS += [
	'debug_toolbar',
]

DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'mymdb',
    'USER': 'mymdb',
    'PASSWORD': 'development',
    'HOST': '127.0.0.1',
    'PORT': '5432',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'default-locmemcache',
        'TIMEOUT': 60, # 60 seconds
    }
}

MEDIA_ROOT = os.path.join(BASE_DIR, '../media_root')

# Django Debug Toolbar
INTERNAL_IPS = [
	'127.0.0.1',
]
