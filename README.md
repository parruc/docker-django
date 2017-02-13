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

    virtualenv .
    pip install -r requirements.txt

Comamnds to build and run docker conainers:
------------------------------------------

First we have to call the init script that compiles the configuration templates
into real configuration files for docker compose and nginx (both int and ext)::


    ./init.py -hn example.com -p 7080 -rw -dbn db_name -dbu db_user
    docker-compose up -d
    service nginx reload

The init script help:
--------------------------
usage: init.py [-h] [-hn HOSTNAME] [-p PORT] [-cp CERTIFICATESPATH]
               [-csp CONTENTSECURITYPOLICY] [-dbn DBNAME] [-dbu DBUSER]
               [-dbp DBPASSWORD] [-dbrp DBROOTPASSWORD] [-pn PROJECTNAME]
               [-dv DJANGOVERSION] [-sc SECRETKEY] [-ul UPLOADLIMIT] [-rw]
               [-v] [-dev]

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
  -dbrp DBROOTPASSWORD, --dbrootpassword DBROOTPASSWORD
                        Database root password
  -pn PROJECTNAME, --projectname PROJECTNAME
                        Name of the project
  -dv DJANGOVERSION, --djangoversion DJANGOVERSION
                        django version
  -sc SECRETKEY, --secretkey SECRETKEY
                        django project secret key
  -ul UPLOADLIMIT, --uploadlimit UPLOADLIMIT
                        max MB uplodable
  -rw, --rewrite        Use this parameter if your website uses url rewrite
  -v, --verbose         Use this parameter to see verbose output
  -dev, --development   Use this parameter to see development to tru
  
The configuration params will be printed on screen and saved on a .config file
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