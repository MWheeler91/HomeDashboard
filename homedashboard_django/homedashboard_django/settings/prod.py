from .base import *

DEBUG = env('DEBUG_PROD')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS_PROD')


CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS_PROD')
CORS_ORIGIN_ALLOW_ALL = False
SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin'
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    },
}
