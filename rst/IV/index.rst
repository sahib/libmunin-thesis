***************
Implementierung
***************


.. epigraph::


    '' *Programmieren Sie immer so, als wäre der Typ, der den Code pflegen muss, ein
    gewaltbereiter Psychopath, der weiß, wo Sie wohnen.* ''

    -- *Peter Stöhr*

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


Kurze Implementierungshistorie
==============================

Probleme:

    - Graphenaufbau (combinations = teuer) 
    - Festlegung von distance_add funktionsweise

Liste verfügbarer Provider und Distanzfunktionen
================================================

pass

Paketübersicht
==============


.. code-block:: bash

   $ tree -I '__pycache__' munin/

::

    munin/
    |---- __init__.py                     | Versionierungs Info
    |---- __main__.py                     | Beispielprogramm
    |---- database.py                     | Manager für alle vorhandenen Songs
    |---- dbus_service.py                 | [Unfertiger] Dbus Service für libmunin
    |---- dbus_client.py                  | [Unfertiger] DBus Client
    |---- distance/                       | Unterverzeichnis für Distanzfunktionen
    |   |---- __init__.py                 | Oberklasse für jede Distanzfunktion
    |   |---- bpm.py                      | BeatsPerMinute Distanzfunktion
    |   |---- date.py                     | ...
    |   |---- ...                         | 
    |---- session.py                      | Implementierung der Session (API)
    |---- easy.py                         | Vereinfachte Session-API
    |---- graph.py                        | Implementiert Graphenoperationen
    |---- helper.py                       | Verschiedene Utilityfunktionen
    |---- history.py                      | Implementierung beider Histories 
    |                                     | und Assoziationsregeln
    |---- plot.py                         | Visualisierungsfunktionen
    |---- provider/                       | Unterverzeichnis für alle Provider
    |   |---- __init__.py                 | Oberklasse für jeden Provider
    |   |---- bpm.py                      | BeatsPerMinute Provider
    |   |---- composite.py                | ...
    |   |---- ...                         | 
    |---- rake.py                         | Implementierung des RAKE Algorithmus
    |---- scripts/                        | Verschiedene eigenständige Helper
    |   |---- moodbar_visualizer.py       | Visualisiert ein moodbar-output
    |   |---- moodbar_walk.py             | Berechnet die moodbar parallel für
    |                                     | jedes Audiofile in einem Verzeichnis
    |---- song.py                         | Implementierung der Song Klasse
    |---- stopwords/                      | 
    |   |---- __init__.py                 | Stoppwort Implementierung
    |   |---- data                        | Stoppwort Datenbank
    |   |   |---- de                      | Jede Datei beeinhaltet pro Zeile
    |   |   |---- en                      | eine Stoppowrt der jeweiligen Sprache
    |   |   |---- es                      | ISO 638-1 Language Code.
    |   |   |---- ...                     |
    |---- testing.py                      | Fixtures und Helper für unittests
    

Anwendungsbeispiel
==================

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


Ist *libmunin* korrekt installiert, so lässt sich dieses Skript überall ablegen
und folgendermaßen ausführen:

.. code-block:: bash

    $ python example.py
    ('Vogelfrey'  , 'Wiegenfest'       , 'Heldentod'      , 'folk metal'),
    ('Debauchery' , 'Continue to Kill' , 'Apostle of War' , 'brutal death')

Kurze Erklärung des Beispiels 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Kurze Erklärung des Outputs
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Der Output ist nicht weiter überraschend: Da sich nur das Genre effektiv
vergleichen lässt und wir uns von dem ersten Song (,, *Trugbild* '') zwei
Empfehlungen geben ließen werden die zwei Songs mit dem ähnlichsten Genre
ausgegeben.

[TODO: Den Mini-Graph einfügen]


Statistiken
===========

LoC Statistiken:

.. code-block:: bash

          65 text files.
          63 unique files.                              
          19 files ignored.

    http://cloc.sourceforge.net v 1.60  T=0.34 s (135.8 files/s, 26868.3 lines/s)
    -------------------------------------------------------------------------------
    Language                     files          blank        comment           code
    -------------------------------------------------------------------------------
    Python                          46           2063           2169           4867
    -------------------------------------------------------------------------------
    SUM:                            46           2063           2169           4867
    -------------------------------------------------------------------------------
Dazu kommen einige weitere Zeilen von *reStructuredText* die die Basis der
Onlinedokumentation bilden:

.. code-block:: bash

    $ wc -l $(find . -iname '*.rst') | tail -1
    2231 insgesamt


Zudem lassen sich einige Statistiken präsentieren die automatisch aus den
``git log`` entstanden sind:

    - GitHub Visualisierungen:
      
        https://github.com/sahib/libmunin/graphs

    - ``gitstats`` Visualisierungen:
      
        http://sahib.github.io/libmunin-thesis/gitstats/index.html

    - ``gource`` Commit-Graph Visualisierung:

        ... TODO ...
