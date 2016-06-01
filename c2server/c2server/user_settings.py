# Fill in the missing values based on the database that you want to use
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # if you are using sqlite,
        'NAME': 'test', # the name of the database,
        'USER': 'test', # the name of the user
        'PASSWORD': 'test', # the password of the user
        'HOST': '', # the database host
        'PORT': '', # the database port
    }
}
