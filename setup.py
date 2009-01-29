#!/usr/bin/env python

from distutils.core import setup
import glob

setup (name = 'ie_shell',
       version = '0.0.3',
       description = """
Python shell and modules for exploration, searching and processing
of data files of Infinity Engine-based games
(Baldur's Gate, Icewind Dale, Planescape: Torment)""",
       author = 'Jarda Benkovsky',
       author_email = 'edheldil@users.sourceforge.net',
       url = 'http://www.eowyn.cz/ie_shell',
       scripts = ['iesh'],
       packages = ['infinity', 'infinity.formats'],
       data_files = [
                     ('share/doc/ie_shell', ['README', 'COPYING']),
                     ('share/doc/ie_shell/examples', glob.glob ('examples/*.py')),
                     ])

