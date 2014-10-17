#!/usr/bin/env python

from distutils.core import setup

setup(
    name="abzsubmit",
    version='0.1',
    description="submission client for acousticbrainz project",
    author="Universitat Pompeu Fabra",
    author_email="alastair.porter@upf.edu",
    url="http://acousticbrainz.org",
    packages=['abz'],
    package_data={'abz': ['default.conf']},
    scripts = ['abzsubmit', 'streaming_extractor_music'],
    license='GPL3+',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Topic :: Multimedia :: Sound/Audio :: Analysis",
        "Topic :: Scientific/Engineering :: Information Analysis"
    ]
)

