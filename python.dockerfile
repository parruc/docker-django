FROM python:3.6
pip install mysqlclient
pip install Django
django-admin startproject {{projectname}}
#RUN apt-get update && apt-get install -y libfreetype6-dev libjpeg62-turbo-dev libmcrypt-dev libpng12-dev && rm -rf /var/lib/apt/lists/*
