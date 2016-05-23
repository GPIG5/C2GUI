All python packages required for running the server can be found in c2server/requirements.txt.

Before you run the server for the first time, you need to initialise a database using the following commands:
$ python3 manage.py makemigrations
$ python3 manage.py migrate
$ python3 manage.py fill_database

You can set the IP address and the host of the environment in c2server/c2gui/communicator.py.

To run the C2 server on a specific address, run the following command:
$ python3 manage.py runserver <ip_address:port>

To run the C2 server on localhost, run:
$ python3 manage.py runserver

The main page of the C2 server GUI can be accessed at "<ip_address:port>/c2gui".
