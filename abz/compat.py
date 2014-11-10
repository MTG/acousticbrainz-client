# Copyright 2014 Music Technology Group - Universitat Pompeu Fabra
# acousticbrainz-client is available under the terms of the GNU
# General Public License, version 3 or higher. See COPYING for more details.

"""python 2/3 compatibility"""


import sys


is_py2 = (sys.version_info[0] == 2)
is_py3 = (sys.version_info[0] == 3)


if is_py2:
    from urlparse import urlunparse
    from ConfigParser import RawConfigParser
else:
    from urllib.parse import urlunparse
    from configparser import RawConfigParser


def decode(msg):
    """decode if msg is a byte string, no-op otherwise
    """
    if isinstance(msg, bytes):
        return msg.decode("utf-8", "replace")
    else:
        return msg
