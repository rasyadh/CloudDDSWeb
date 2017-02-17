# CloudDDSWeb
Website Cloud DDS base on OpenStack

Build by Flask and AngularJS

Recommended using Linux Operating System

1. Use Virtual Enviroment with this commands
   virtualenv env

2. Activate your Virtual Environment
   #Linux
   source env/bin/activate
   
   #Windows
   /env/Scripts/activate
   
3. Install requirements for this project
   $ pip install -r requirements.txt
   
   NB : Make sure your virtual environment activated before install requirements.txt
   
4. Create the database
   $ python manage.py createdb
   
5. Create user admin
   $ python manage.py create_admin
