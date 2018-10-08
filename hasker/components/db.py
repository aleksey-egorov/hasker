# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'hasker',
        'USER' : 'hasker',
        'PASSWORD' : DB_PASSWORD,
        'HOST' : '127.0.0.1',
        'PORT' : '5432',

    }
}
