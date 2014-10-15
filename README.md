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

FAQ
---

* __Why does Essentia need taglib and acousticbrainz-client also need pytaglib?:__ acousticbrainz-client uses pytaglib, first, to check if a file has a recording MBID before running Essentia. Essentia uses taglib for creating the 'tags' section of the output JSON.
* __Why not just use the MBID from the tags section of Essentia's JSON then?:__ Because Essentia takes a bit to run, and we'd rather not run it on a file we won't be able to submit.
* __Couldn't you do this some way that doesn't require running Essentia first but still doesn't require installing pytaglib to get this to work?:__ Yup, ideally we'd remove that extra dependency, and it's almost certainly possible. Pull requests welcome!
* __Where does the md5 in the generated data come from, and what does it include?:__ Essentia produces this value, using FFmpeg/LibAV's MD5 calculation functions, passing av\_read\_frame packets to it.
* __What about data that doesn't have recording MBIDs? Surely you can still do something with that.:__ Probably. But for now we aren't. We'd probably like non-MBID submissions to be possible, but determining the right way to index this sort of submission in external sources of metadata is a hard problem, and adding MBIDs to files isn't too hard for the pile of MusicBrainz editors we've been having run this code.

License
-------
This application is Copyright Music Technology Group, Universitat Pompeu Fabra.
It is available under the terms of the GNU GPL v3+. See COPYING for details.
