Acousticbrainz client
---------------------

This client lets you submit your own audio features to the extracted project

Requirements
============

We use pytaglib to read your tags.
You also need requests to submit data

If you have audio files that you want to submit that don't have
MBID tags in them, you can also install acoustid and we will try
and identify the track by fingerprint.

Installation
------------

First, download the extractor related to your platform from here:

Or if you want to, compile your own version of essentia (see below)
Copy the extractor file into this directory.

And use setup.py to install the script:

    python setup.py install


Getting a feature extractor
---------------------------
We provide static builds of feature extractors for popular platforms. You can
download the one that you need and put it in this directory, or somewhere in
your PATH.
The extractor is provided as part of the essentia project. You can compile
your own extractor if you want. Just download essentia and compile it with examples

    ./waf configure --with-examples
    ./waf

and get the resulting file from `build/src/examples/streaming_extractor_music`

Running
-------

Run it like this:

    ./absubmit [some dirs] ...

and go and have a coffee

Configuration files:
-------------------

~/.abzsubmit.conf
~/.abzsubmit.log

If you want to have a custom location of the extractor file, you can edit your
`~/.abzsubmit.conf` file. Add or edit the section that looks like this:

```
[essentia]
path: /path/to/streaming_extractor_music
```

If you don't specify an absolute path, we will first look in $PATH, and then
the same directory as the submission script.

The log file lists each file that has been uploaded. This is so that the script
does not send updates twice for the same file. When you have finished uploading
features you can delete this file.

License
-------
This application is Copyright Music Technology Group, Universitat Pompeu Fabra.
It is available under the terms of the GNU GPL v3+. See COPYING for details.
