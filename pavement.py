#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# pavement.py is part of hanzi-colorize which makes Hanzi data into
# colored stroke order diagrams
#
# Copyright 2018 hanzi-colorize repository contributors
# based on kanji-colorize, Copyright 2012 Cayenne Boyer
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this program.  If not, see
# <http://www.gnu.org/licenses/>.

from paver.easy import *
from paver.setuputils import setup
import zipfile


options(
    anki=Bunch(
        builddir=path('build') / 'anki_addon',
        zip=path('dist') / 'HanziColorizerAnkiAddon.zip'))


setup(
    name='HanziColorizer',
    description='script and module to create colored stroke order '
        'diagrams based on HanziVG data',
    long_description=open('README.rst').read(),
    version='0.11dev',
    author='Cayenne',
    author_email='connum+github@gmail.com',
    url='http://github.com/Connum/hanzi-colorize',
    packages=['hanzicolorizer'],
    scripts=['hanzi_colorize.py'],
    package_data={'hanzicolorizer': ['data/hanzivg/hanzi/*.svg']},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU Affero General Public License '
            'v3 or later (AGPLv3+)',
        'Programming Language :: Python',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Education',
        'Topic :: Multimedia :: Graphics' ])


@task
@needs('generate_setup', 'minilib', 'setuptools.command.sdist')
def sdist():
    pass


@task
def clean_anki_addon(options):
    if options.anki.builddir.exists():
        options.anki.builddir.rmtree()


@task
@needs('setuptools.command.build', 'clean_anki_addon')
def build_anki_addon(options):

    import argparse
    import colorsys

    # somewhere to put things
    options.anki.builddir.makedirs()

    # add addon files
    (path('anki') / 'hanzi_colorizer.py').copy(options.anki.builddir)
    lib_path = path('build') / 'lib' / 'hanzicolorizer'
    lib_path.copytree(options.anki.builddir / 'hanzicolorizer')

    # add required modules, minus the c in .pyc to get .py files
    path(argparse.__file__[:-1]).copy(options.anki.builddir)
    path(colorsys.__file__[:-1]).copy(options.anki.builddir)

    # add licenses
    license_dest = options.anki.builddir / 'hanzicolorizer' / 'licenses'
    path('licenses').copytree(license_dest)


@task
@needs('build_anki_addon')
def dist_anki_addon(options):
    print("create addon zip at " + options.anki.zip)
    with zipfile.ZipFile(options.anki.zip, 'w') as addon_zip:
        for file in options.anki.builddir.walkfiles():
            addon_zip.write(file, options.anki.builddir.relpathto(file))
