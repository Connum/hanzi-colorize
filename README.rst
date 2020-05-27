==============
HanziColorizer
==============

.. image:: kanji-colorize-examples.png

About
-----

``hanzi_colorize.py`` is a script for coloring, resizing, and renaming
the stroke order diagrams from the
`HanziVG <https://github.com/Connum/hanzivg/>`_ project.
It's basically a clone of `cayennes/kanji-colorize <https://github.com/cayennes/kanji-colorize>`_ written to create
sets that make it possibe to easily add stroke order diagrams to an
`anki <http://ankisrs.net/>`_ kanji deck, but they can be used for
anything you want some nicely colored stroke order diagrams for.

**CAUTION: I have not tested the pure script functionality yet, only the Anki addon integration!
Also, the python tests are currently failing because I haven't adapted them from KanjiVG to HanziVG yet!**

Using with Anki
---------------

There is an addon for Anki2 coming soon.
Meanwhile, read the "Development" section below.

Downloading and Running the Software
------------------------------------

The `hanzi_colorize.py` script makes it possible to generate diagrams to your
own specifications.  It may have issues with a python not built with
wide-character support

Feedback
--------

If there's anything you think would improve the Anki addon, you can use the
`issue tracker <https://github.com/Connum/hanzi-colorize/issues>`_ .

If you find an error in the stroke order data, please use the 
`HanziVG issue tracker <https://github.com/Connum/hanzivg/issues/`_ .

Development
-----------

Have you created an improvement to KanjiColorizer that you think
other people would also like to have?  If so, please submit a patch or a
pull request!  I'm not always very prompt but I do get to them
eventually.

Please make sure existing tests pass.  Even better, add new tests for
anything you add.  Either doctest or unittest is fine, though ideally
the doctests would contain executable examples that fully illustrate the
function and the unittest tests would contain further worthwhile checks.

Activate the virtual environment and install requirements:

.. code:: bash

    $ python3 -m venv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt

To run the existing tests:

.. code:: bash

    $ python -m kanjicolorizer.colorizer
    $ python -m unittest discover -s kanjicolorizer

To create a new release:

.. code :: bash

    $ paver dist_anki_addon

Test by unzipping the zip file in `dist` into a new directory in `~/.local/share/Anki2/addons21` (or the equivalent for the OS being tested).

License
-------

The code is available under the Affero GPL version 3 or later and the SVG
images are available under Creative Commons Attribution-Share Alike 3.0.
See file headers and files in ``licenses/`` for more information.
