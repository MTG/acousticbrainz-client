# Copyright 2014 Music Technology Group - Universitat Pompeu Fabra
# acousticbrainz-client is available under the terms of the GNU
# General Public License, version 3 or higher. See COPYING for more details.

has_acoustid = False
try:
    import acoustid
    has_acoustid = True
except ImportError:
    pass

def get_recordingid_for_file(filepath):
    pass
