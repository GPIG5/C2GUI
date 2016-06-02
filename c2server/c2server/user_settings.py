# Fill in the missing values based on the database that you want to use
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # if you are using sqlite,
        'NAME': 'c2', # the name of the database,
        'USER': 'c2user', # the name of the user
        'PASSWORD': 'test', # the password of the user
        'HOST': 'localhost', # the database host
        'PORT': '', # the database port
    }
}
