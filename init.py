#!bin/python
# -*- coding: utf-8 -*-
from crontab import CronTab
from jinja2 import Template

try:
    from string import letters as ascii_letters
except:
    from string import ascii_letters

import argparse
import errno
import json
import glob
import logging
import os
import random
import stat
import string


logging.basicConfig()
logger = logging.getLogger(__name__)


default_csp = ("default-src 'self'; img-src 'self' data: *; style-src 'self' "
               "'unsafe-inline' *.googleapis.com; font-src 'self' data: "
               "*.googleapis.com *.gstatic.com; script-src 'self' "
               "'unsafe-inline' 'unsafe-eval' *.googleapis.com; child-src "
               "'self' *.youtube.com; connect-src 'self'; media-src 'self'")

password_chars = ascii_letters + string.digits + ",;.+-_="


def get_random_string(size=32, chars=password_chars):
    return ''.join(random.choice(chars) for _ in range(size))


def replace_words_in_file(src_file_path, values):
    dst_file_path = src_file_path.replace(".jinja2", "")
    input_text = ""
    with open(src_file_path, "r") as src_file:
        input_text = src_file.read()
    input_template = Template(input_text)
    output_text = input_template.render(**values)
    with open(dst_file_path, "w") as output_file:
        output_file.write(output_text)
    return dst_file_path


def create_link_if_not_exist(source, dest):
    try:
        os.symlink(source, dest)
    except Exception as e:
        if e.errno == errno.EEXIST:
            logger.info("Cannot create link because file '%s' already exists",
                        dest)
        else:
            logger.warning("Could not create symlink: from %s to %s with error %s",
                           source, dest, e)


def create_nginx_links(file, hostname):
    nginx_available = "/" + os.path.join("etc", "nginx", "sites-available",
                                         hostname.strip(".") + ".conf")
    nginx_enabled = "/" + os.path.join("etc", "nginx", "sites-enabled",
                                       hostname.strip(".") + ".conf")
    create_link_if_not_exist(file, nginx_available)
    create_link_if_not_exist(nginx_available, nginx_enabled)


try:
    with open(".config", "r") as in_file:
        defaults = json.load(in_file)
        error_loading = False
except Exception as ex:
    defaults = {}
    error_loading = True
    logger.error("Exiting: Error loading .config file: %s", ex)
    exit()

parser = argparse.ArgumentParser(description='Docker mariadb django nginx \
                                              stack configurator.')
parser.add_argument('-hn', '--hostname', help='Host name',
                    default=defaults.get("hostname", "example.com"),
                    required=False)
parser.add_argument('-pe', '--portexternal',
                    help='Http external nginx port number publically visible',
                    default=defaults.get("portexternal", 80), required=False)
parser.add_argument('-pes', '--portexternalssl',
                    help='Https external nginx port number publically visible',
                    default=defaults.get("portexternalssl", 443), required=False)
parser.add_argument('-pi', '--portinternal',
                    help='Http internal nginx port number publically visible',
                    default=defaults.get("portinternal", 7080), required=False)
parser.add_argument('-cp', '--certificatespath',
                    help='Use this parameter for certificates path',
                    default=defaults.get("certificatespath", ""),
                    required=False)
parser.add_argument('-csp', '--contentsecuritypolicy',
                    help='Use this parameter for the value of the content '
                    'security policy http header',
                    default=defaults.get("contentsecuritypolicy", default_csp),
                    required=False)
parser.add_argument('-dbn', '--dbname', help='Database name', required=False,
                    default=defaults.get("dbname", "database"))
parser.add_argument('-dbu', '--dbuser', help='Database user', required=False,
                    default=defaults.get("dbuser", "user"))
parser.add_argument('-dbp', '--dbpassword', help='Database password',
                    required=False,
                    default=defaults.get("dbpassword", get_random_string()))
parser.add_argument('-g', '--gis',
                    help="Use this parameter to add GIS support to postgres",
                    default=defaults.get("gis", False),
                    action='store_true')
parser.add_argument('-gr', '--gitrepository',
                    help="Project repository checkout",
                    default=defaults.get("gitrepository", ""),)
parser.add_argument('-gb', '--gitbranch',
                    help="Project repository branch",
                    default=defaults.get("gitbranch", "master"),)
parser.add_argument('-l', '--libraries', help='apt requirements', required=False,
                    default=defaults.get("libraries", []))
parser.add_argument('-r', '--requirements', help='Django app requirements', required=False,
                    default=defaults.get("requirements", []))
parser.add_argument('-rd', '--requirementsdev', help='Django app development requirements', required=False,
                    default=defaults.get("requirementsdev", []))
parser.add_argument('-smtpu', '--smtpuser', help='SMTP user',
                    required=False,
                    default=defaults.get("smtpuser", ""))
parser.add_argument('-smtpp', '--smtppassword', help='SMTP password',
                    required=False,
                    default=defaults.get("smtppassword", ""))
parser.add_argument('-smtph', '--smtphost', help='SMTP host address',
                    required=False,
                    default=defaults.get("smtphost", ""))
parser.add_argument('-pn', '--projectname', help='Name of the project',
                    required=False, default=defaults.get("projectname",
                                                         "project"))
parser.add_argument('-pv', '--pythonversion', help='Python version to use as base docker image',
                    required=False, default=defaults.get("pythonversion",
                                                         '3.6'))
parser.add_argument('-sc', '--secretkey', help='django project secret key',
                    required=False, default=defaults.get("secretkey",
                                                         get_random_string(50)))
parser.add_argument('-sp', '--spooler', help='add spool process',
                    required=False, default=defaults.get("spooler", False),
                    action='store_true')
parser.add_argument('-scale', '--scale', help='django instances number',
                    required=False, default=defaults.get("scale", 1)),

parser.add_argument('-ul', '--uploadlimit', help='max MB uplodable',
                    required=False, default=defaults.get("uploadlimit"))
parser.add_argument('-br', '--backuprepository', help='backup git repo',
                    required=False, default=defaults.get("backuprepository",
                                                         None))
parser.add_argument('-bf', '--backupfolders', help='Folders to backup', required=False,
                    default=defaults.get("backupfolders", []))
parser.add_argument('-bi', '--backupignores', help='Folders to ignore during backup', required=False,
                    default=defaults.get("backupignores", []))
parser.add_argument('-cm', '--cronjobminute', help='backup croonjob minute',
                    required=False, default=defaults.get("cronjobminute",
                                                         "30"))
parser.add_argument('-ch', '--cronjobhour', help='backup cronjob hour',
                    required=False, default=defaults.get("cronjobhour",
                                                         "03"))
parser.add_argument('-v', '--verbose',
                    help="Use this parameter to see verbose output",
                    default=defaults.get("verbose", False),
                    action='store_true')
parser.add_argument('-c', '--create',
                    help="Use this parameter to create the .config file if does not exists",
                    default=defaults.get("create", False),
                    action='store_true')
parser.add_argument('-dev', '--development',
                    help="Use this parameter to see development to true",
                    default=defaults.get("development", False),
                    action='store_true')
parser.add_argument('-async', '--async',
                    help="Use this parameter to use async server",
                    default=defaults.get("async", False),
                    action='store_true')

args = parser.parse_args()
args_dict = vars(args)
if args.verbose:
    logger.setLevel(logging.DEBUG)

base_path = os.path.dirname(os.path.realpath(__file__))
args_dict["projectpath"] = base_path
root_cron = None
if not os.path.exists(os.path.join(base_path, "config")):
    os.makedirs(os.path.join(base_path, "config"))
try:
    root_cron = CronTab(user='root')
except IOError:
    logger.warning("Not changing cronjob: not root")

for filename in glob.iglob(os.path.join(base_path, "config.jinja2", "*.jinja2")):
    src_file_path = os.path.join(base_path, "config.jinja2", filename) 
    dst_file_path = replace_words_in_file(src_file_path, args_dict)
    dst_file_name = dst_file_path.split("/")[-1]
    if dst_file_path.endswith("nginx.external.conf"):
        create_nginx_links(dst_file_path, args.hostname)
    if dst_file_path.endswith(".sh"):
        st = os.stat(dst_file_path)
        os.chmod(dst_file_path, st.st_mode | stat.S_IEXEC)

    if dst_file_name.startswith("cron-") and args_dict.get("backuprepository", False):
        if root_cron:
            command = dst_file_path + " >> /var/log/" + dst_file_name + ".log  2>&1"
            old_jobs = root_cron.find_command(command)
            for job in old_jobs:
                root_cron.remove(job)

            root_job = root_cron.new(command=command)
            root_job.minute.on(args_dict["cronjobminute"])
            root_job.hour.on(args_dict["cronjobhour"])
            root_job.enable()
            root_cron.write()

# save values #
if not error_loading or args_dict["create"]:
    with open(".config", "w") as out_file:
        json.dump(args_dict, out_file, sort_keys=True, indent=4)
