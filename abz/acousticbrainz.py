# Copyright 2014 Music Technology Group - Universitat Pompeu Fabra
# acousticbrainz-client is available under the terms of the GNU
# General Public License, version 3 or higher. See COPYING for more details.

from __future__ import print_function

import json
import os
import subprocess
import tempfile
import urlparse
import uuid
import sqlite3

import requests
import taglib

import config

from sys import exit

config.load_settings()
conn = sqlite3.connect(config.get_sqlite_file())

def add_to_filelist(filepath, reason=None):
    query = """insert into filelog(filename, reason) values(?, ?)"""
    c = conn.cursor()
    r = c.execute(query, (filepath, reason))
    conn.commit()

def is_processed(filepath):
    query = """select * from filelog where filename = ?"""
    c = conn.cursor()
    r = c.execute(query, (filepath, ))
    if len(r.fetchall()):
        return True
    else:
        return False

def get_musicbrainz_recordingid(filepath):
    f = taglib.File(filepath)
    # Historically this was called _TRACKID, but it's a recording id
    if "MUSICBRAINZ_TRACKID" in f.tags:
        recordingid = f.tags["MUSICBRAINZ_TRACKID"]
        if len(recordingid) == 0:
            return None
        # TODO: If there's more than 1 recording id we don't know which
        # one is correct. Would this be an error?
        if isinstance(recordingid, list) and len(recordingid) > 0:
            recordingid = recordingid[0]
        try:
            u = uuid.UUID(recordingid)
            return recordingid
        except ValueError:
            return None

def run_extractor(input_path, output_path):
    """
    :raises subprocess.CalledProcessError: if the extractor exits with a non-zero
                                           return code
    """
    extractor = config.settings["essentia_path"]
    args = [extractor, input_path, output_path]
    subprocess.check_call(args)

def submit_features(recordingid, features):
    featstr = json.dumps(features)

    host = config.settings["host"]
    url = urlparse.urlunparse(('http', host, '/%s/low-level' % recordingid, '', '', ''))
    r = requests.post(url, data=featstr)
    r.raise_for_status()

def extractor_output_file_name(base):
    """
    Returns `base` + ".json" if that file exists and just `base` otherwise.
    """
    maybename = base + os.extsep + "json"
    if os.path.isfile(maybename):
        return maybename
    return base


def process_file(filepath):
    print("Processing file %s" % filepath)
    if is_processed(filepath):
        print(" * already processed, skipping")
        return
    recid = get_musicbrainz_recordingid(filepath)
    # TODO: We need to decide if this is lossless
    lossless = filepath.lower().endswith(".flac")

    if recid:
        print(" - has recid %s" % recid)
        fd, tmpname = tempfile.mkstemp(suffix='.json')
        os.close(fd)
        os.unlink(tmpname)
        try:
            run_extractor(filepath, tmpname)
        except subprocess.CalledProcessError as e:
            print(" ** The extractor's return code was %s" % e.returncode)
        else:
            tmpname = extractor_output_file_name(tmpname)
            features = json.load(open(tmpname))
            features["metadata"]["version"]["essentia_build_sha"] = config.settings["essentia_build_sha"]
            features["metadata"]["audio_properties"]["lossless"] = lossless

            try:
                submit_features(recid, features)
            except requests.exceptions.HTTPError as e:
                print(" ** Got an error submitting the track. Error was:")
                print(e.response.text)
            add_to_filelist(filepath)
        finally:
            tmpname = extractor_output_file_name(tmpname)
            if os.path.isfile(tmpname):
                os.unlink(tmpname)
    else:
        print(" - no recid")

def process_directory(directory_path):
    print("processing directory %s" % directory_path)

    for dirpath, dirnames, filenames in os.walk(directory_path):
        for f in filenames:
            if f.lower().endswith(config.settings["extensions"]):
                process_file(os.path.abspath(os.path.join(dirpath, f)))


def process(path):
    if not os.path.exists(path):
        exit(path + "does not exist")
    path = os.path.abspath(path)
    if os.path.isfile(path):
        process_file(path)
    elif os.path.isdir(path):
        process_directory(path)
