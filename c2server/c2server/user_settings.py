# Fill in the missing values based on the database that you want to use
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',# or 'django.db.backends.sqlite3' if you are using sqlite,
        'NAME': '', # the name of the database,
        'USER': '', # the name of the user
        'PASSWORD': '', # the password of the user
        'HOST': '', # the database host
        'PORT': '', # the database port
    }
}
