# Copyright 2014 Music Technology Group - Universitat Pompeu Fabra
# acousticbrainz-client is available under the terms of the GNU
# General Public License, version 3 or higher. See COPYING for more details.

from __future__ import print_function

import json
import os
import sqlite3
import subprocess
import sys
import tempfile
import uuid

try:
    import requests
except ImportError:
    from .vendor import requests

from abz import compat, config

config.load_settings()
conn = sqlite3.connect(config.get_sqlite_file())
VERBOSE = False

RESET = "\x1b[0m"
RED = "\x1b[31m"
GREEN = "\x1b[32m"


def _update_progress(msg, status="...", colour=RESET):
    if VERBOSE:
        sys.stdout.write("%s[%-10s]%s " % (colour, status, RESET))
        print(msg.encode("ascii", "ignore"))
    else:
        sys.stdout.write("%s[%-10s]%s " % (colour, status, RESET))
        sys.stdout.write(msg+"\x1b[K\r")
        sys.stdout.flush()


def _start_progress(msg, status="...", colour=RESET):
    print()
    _update_progress(msg, status, colour)


def add_to_filelist(filepath, reason=None):
    query = """insert into filelog(filename, reason) values(?, ?)"""
    c = conn.cursor()
    c.execute(query, (compat.decode(filepath), reason))
    conn.commit()


def is_valid_uuid(u):
    try:
        u = uuid.UUID(u)
        return True
    except ValueError:
        return False


def is_processed(filepath):
    query = """select * from filelog where filename = ?"""
    c = conn.cursor()
    r = c.execute(query, (compat.decode(filepath), ))
    if len(r.fetchall()):
        return True
    else:
        return False

def get_processed_status(filepath):
    query = """select reason from filelog where filename = ?"""
    c = conn.cursor()
    c.execute(query,(filepath,))
    processed_status = c.fetchone()
    return processed_status[0]

def run_extractor(input_path, output_path):
    extractor = config.settings["essentia_path"]
    profile = config.settings["profile_file"]
    args = [extractor, input_path, output_path, profile]

    p = subprocess.Popen(args, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    (out, err) = p.communicate()
    retcode = p.returncode
    return retcode, out


def submit_features(recordingid, features):
    featstr = json.dumps(features)

    host = config.settings["host"]
    url = compat.urlunparse(('http', host, '/%s/low-level' % recordingid, '', '', ''))
    r = requests.post(url, data=featstr)
    r.raise_for_status()


def process_file(filepath):
    _start_progress(filepath)
    if is_processed(filepath):
        processed_status = get_processed_status(filepath)
        if processed_status == None:
	        status = ":) done"
	        colour = GREEN
        else:
	        status = ":( nombid"
	        colour = RED
        _update_progress(filepath, status, colour)
        return

    fd, tmpname = tempfile.mkstemp(suffix='.json')
    os.close(fd)
    os.unlink(tmpname)
    retcode, out = run_extractor(filepath, tmpname)
    if retcode == 2:
        _update_progress(filepath, ":( nombid", RED)
        print()
        print(out)
        add_to_filelist(filepath, "nombid")
    elif retcode == 1:
        _update_progress(filepath, ":( extract", RED)
        print()
        print(out)
        add_to_filelist(filepath, "extractor")
    elif retcode > 0 or retcode < 0:  # Unknown error, not 0, 1, 2
        _update_progress(filepath, ":( unk %s" % retcode, RED)
        print()
        print(out)
    else:
        if os.path.isfile(tmpname):
            try:
                features = json.load(open(tmpname))
                # Recording MBIDs are tagged with _trackid for historic reasons
                recordingids = features["metadata"]["tags"]["musicbrainz_trackid"]
                if not isinstance(recordingids, list):
                    recordingids = [recordingids]
                recs = [r for r in recordingids if is_valid_uuid(r)]
                if recs:
                    recid = recs[0]
                    try:
                        submit_features(recid, features)
                    except requests.exceptions.HTTPError as e:
                        _update_progress(filepath, ":( submit", RED)
                        print()
                        print(e.response.text)
                    add_to_filelist(filepath)
                    _update_progress(filepath, ":)", GREEN)
                else:
                    _update_progress(filepath, ":( badmbid", RED)

            except ValueError:
                _update_progress(filepath, ":( json", RED)
                add_to_filelist(filepath, "json")

    if os.path.isfile(tmpname):
        os.unlink(tmpname)


def process_directory(directory_path):
    _start_progress("processing %s" % directory_path)

    for dirpath, dirnames, filenames in os.walk(directory_path):
        for f in filenames:
            if f.lower().endswith(config.settings["extensions"]):
                process_file(os.path.abspath(os.path.join(dirpath, f)))


def process(path):
    if not os.path.exists(path):
        sys.exit(path + " does not exist")
    path = os.path.abspath(path)
    if os.path.isfile(path):
        process_file(path)
    elif os.path.isdir(path):
        process_directory(path)


def cleanup():
    if os.path.isfile(config.settings["profile_file"]):
        os.unlink(config.settings["profile_file"])
