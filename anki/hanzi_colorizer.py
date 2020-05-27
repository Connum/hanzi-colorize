#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# hanzi_colorizer.py is part of hanzi-colorize which makes HanziVG data
# into colored stroke order diagrams; this is the anki2 addon file.
#
# Copyright 2018 hanzi-colorize repository contributors
# based on kanji-colorize, Copyright 2012 Cayenne Boyer
#
# The code to do this automatically when the Hanzi field is exited was
# originally based on the Japanese support reading generation addon by
# Damien Elmes
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

# Installation: copy this file and the hanzicolorizer directory to your
# Anki addons folder.

# Usage: Add a "Diagram" field to a model with "Chinese" or "Mandarin"
# in the name and a field named "Hanzi".  When you finish editing the
# hanzi field, if it contains precisely one character, a colored stroke
# order diagram will be added to the Diagram field in the same way that
# the Japanese support plugin adds readings.
#
# To add diagrams to all such fields, or regenerate them with new
# settings, use the "Hanzi Colorizer: (re)generate all" option in the
# tools menu.


from anki.hooks import addHook
from aqt import mw
from aqt.utils import showInfo, askUser
from aqt.qt import *
from .hanzicolorizer.colorizer import (KanjiVG, KanjiColorizer,
                                      InvalidCharacterError)

# Configuration

addon_config = mw.addonManager.getConfig(__name__)

config = "--mode "
config += addon_config["mode"]
if addon_config["group-mode"]:
  config += " --group-mode "
config += " --saturation "
config += str(addon_config["saturation"])
config += " --value "
config += str(addon_config["value"])
config += " --image-size "
config += str(addon_config["image-size"])

modelNameSubstring = ['chinese','mandarin','hanzi']
srcField = ['Hanzi', 'Word (in Kanji/Hanzi)', 'Word (in Hanzi)']
dstField = ['Diagram', 'Stroke Order Diagram 1', 'Stroke order diagram (if you\'d like to test stroke order)', 'Stroke Order Diagram 1 (And component parts/mnemonics for meaning)']

# avoid errors due to invalid config
if 'model' in addon_config and type(addon_config['model']) is str:
    modelNameSubstring = [addon_config['model'].lower()]
if 'model' in addon_config and isinstance(addon_config['model'], list):
    modelNameSubstring = addon_config['model']
if 'src-field' in addon_config and type(addon_config['src-field']) is str:
    srcField = [addon_config['src-field']]
if 'src-field' in addon_config and isinstance(addon_config['src-field'], list):
    srcField = addon_config['src-field']
if 'dst-field' in addon_config and type(addon_config['dst-field']) is str:
    dstField = [addon_config['dst-field']]
if 'dst-field' in addon_config and isinstance(addon_config['dst-field'], list):
    dstField = addon_config['dst-field']

kc = KanjiColorizer(config)


def modelIsCorrectType(model):
    global modelNameSubstring
    global srcField
    global dstField
    
    '''
    Returns True if model has Chinese or Mandarin in the name and has both srcField
    and dstField; otherwise returns False
    '''
    # Does the model name have Chinese or Mandarin in it?
    model_name = model['name'].lower()
    fields = mw.col.models.fieldNames(model)

    isValidModel = False
    hasValidSrcField = False
    hasValidDstField = False
    
    if isinstance(modelNameSubstring, list):
        for f in modelNameSubstring:
            if f.lower() in model_name:
                isValidModel = True
                break
    else:
        hasValidSrcField = modelNameSubstring in model_name

    if isinstance(srcField, list):
        for f in srcField:
            if f in fields:
                hasValidSrcField = True
                break
    else:
        hasValidSrcField = srcField in fields

    if isinstance(dstField, list):
        for f in dstField:
            if f in fields:
                hasValidDstField = True
                break
    else:
        hasValidDstField = dstField in fields

    return (isValidModel and hasValidSrcField and hasValidDstField)


def characters_to_colorize(s):
    '''
    Given a string, returns a list of characters to colorize

    If the string consists of only a single character, returns a list
    containing that character.  If it is longer, returns a list of  only the
    hanzi.

    '''
    if len(s) <= 1:
        return list(s)
    return [c for c in s if ord(c) >= 19968 and ord(c) <= 40879]


def addKanji(note, flag=False, currentFieldIndex=None):
    '''
    Checks to see if a hanzi should be added, and adds it if so.
    '''
    if not modelIsCorrectType(note.model()):
        return flag
        
    fields = mw.col.models.fieldNames(note.model())

    if isinstance(srcField, list):
        for f in srcField:
            if f in fields:
                hasValidSrcField = True
                useSrcField = f
                break
    else:
        useSrcField = srcField

    if isinstance(dstField, list):
        for f in dstField:
            if f in fields:
                hasValidDstField = True
                useDstField = f
                break
    else:
        useDstField = dstField

    if currentFieldIndex != None: # We've left a field
        # But it isn't the relevant one
        if note.model()['flds'][currentFieldIndex]['name'] != useSrcField:
            return flag

    srcTxt = mw.col.media.strip(note[useSrcField])

    oldDst = note[useDstField]
    dst=''

    for character in characters_to_colorize(str(srcTxt)):
        # write to file; anki works in the media directory by default
        try:
            filename = KanjiVG(character).ascii_filename
        except InvalidCharacterError:
            # silently ignore non-Japanese characters
            continue
        char_svg = kc.get_colored_svg(character).encode('utf_8')
        anki_fname = mw.col.media.writeData(filename, char_svg)
        dst += '<img src="{!s}">'.format(anki_fname)

    if dst != oldDst and dst != '':
        note[useDstField] = dst
        note.flush()
        return True

    return flag


# Add a colorized hanzi to a Diagram whenever leaving a Hanzi field

def onFocusLost(flag, note, currentFieldIndex):
    return addKanji(note, flag, currentFieldIndex)

addHook('editFocusLost', onFocusLost)


# menu item to regenerate all

def regenerate_all():
    # Find the models that have the right name and fields; faster than
    # checking every note
    if not askUser("Do you want to regenerate all hanzi diagrams? "
                   'This may take some time and will overwrite the '
                   'destination Diagram fields.'):
        return
    models = [m for m in mw.col.models.all() if modelIsCorrectType(m)]
    # Find the notes in those models and give them hanzi
    for model in models:
        for nid in mw.col.models.nids(model):
            addKanji(mw.col.getNote(nid))
    showInfo("Done regenerating colorized hanzi diagrams!")

# add menu item
do_regenerate_all = QAction("Hanzi Colorizer: (re)generate all", mw)
do_regenerate_all.triggered.connect(regenerate_all)
mw.form.menuTools.addAction(do_regenerate_all)
