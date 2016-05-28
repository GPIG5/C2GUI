# Fill in the missing values based on the database that you want to use
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',# or 'django.db.backends.sqlite3' if you are using sqlite,
        'NAME': 'postgres', # the name of the database,
        'USER': 'postgres', # the name of the user
        'PASSWORD': 'pass', # the password of the user
        'HOST': '127.0.0.1', # the database host
        'PORT': '5432', # the database port
    }
}
