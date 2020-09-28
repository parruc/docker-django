#!/bin/bash

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
	sudo apt install python3 python3-dev python3-pip nodejs npm nginx docker.io
else
	echo "Ensure to install python3 python3-dev python3-pip nodejs npm nginx and docker.io equivalent on your OS"
fi
pip3 install virtualenv docker-compose 
virtualenv --python=python3 .
bin/pip install -r requirements.txt
sudo ./init.py
sudo chown -R `id -un` .
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
	sudo service nginx reload
else
	echo "Remember to restart NGINX"
fi
