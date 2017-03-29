from __future__ import absolute_import, division, print_function
from os.path import join as pjoin

# Format expected by setup.py and doc/source/conf.py: string of form "X.Y.Z"
_version_major = 0
_version_minor = 1
_version_micro = ''  # use '' for first of series, number for 1 and above
_version_extra = 'dev'
# _version_extra = ''  # Uncomment this for full releases

# Construct full version string from these.
_ver = [_version_major, _version_minor]
if _version_micro:
    _ver.append(_version_micro)
if _version_extra:
    _ver.append(_version_extra)

__version__ = '.'.join(map(str, _ver))

CLASSIFIERS = ["Development Status :: 3 - Alpha",
               "Environment :: Console",
               "Intended Audience :: Science/Research",
               "License :: OSI Approved :: Apache 2.0 License",
               "Operating System :: OS Independent",
               "Programming Language :: Python",
               "Topic :: Scientific/Engineering"]

# Description should be a one-liner:
description = "Functional gradients"
# Long description will go up on the pypi page
long_description = """

Functional gradients
========
This package contains code that reproduces results reported in  "Task-induced 
changes in neural acitivity are organized along multiple functional gradients".
The figures presented in the paper are post-processed versions of figures 
generated with this code.

License
=======
``functional gradients`` is licensed under the terms of the Apache 2.0 license. 
See the file "LICENSE" for information on the history of this software, terms 
& conditions for usage, and a DISCLAIMER OF ALL WARRANTIES.

All trademarks referenced herein are property of their respective holders.

Copyright (c) 2017--, Marcel Falkiewicz, Max Planck Institute for Human Cognitive
and Brain Sciences, Leipzig, Germany.
"""

NAME = "functional_gradients"
MAINTAINER = "Marcel Falkiewicz"
MAINTAINER_EMAIL = "mfalkiewicz@gmail.com"
DESCRIPTION = description
LONG_DESCRIPTION = long_description
URL = "http://github.com/mfalkiewicz/functional_gradients"
DOWNLOAD_URL = ""
LICENSE = "Apache 2.0"
AUTHOR = "Marcel Falkiewicz"
AUTHOR_EMAIL = "mfalkiewicz@gmail.com"
PLATFORMS = "OS Independent"
MAJOR = _version_major
MINOR = _version_minor
MICRO = _version_micro
VERSION = __version__
PACKAGE_DATA = {'functional_data': [pjoin('data', '*')]}
REQUIRES = ["numpy","mapalign","nibabel","h5py","pandas"]
