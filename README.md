Acousticbrainz client
---------------------

For more information about acousticbrainz, see http://acousticbrainz.org

This client lets you submit your own audio features to the acousticbrainz project.

Requirements
============

This client has been tested on linux
with python 2.6, 2.7, 3.1, 3.2, 3.3 and 3.4.

The only additional requirement is the python `requests` package.
On debian, ubuntu, and related distributions you can run

    $ sudo apt-get install python-requests

or install with pip:

    $ sudo pip install -r requirements.txt


Getting a feature extractor
---------------------------
To contribute data to acousticbrainz you first need an _extractor_. This is a
program that analyses your music and generates a file.

We provide static builds of extractors for popular platforms. Find one
for your platform here:

http://acousticbrainz.org/download

Put your extractor in this directory. These files require no additional dependencies.

We prefer that you use one of our provided extractors. This lets us be sure that different
versions of software don't cause variations in the data that we are collecting.
If you really want to, you can make your own, but note that this requires
a fair number of dependencies to compile. It will certainly be easier to use one of
our binaries to get started. 

The extractor is provided as part of the [essentia project](http://essentia.upf.edu/).
To build it, download essentia and compile the examples. 

    git clone https://github.com/MTG/essentia.git
    cd essentia
    ./waf configure --with-example=streaming_extractor_music
    ./waf

and get the resulting file from `build/src/examples/streaming_extractor_music`

Installation
------------

First, download the extractor related to your platform and put it in
this directory.

You can run `./abzsubmit` from this directory, or install it:

    sudo python setup.py install

and run `abzsubmit` from any shell.


Running
-------

Run it like this:

    ./abzsubmit [some dirs] ...

and go and have a coffee. :-)

Configuration files:
-------------------

~/.abzsubmit/abzsubmit.conf
~/.abzsubmit/filelog.sqlite

If you want to `abzsubmit` to look in a custom location for your extractor program, you can edit your
`~/.abzsubmit.conf` file. Add or edit the section that looks like this:

```
[essentia]
path: /path/to/streaming_extractor_music
```

If you don't specify an absolute path, we will first look in `$PATH`, and then
the same directory as the submission script, `abzsubmit`.

The sqlite database is used to keep track of uploaded files so that they are
not submitted twice.

FAQ
---

* __Where does the md5 in the generated data come from, and what does it include?:__ Essentia produces this value, using FFmpeg/LibAV's MD5 calculation functions, passing av\_read\_frame packets to it.
* __What about data that doesn't have recording MBIDs? Surely you can still do something with that.:__ Probably. But for now we aren't. We'd probably like non-MBID submissions to be possible, but determining the right way to index this sort of submission in external sources of metadata is a hard problem, and adding MBIDs to files isn't too hard for the pile of MusicBrainz editors we've been having run this code.

License
-------
This application is Copyright Music Technology Group, Universitat Pompeu Fabra.
It is available under the terms of the GNU GPL v3+. See COPYING for details.
