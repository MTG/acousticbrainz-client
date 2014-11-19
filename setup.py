#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    import warnings
    warnings.warn(
        "Installing with distutils. You will need to run `pip install requests` "
        "to install additional requirements")
    from distutils.core import setup

setup(
    name="abzsubmit",
    version='0.2dev',
    description="Submission client for AcousticBrainz project",
    author="Universitat Pompeu Fabra",
    author_email="alastair.porter@upf.edu",
    url="http://acousticbrainz.org",
    packages=['abz'],
    package_data={'abz': ['default.conf']},
    scripts=['abzsubmit'],
    data_files=[('bin', ['streaming_extractor_music'])],
    install_requires=['requests>2.4'],
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
