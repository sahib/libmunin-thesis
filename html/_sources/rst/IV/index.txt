***************
Implementierung
***************


.. epigraph::


    '' *Programmieren Sie immer so, als wäre der Typ, der den Code pflegen muss, ein
    gewaltbereiter Psychopath, der weiß, wo Sie wohnen* ''

    -- *Peter Stöhr*


Übersicht
=========

::

    munin/
    |---- __init__.py                     # Version Info
    |---- __main__.py                     # Contains an example program
    |---- database.py                     # Implements all TODO
    |---- dbus_client.py
    |---- dbus_service.py
    |---- distance/
    |   |---- __init__.py
    |   |---- bpm.py
    |   |---- date.py
    |   |---- genre.py
    |   |---- keywords.py
    |   |---- levenshtein.py
    |   |---- moodbar.py
    |   |---- rating.py
    |   |---- wordlist.py
    |---- easy.py
    |---- graph.py
    |---- helper.py
    |---- history.py
    |---- plot.py
    |---- provider/
    |   |---- __init__.py
    |   |---- bpm.py
    |   |---- composite.py
    |   |---- date.py
    |   |---- generate_genre_list.py
    |   |---- genre.list
    |   |---- genre.py
    |   |---- keywords.py
    |   |---- moodbar.py
    |   |---- normalize.py
    |   |---- stem.py
    |   |---- wordlist.py
    |---- rake.py
    |---- scripts/
    |   |---- moodbar_visualizer.py
    |   |---- moodbar_walk.py
    |---- session.py
    |---- song.py
    |---- stopwords/                     # Stopword supoort
    |   |---- data                       # Stopworddatabase 
    |   |   |---- de                     # Each file contains a newline separated
    |   |   |---- en                     # list of stopwords. 
    |   |   |---- es                     # File name is the ISO 638-1 language code.
    |   |   |---- …
    |   |---- __init__.py
    |---- testing.py

    5 directories, 57 files
    
Entwicklungsumgebung
====================

Als Programmiersprache wurde *Python* aus folgenden Gründen ausgewählt:

* Exzellenter Support für *Rapid Prototyping* - eine wichtige Eigenschaft bei
  nur knapp 3 Monaten Implementierungs-Zeit.
* Große Zahl an nützlichen Libraries, besonders für den wissenschaftlichen Einsatz.
* Neben *C* die *Lingua Franca* des Autors.

Alle Quellen die während dieses Projektes entstanden sind finden sich auf der
sozialen Code-Hosting Plattform Github. Der Vorteil dieser Plattform besteht
darin dass sie von sehr vielen Entwicklern besucht werden, die die Software
ausprobieren und möglicherweise verbessern oder zumindestens die Seite für
spätere Projekte bookmarken.  Daher auch Github's Slogan *Social Coding*.

Die dazugehörige Dokumentation wird bei jedem commit automatisch aus den
Sourcen, mittels des freien Dokumentationsgenerators Sphinx, auf der
Dokumentations-Hosting Plattform *ReadTheDocs* gebaut und dort verfügbar
gemacht: https://libmunin.rtfd.org

Zudem werden pro Commit unittests auf der Continious-Integration Plattform
*TravisCI* für verschiedene Python-Versionen durchgeführt.  Dies hat den Vorteil
dass fehlerhafte Versionen aufgedeckt werden, selbst wenn man vergessen hat die
unittests lokal durchzuführen.

Schlägt der Build fehl so färben sich kleine Buttons in den oben genannten
Diensten rot und man wird per Mail benachrichtigt. (Siehe :num:`fig-travis-badge`)

.. _fig-travis-badge:

.. figure:: figs/travis_badge.png
    :align: center
    :alt: Screenshot der Statusbuttons auf der Github-Seite.

    Screenshot der Statusbuttons auf der Github-Seite.

Versionen die als stabil eingestuft werden, werden auf *PyPi (Python Package Index)*
veröffentlicht, wo sie mithilfe des folgenden Befehles samt
Python-Abhängigkeiten installiert werden können:

.. code-block:: bash

    $ sudo pip install libmunin

Auf lokaler Seite wird jede Änderungen versioniert, um die Fehlersuche zu
vereinfachen - im Notfall kann man stets auf funktionierende Versionen
zurückgehen. 

Der Quelltext selber wird in *gVim* geschrieben. Dass sich der Python-Quelltext
dabei an die gängigen Konventionen hält wird durch die Zusatzprogramme *PEP8*
und *flake8* überprüft.


Historie
========

Putting it together
===================

.. code-block:: python
    :linenos:
    :emphasize-lines: 1,3,11,12,14,21

    from munin.easy import EasySession

    MY_DATABASE = [
        # Artist:            Album:               Title:             Genre:
        ('Akrea'          , 'Lebenslinie'      , 'Trugbild'       , 'death metal'),
        ('Vogelfrey'      , 'Wiegenfest'       , 'Heldentod'      , 'folk metal'),
        ('Letzte Instanz' , 'Götter auf Abruf' , 'Salve te'       , 'folk rock'),
        ('Debauchery'     , 'Continue to Kill' , 'Apostle of War' , 'brutal death')
    ]

    session = EasySession()
    with session.transaction():
        for idx, (artist, album, title, genre) in enumerate(MY_DATABASE):
             session.mapping[session.add({
                 'artist': artist,
                 'album': album,
                 'title': title,
                 'genre': genre
             })] = idx

    for munin_song in session.recommend_from_seed(session[0], 2):
        print(MY_DATABASE[munin_song.uid])


The output of this little wonder should be:

.. code-block:: python

    ('Vogelfrey'  , 'Wiegenfest'       , 'Heldentod'      , 'folk metal'),
    ('Debauchery' , 'Continue to Kill' , 'Apostle of War' , 'brutal death')

