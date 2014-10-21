#!/usr/bin/env python

import os
import sys
import json
from math import fabs

ERR_THRESHOLD = 0.0001 # range 0 - 1.0

def traverse(path, jdata1, jdata2):
    if type(jdata1) is dict:
        for k in sorted(jdata1.keys()):
            path.append(k)
            if not jdata2.has_key(k):
                print "json2 is missing %s" % (":".join(path))
                sys.exit(-1)

            traverse(path, jdata1[k], jdata2[k])
            path.pop()
        return

    if type(jdata1) is list:
        for i, item in enumerate(jdata1):
            path.append("%d" % i)
            try:
                dummy = jdata2[i]
            except IndexError:
                print "json2 is missing %s" % (":".join(path))
                sys.exit(-1)
            traverse(path, item, jdata2[i])
            path.pop()
        return

    if type(jdata1) is float:
        if jdata1 != jdata2:
            err = (jdata1 - jdata2) / ((jdata1 + jdata2) / 2)
            if err > ERR_THRESHOLD:
                print "%s : '%s' vs '%s' (%.3f%% err)" % (":".join(path), repr(jdata1), repr(jdata2), err * 100)
    elif type(jdata1) is int:
        if jdata1 != jdata2:
            err = (jdata1 - jdata2) / ((jdata1 + jdata2) / 2.0)
            if err > ERR_THRESHOLD:
                print "%s : '%d' vs '%d' (%.3f%% err)" % (":".join(path), jdata1, jdata2, err * 100)
    elif repr(jdata1) != repr(jdata2):
        print "%s : '%s' vs '%s'" % (":".join(path), repr(jdata1), repr(jdata2))

if len(sys.argv) < 3:
    print "Usage: %s <json file 1> <json file 2>" % sys.argv[0]
    sys.exit(-1)

try:    
    f1 = open(sys.argv[1], "r")
    json1 = f1.read()
    f1.close()
except IOError, e:
    print "Cannot open %s: %s" % (sys.argv[1], e)
    sys.exit(-1)

try:    
    f2 = open(sys.argv[2], "r")
    json2 = f2.read()
    f2.close()
except IOError, e:
    print "Cannot open %s: %s" % (sys.argv[1], e)
    sys.exit(-1)

try:
    jdata1 = json.loads(json1)
except ValueError, e:
    print "Cannot parse JSON 1: %s" % e
    sys.exit(-1)

try:
    jdata2 = json.loads(json2)
except ValueError, e:
    print "Cannot parse JSON 2: %s" % e
    sys.exit(-1)

traverse([], jdata1, jdata2)
