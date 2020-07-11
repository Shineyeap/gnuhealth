#!/usr/bin/env python3

##############################################################################
#
#    GNU Health: The Free Health and Hospital Information System
#    Copyright (C) 2008-2020 Luis Falcon <falcon@gnu.org>
#    Copyright (C) 2011-2020 GNU Solidario <health@gnusolidario.org>
#
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import os
import sys
import bcrypt
import getpass
import tinydb
from pathlib import Path
from tinydb import TinyDB, Query
import configparser

homedir = str(Path.home())
gh_dir = os.path.join(homedir, 'mygnuhealth')
config_file = os.path.join(gh_dir, 'ghealth.conf')
dbfile = os.path.join(gh_dir, 'ghealth.db')


def check_inst_dir():
    if not (os.path.isdir(gh_dir)):
        print ("Initializing MyGNUHealth directory")
        try:
            os.mkdir(gh_dir)
        except:
            print ("Error initializing MyGNUHealth directory")

def check_config():
    if not os.path.isfile(config_file):
        print ("Configuration file not found. Writing defaults")
        set_default_config_file()


def check_db():
    if not os.path.isfile(dbfile):
        print ("DB file not found. Initializing MyGNUHealth...")
        db = TinyDB(dbfile)
        init_db(db)

def validate_password():
    passwd = getpass.getpass()
    print ("Again")
    passwd2 = getpass.getpass()
    if (passwd != passwd2):
        print ("Password mismatch")
        return validate_password()
    return passwd

def set_default_config_file():
    config = configparser.ConfigParser()
    config.read(config_file)
    if not 'security' in config.sections():
        config.add_section('security')

    config.set ('security','key_method','bcrypt')
    output_file = open(config_file,'w')
    config.write(output_file)



def init_db(db):
    gh_key = validate_password()
    encrypted_key = bcrypt.hashpw(gh_key.encode('utf-8'), \
        bcrypt.gensalt()).decode('utf-8')

    credentials = db.table('credentials')
    credentials.insert({'master_key':encrypted_key})

    print ("MyGNUHealth DB initialized !")


def verify_installation_status():
    check_inst_dir()
    check_config()
    check_db()

