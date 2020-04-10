Brief guide
===========

Requirements:
-------------

* nginx
* docker
* docker-compose
* virtualenv

Installation example on deb based systems::

    apt-get install nginx docker docker-compose virtualenv

Create a local virtualenv and install requirements::

    virtualenv . --python=python3
    pip install -r requirements.txt

Comamnds to build and run docker conainers:
------------------------------------------

First we have to call the init script that compiles the configuration templates
into real configuration files for docker compose and nginx (both int and ext)
Arguments can be passed to the command but easiest way is to use a .config file
containing the relevant setup information in json format::


    ./init.py -hn example.com -p 7080 -rw -dbn db_name -dbu db_user
    docker-compose up -d
    service nginx reload

The init script help:

```bash
--------------------------
usage: init.py [-h] [-hn HOSTNAME] [-p PORT] [-cp CERTIFICATESPATH]
               [-csp CONTENTSECURITYPOLICY] [-dbn DBNAME] [-dbu DBUSER]
               [-dbp DBPASSWORD] [-g] [-r REQUIREMENTS] [-smtpu SMTPUSER]
               [-smtpp SMTPPASSWORD] [-smtph SMTPHOST] [-pn PROJECTNAME]
               [-pv PYTHONVERSION] [-sc SECRETKEY] [-ul UPLOADLIMIT]
               [-br BACKUPREPOSITORY] [-cm CRONJOBMINUTE] [-ch CRONJOBHOUR]
               [-v] [-c] [-dev]

Docker mariadb django nginx stack configurator.

optional arguments:
  -h, --help            show this help message and exit
  -hn HOSTNAME, --hostname HOSTNAME
                        Host name
  -p PORT, --port PORT  Http internal nginx port number publically visible
  -cp CERTIFICATESPATH, --certificatespath CERTIFICATESPATH
                        Use this parameter for certificates path
  -csp CONTENTSECURITYPOLICY, --contentsecuritypolicy CONTENTSECURITYPOLICY
                        Use this parameter for the value of the content
                        security policy http header
  -dbn DBNAME, --dbname DBNAME
                        Database name
  -dbu DBUSER, --dbuser DBUSER
                        Database user
  -dbp DBPASSWORD, --dbpassword DBPASSWORD
                        Database password
  -g, --gis             Use this parameter to add GIS support to postgres
  -r REQUIREMENTS, --requirements REQUIREMENTS
                        Django app requirements
  -smtpu SMTPUSER, --smtpuser SMTPUSER
                        SMTP user
  -smtpp SMTPPASSWORD, --smtppassword SMTPPASSWORD
                        SMTP password
  -smtph SMTPHOST, --smtphost SMTPHOST
                        SMTP host address
  -pn PROJECTNAME, --projectname PROJECTNAME
                        Name of the project
  -pv PYTHONVERSION, --pythonversion PYTHONVERSION
                        Python version to use as base docker image
  -sc SECRETKEY, --secretkey SECRETKEY
                        django project secret key
  -ul UPLOADLIMIT, --uploadlimit UPLOADLIMIT
                        max MB uplodable
  -br BACKUPREPOSITORY, --backuprepository BACKUPREPOSITORY
                        backup git repo
  -cm CRONJOBMINUTE, --cronjobminute CRONJOBMINUTE
                        backup croonjob minute
  -ch CRONJOBHOUR, --cronjobhour CRONJOBHOUR
                        backup cronjob hour
  -v, --verbose         Use this parameter to see verbose output
  -c, --create          Use this parameter to create the .config file if does
                        not exists
  -dev, --development   Use this parameter to see development to true
```

The configuration params will be printed on screen and saved in the .config file.
params order of resultion is:

cli arguments -> .config fie -> defaults

The init script, after compiling the external nginx configuration file will
create a symlink in te appropriated nginx directory:
/etc/nginx/sites-(available|enabled)/example.com.conf

If we want to make everyting this effective we will have to restart nginx:
service nginx reload

Fix permissions
---------------

static directory will have all files created by the user running all the process
above. If your architecture requires write permission you will have to change
the owner::

Makefile commands:
------------------

Adds system packages on Linux

    make dependencies

Install node project and packages

    make node

Create migrations

    make: migrations

Execute migrations

    make migrate

Extracts and compiles tranlation messages

    make messages

Compiles static resources for production

    make theme

Compiles static resources and starts hot-reload

    make theme_dev

Updates the repository and runs pull, migrate, messages and theme

    make update

Exactly the same as update but starts layout dev server

    make update_dev

HTTPS
-----

If you want to setup an https server you will also need letsencrypt::

    sudo apt-get install letsencrypt

And you will have to create your own certificates::

    letsencrypt certonly --webroot -w . -d example.com -d www.example.com


To use https you can use certificatespath arguemnt writing the path where the
certificates are. The certificates must have been created externally
using certpath command (installed as python requirement)


When developement is active:

 * Django is execute in debug models
 * Debug toolbar is shown
 * uwsgi starts with python-autoreload=1 and honour-stdin=true to allow pdb
 * docker compose launches uwsgi using stdin_open: true tty: true to allow pdb

Super user creation
-------------------

To create the admin user you can run 

```bash
docker-compose run django /project/bin/python /project/PROJECT_NAME/manage.py createsuperuser
```
