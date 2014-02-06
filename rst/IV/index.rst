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

Insgesamt wurden 13 unterschiedliche Provider implementiert - davon variieren
einige allerdings nur in Details. Dazu gesellen sich 9 Distanzfunktionen - auch
manche davon unterscheiden sich nur in ihrer Fusionierungsmethode.

Liste der Provider
------------------

#. ``Date``
#. ``Moodbar``
#. ``Rating``
#. ``BPM``
#. ``GenreTreeAvgLink``, ``GenreTree``
#. ``Wordlist``, ``Levenshtein``, ``Keywords``

Liste der Distanzfunktionen
---------------------------

#. ``Date``
#. ``Moodbar``
#. ``Wordlist``
#. ``BPM``
#. ``Normalize``, ``ArtistNormalize``, ``AlbumNormalize``
#. ``Composite``
#. ``Stem``
#. ``GenreTree``
#. ``Keywords``
#. ``PlyrLyrics``, ``DiscogsGenre``


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

Kurze Erläuterung des Beispiels 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* **Zeile 1:** 
  
  Der Einstiegspunkt von *libmunin's* API ist immer eine *Session*.
  Da die Konfiguration einer solchen (Auswahl von Provider, Distanzfunktionen
  und Weighting) mitunder recht anstrengend werden kann greifen wir auf eine
  Session mit vorgefertigter :term:`Maske` zurück - die sogenannte
  ``EasySession``.
  
* **Zeile 3:**

  Hier erstellen wir uns eine Pseudo-Datenbank aus vier Liedern mit vier
  einzelnen Attributen jeweils.

* **Zeile 11:** 

  Hier wird die oben erwähnte ``EasySession`` instanziert. Sie dient uns jetzt
  als *Sitzung* - alle relevanten Methoden von *libmunin* können auf der
  *Session* aufgerufen werden.

* **Zeile 12:**

  Bein initialen Importieren der Datenbank werden alle Songs über die ``add``
  Operation hinzugefügt. Da ``add`` noch keine Verbindungen zwischen den
  einzelnen Songs herstellt stellen wir mit dieser Zeile sicher nach dem
  Importieren ein ``rebuild`` ausgeführt wird.

* **Zeile 14:**

  Wir iterieren (**Zeile 13**) über alle Songs in unserer Pseudo-Datenbank und 
  fügen diese der *Session* hinzu (über die ``add`` Operation). Ein Problem dass
  man bei der Benutzung der Library hat ist: *libmunin* und der Nutzter halten
  zwei verschiedene Datenbanken im Speicher. Der Benutzer verwaltet die
  Originaldaten mit denen er arbeitet während *libmunin* nur normalisierte Daten
  speichert. Empfehlungen werden aber immer als

    This is perhaps the hardest line to grok. With ``session.add`` we add a
    single song to the Session. ``session.add`` expects a dictionary with keys 
    (the keys are pre-defined in the case of ``EasySession``, but can be
    configured in the normal session) and the values you want to set per song.

    Internally for each dictionary a :class:`munin.song.Song` will be created -
    a readonly mapping with normalized version of the values you passed.
    *Normalized* you ask? How? Well, let's introduce a new verb: A *Provider*
    can normalize a value for a certain *Attribute* (e.g. ``'artist'``) in a way
    that comparing values with each other gets faster and easier. More on that
    later.

    Now, what about that ``session.mapping`` thing? You might not have noticed
    it, but *libmunin* has an internal representation of songs which differs
    from the songs in ``MY_DATABASE``. Since recommendations are given in the
    internal representation, you gonna need to have a way to map those back to
    the actual values. ``session.mapping`` is just a dictionary with the only
    plus that it gets saved along with the session. In our example we take the
    return value from ``session.add`` (the *UID* of a song - which is an
    integer) and map it to the index in ``MY_DATABASE``.

    More on that in Part 4_.

    *Tip:* Try to keep the database index and the *UID* in sync.

* **Zeile 21:**

    In these two lines we do what *libmunin* is actually for - recommending songs.
    Most API-calls take either a song (a :class:`munin.song.Song`) or the *UID* we
    got from :func:`add`. ``session.recommend_from_seed`` takes two arguments. A
    song we want to get recommendations from, and how many we want. In this case
    we want two recommendations from the first song in the database (the one by
    *Akrea*). If we want to transform an *UID* to a full-fledged Song, wen can use 
    the ``__getattr__`` of Session::

      >>> session[0]
      <munin.song.Song(...)>

    But since we can pass either *UIDs* or the lookuped song, these two lines 
    are completely equal::

      >>> session.recommend_from_seed(session[0], 2)
      >>> session.recommend_from_seed(0, 2)

    The function will return an iterator that will lazily yield a
    :class:`munin.song.Song` as a recommendation.


Kurze Erläuterung des Outputs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

    $ wc -l $(find . -iname '*.rst')
    2231 insgesamt


Zudem lassen sich einige Statistiken präsentieren die automatisch aus den
``git log`` entstanden sind:

    - GitHub Visualisierungen:
      
        https://github.com/sahib/libmunin/graphs

    - ``gitstats`` Visualisierungen:
      
        http://sahib.github.io/libmunin-thesis/gitstats/index.html

    - ``gource`` Commit-Graph Visualisierung:

        ... TODO ...
