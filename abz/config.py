# Copyright 2014 Music Technology Group - Universitat Pompeu Fabra
# acousticbrainz-client is available under the terms of the GNU
# General Public License, version 3 or higher. See COPYING for more details.

from __future__ import print_function

import ConfigParser
import os
import sys
import hashlib
import sqlite3
import shutil

CONFIG_FILE="abzsubmit.conf"
OLDCONFIGFILE = os.path.join(os.path.expanduser("~"), ".abzsubmit.conf")
PROCESSED_FILE_LIST = os.path.expanduser("~/.abzsubmit.log")

settings = {}

def create_sqlite(dbfile):
    conn = sqlite3.connect(dbfile)
    c = conn.cursor()
    c.execute("""create table filelog (id integer primary key, filename text not null, reason text)""")
    c.execute("""create index filelog_filename on filelog(filename)""")
    conn.commit()

def migrate_old_settings(dbfile):
    # 1. Move old config file to config directory
    if os.path.exists(OLDCONFIGFILE):
        configfile = os.path.join(get_config_dir(), CONFIG_FILE)
        print("Moving %s to new location %s" % (OLDCONFIGFILE, configfile), file=sys.stderr)
        shutil.move(OLDCONFIGFILE, configfile)

    # 2. Copy contents of logfile to sqlite
    if os.path.exists(PROCESSED_FILE_LIST):
        print("Migrating old submit log to sqlite", file=sys.stderr)
        conn = sqlite3.connect(dbfile)
        c = conn.cursor()
        for l in open(PROCESSED_FILE_LIST).readlines():
            l = l.strip()
            query = """insert into filelog(filename) values(?)"""
            c.execute(query, (l.decode("utf-8"), ))
        conn.commit()
        os.unlink(PROCESSED_FILE_LIST)

def get_config_dir():
    confdir = os.path.join(os.path.expanduser("~"), ".abzsubmit")
    return confdir

def get_sqlite_file():
    dbfile = os.path.join(get_config_dir(), "filelog.sqlite")
    return dbfile

def load_settings():
    if not os.path.exists(get_config_dir()):
        os.makedirs(get_config_dir())

    dbfile = get_sqlite_file()
    if not os.path.exists(dbfile):
        create_sqlite(dbfile)
    if os.path.exists(OLDCONFIGFILE) or os.path.exists(PROCESSED_FILE_LIST):
        migrate_old_settings(dbfile)

    defaultfile = "abz/default.conf"
    configfile = os.path.join(get_config_dir(), CONFIG_FILE)
    config = ConfigParser.RawConfigParser()
    config.read(defaultfile)
    if os.path.exists(configfile):
        config.read(configfile)

    settings["host"] = config.get("acousticbrainz", "host")

    essentia = config.get("essentia", "path")
    if not os.path.isabs(essentia):
        essentia = os.path.abspath(os.path.expanduser(essentia))
    if not os.path.exists(essentia):
        raise Exception ("Cannot find the extractor %r" % essentia)

    h = hashlib.sha1()
    h.update(open(essentia, "rb").read())
    settings["essentia_path"] = essentia
    settings["essentia_build_sha"] = h.hexdigest()

    extensions = config.get("acousticbrainz", "extensions")
    extensions = [".%s" % e.lower() for e in extensions.split()]
    settings["extensions"] = tuple(extensions)
