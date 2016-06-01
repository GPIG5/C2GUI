# Fill in the missing values based on the database that you want to use
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # if you are using sqlite,
        'NAME': 'postgres', # the name of the database,
        'USER': 'mjm540', # the name of the user
        'PASSWORD': '', # the password of the user
        'HOST': 'localhost', # the database host
        'PORT': '', # the database port
    }
}
