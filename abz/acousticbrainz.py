import json
import os
import subprocess
import tempfile
import urlparse
import uuid

import requests
import taglib

import config

from sys import exit

config.load_settings()

processed_files = set()
PROCESSED_FILE_LIST = os.path.expanduser("~/.abzsubmit.log")
def load_processed_filelist():
    global processed_files
    if os.path.exists(PROCESSED_FILE_LIST):
        fp = open(PROCESSED_FILE_LIST)
        lines = [l.strip() for l in list(fp)]
        processed_files = set(lines)

def add_to_filelist(filepath):
    # TODO: This will slow down as more files are processed. We should
    # keep an open file handle and append to it
    processed_files.add(filepath)
    fp = open(PROCESSED_FILE_LIST, "w")
    for f in processed_files:
        fp.write("%s\n" % f)
    fp.close()

def is_processed(filepath):
    return filepath in processed_files

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
    extractor = config.settings["essentia_path"]
    args = [extractor, input_path, output_path]
    p = subprocess.Popen(args)
    p.communicate()

def submit_features(recordingid, features):
    featstr = json.dumps(features)

    host = config.settings["host"]
    url = urlparse.urlunparse(('http', host, '/%s/low-level' % recordingid, '', '', ''))
    r = requests.post(url, data=featstr)

def process_file(filepath):
    print "Processing file", filepath
    if is_processed(filepath):
        print " * already processed, skipping"
        return
    recid = get_musicbrainz_recordingid(filepath)
    # TODO: We need to decide if this is lossless
    lossless = filepath.lower().endswith(".flac")

    if recid:
        print " - has recid", recid
        fd, tmpname = tempfile.mkstemp()
        os.close(fd)
        os.unlink(tmpname)
        run_extractor(filepath, tmpname)
        # The extractor adds .json to the filename you give it, so
        # we don't pass that, and use it afterwards to read the file.
        # This is an abuse of mkstemp, sorry.
        tmpname = "%s.json" % tmpname

        features = json.load(open(tmpname))
        features["metadata"]["version"]["essentia_build_sha"] = config.settings["essentia_build_sha"]
        features["metadata"]["audio_properties"]["lossless"] = lossless

        submit_features(recid, features)

        os.unlink(tmpname)
        add_to_filelist(filepath)
    else:
        print " - no recid"

def process_directory(directory_path):
    print "processing directory", directory_path

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
