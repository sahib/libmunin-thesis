***************
Implementierung
***************

.. epigraph::


    '' *Programmieren Sie immer so, als wäre der Typ, der den Code pflegen muss, ein
    gewaltbereiter Psychopath, der weiß, wo Sie wohnen.* ''

    -- *Peter Stöhr*

Kurze Implementierungshistorie
==============================

Probleme:

    - Graphenaufbau (combinations = teuer) 
    - Festlegung von distance_add funktionsweise

Parallel zur Implementierugn wurde ein ,,Tagebuch'' :cite:`THV` verfasst das
dazu dienen sollte Ideen und Geschehnisse festzuhalten - weniger als Information
für Dritte.

Liste verfügbarer Provider und Distanzfunktionen
================================================

Insgesamt wurden 13 unterschiedliche Provider implementiert - davon variieren
einige allerdings nur in Details. Dazu gesellen sich 9 Distanzfunktionen - auch
manche davon unterscheiden sich nur in ihrer Fusionierungsmethode.

Liste der Distanzfunktionen
---------------------------

Die genaue Berechnung der Distanz wird in der Bachelorarbeit betrachtet.

``Date``
~~~~~~~~

``Moodbar``
~~~~~~~~~~~

``Rating``
~~~~~~~~~~

``BPM``
~~~~~~~

``Wordlist``, ``Levenshtein``, ``Keywords``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``GenreTreeAvgLink``, ``GenreTree``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Liste der Distanzfunktionen
---------------------------

Die genaue Funtkionsweise der Provider wird in der Bachelorarbeitet betrachtet.
Im folgenden wird nur eine Auflistung verfügbarer Provider gegeben und welche
Eingabe sie erwarten sowie welche Ausgabe sie produzieren.


``Date``
~~~~~~~~

Wandelt und normalisiert ein Datum dass als String übergeben wird zu einer
Jahreszahl (*1975* beispielsweise). Dabei werden die häufigsten
Datum-Formattierungen automatisch erkannt. Dies ist nötig da je nach Region ganz
unterschiedliche Datumsangaben in den Audiofiles getaggt sind. 

``Moodbar``
~~~~~~~~~~~

Berechnet mit dem ``moodbar`` (TODO: zitieren) Programm aus einen beliebigen
Audio File einen Vektor mit 1000 RGB-Farbwerten. Jeder dieser Farbwerte
repräsentiert den Anteil niedriger Frequenzen (rot), mittlerer (grün) und
hoher Frequenzen (blau) in einem Tausendstel des Audiostücks. 

Obwohl man aus dem Namen dises Verfahren schließen könnte dass hier die
*Stimmung* im Lied angedeutet wird, kann man aus diesen Informationen
lediglich herauslesen wie ,,engergetisch'' ein Lied zu einem bestimmten
Zeitpunkt ist - mit etwas Glück kann man auch Instrumente erkennen - so ist
die Kombination von E-Gitarre und Drums oft ein helles Türkis.

Aus diesem RGB-Vektoren werden die prägnantesten Merkmale abgeleitet - die
dominaten Farben, der Stilleanteil (*schwarz*) und einige weitere Merkmale.

Dieser Provider kommt in drei verschiedenen Ausführungen daher die sich in dem
Typ ihrer Eingabe unterscheiden:

* ``Moodbar``: Nimmt eine Liste von 1000 RGB-Werten.
* ``MoodbarFile``: Nimmt ein Pfad zu einem von der ``moodbar`` erstellten Datei
  entgegen die einen Vektor aus 1000 RGB-Werten binär beeinhaltet.
* ``MoodbarAudioFile``: Nimmt ein Pfad zu einer beliebigen Audio-Datei entgegen
  und führt das ``moodbar``-Utility darauf aus falls noch keine weiter Datei mit
  demselben Pfad plus der zusätzlichen Endung ``.mood`` vorhanden ist.

``Wordlist``
~~~~~~~~~~~~

Bricht einen String in eine Liste von Wörter auf.

``BPM``
~~~~~~~

Berechnet die ,,Beats-Per-Minute'' eines Lieds (Zitieren) - dies funktioniert
nicht nur für stark beat-lastige Musikrichtungen wie Techno sondern auch für
normale Musikrichtungen. 

TODO: Hinweis auf bpm-tools

``Normalize``, ``ArtistNormalize``, ``AlbumNormalize``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``Composite``
~~~~~~~~~~~~~

Erlaubt das Verketten von Providern. Er erste Eingabewert wird dem ersten
Provider in der Kette gegeben und die Ausgabe, ähnliche wie beiner Unix-Pipe, 
wird an den nächsten Provider in der Kette als Eingabe weitergegeben.

Ein Anwendungsbeispiel wäre das Zusammenschalten ::

    Eingabe: Artist, Album -> PlyrLyrics | Stem | Keywords -> Ausgabe: Stemmed Keywords

``Stem``
~~~~~~~~

``GenreTree``
~~~~~~~~~~~~~

Der wohl komplizierteste :term:`Provider`.

``Keywords``
~~~~~~~~~~~~

Extrahiert aus einem Text als Eingabe alle *relevanten* Stichwörter. 
Ein Beispiel dieser *Keywords* wird in :num:`fig-yellow-keywords` gezeigt.
Zudem wird die Sprache des Eingabetextes erkannt und mit abgespeichert.

.. _fig-yellow-keywords:

.. figtable::
    :caption: Die extrahierten Keywords aus ,,Yellow Submarine'', samt deren
              Rating.
    :alt: Extrahierte Keywords aus ,,Yellow Submarine''
    :spec: r l

    ====== =================================
    Rating Keywords 
    ====== =================================
    22.558 'yellow', 'submarin'
    20.835 'full', 'speed', 'ahead', 'mr'
     8.343 'live', 'beneath'
     5.247 'band', 'begin'
     3.297 'sea'
     3.227 'green'
     2.797 'captain'
           ...
    ====== ================================= 


``PlyrLyrics``
~~~~~~~~~~~~~~

Besorgt mittels *libglyr* Liedtexte aus dem Internet. Bereits gesuchte Liedtexte
werden dabei zwischengespeichert. Dieser :term:`Provider` eignet sich besonders im
Zusammenhang mit dem *Keywords* zusammen als *Composite* Provider.

``DiscogsGenre``
~~~~~~~~~~~~~~~~


Paketübersicht
==============

In der Programmiersprache *Python* entspricht jede einzelne ``.py`` Datei einem
*Modul*. Die Auflistung unter :num:`fig-module-tree` soll eine Übersicht darüber
geben welche Funktionen in welchem Modul implementiert worden.

.. _fig-module-tree:

.. figtable::
    :caption: Verzeichnisbaum mit den einzelnen Modulen von *libmunin*
    :alt: Verzeichnisbaum der Implementierung
    :spec: l l l l | l

    +-------------------+-------------------+-----------------+-------+---------------------------------------------+
    | **Verzeichnisse** | (gekürzt)         |                 |       | **Beschreibung**                            |
    +===================+===================+=================+=======+=============================================+
    | **munin/**        |                   |                 |       | Quelltextverzeichnis                        |
    +-------------------+-------------------+-----------------+-------+---------------------------------------------+
    |                   | *__init__.py*     |                 |       | Versionierungs Info                         |
    +-------------------+-------------------+-----------------+-------+---------------------------------------------+
    |                   | *__main__.py*     |                 |       | Beispielprogramm                            |
    +-------------------+-------------------+-----------------+-------+---------------------------------------------+
    |                   | *database.py*     |                 |       | Implementierung von ``Database``            |
    +-------------------+-------------------+-----------------+-------+---------------------------------------------+
    |                   | *dbus_service.py* |                 |       | Unfertiger DBus Service.                    |
    +-------------------+-------------------+-----------------+-------+---------------------------------------------+
    |                   | *dbus_client*     |                 |       | Unfertiger DBus Beispiel-Client.            |
    +-------------------+-------------------+-----------------+-------+---------------------------------------------+
    |                   | **distance/**     |                 |       | Unterverzeichnis für Distanzfunktionen      |
    +-------------------+-------------------+-----------------+-------+---------------------------------------------+
    |                   |                   | *__init__.py*   |       | Implementierung von ``DistanceFunction``    |
    +-------------------+-------------------+-----------------+-------+---------------------------------------------+
    |                   |                   | *bpm.py*        |       | Implementierung von ``BPMDistance``         |
    +-------------------+-------------------+-----------------+-------+---------------------------------------------+
    |                   |                   | *date.py*       |       | Implementierung von ``DateDistance``        |
    +-------------------+-------------------+-----------------+-------+---------------------------------------------+
    |                   |                   | *...*           |       | Weitere Subklassen von ``DistanceFunction`` |
    +-------------------+-------------------+-----------------+-------+---------------------------------------------+
    |                   | *session.py*      |                 |       | Implementierung der ``Session`` (API)       |
    +-------------------+-------------------+-----------------+-------+---------------------------------------------+
    |                   | *easy.py*         |                 |       | Implementierung der ``EasySession``         |
    +-------------------+-------------------+-----------------+-------+---------------------------------------------+
    |                   | *graph.py*        |                 |       | Implementierung der Graphenoperationen      |
    +-------------------+-------------------+-----------------+-------+---------------------------------------------+
    |                   | *helper.py*       |                 |       | Gesammelte, oftgenutzte Funktionen          |
    +-------------------+-------------------+-----------------+-------+---------------------------------------------+
    |                   | *history.py*      |                 |       | Implementierung der ``History`` u. Regeln   |
    +-------------------+-------------------+-----------------+-------+---------------------------------------------+
    |                   | *plot.py*         |                 |       | Visualisierungsfunktionen für Graphen       |
    +-------------------+-------------------+-----------------+-------+---------------------------------------------+
    |                   | **provider/**     |                 |       | Unterverzeichnis für Provider               |
    +-------------------+-------------------+-----------------+-------+---------------------------------------------+
    |                   |                   | *__init__.py*   |       | Implementierung von ``Provider``            |
    +-------------------+-------------------+-----------------+-------+---------------------------------------------+
    |                   |                   | *bpm.py*        |       | Implementierung von ``BPMProvider``         |
    +-------------------+-------------------+-----------------+-------+---------------------------------------------+
    |                   |                   | *composite.py*  |       | Implementierung des ``CompositeProvider``   |
    +-------------------+-------------------+-----------------+-------+---------------------------------------------+
    |                   |                   | *...*           |       | Weitere Subklassen von ``Provider``         |
    +-------------------+-------------------+-----------------+-------+---------------------------------------------+
    |                   | *rake.py*         |                 |       | Implementierung des RAKE-Algorightmus       |
    +-------------------+-------------------+-----------------+-------+---------------------------------------------+
    |                   | **scripts/**      |                 |       | Unterverzeichnis für ,,Test Scripts''       |
    +-------------------+-------------------+-----------------+-------+---------------------------------------------+
    |                   |                   | *visualizer.py* |       | Zeichnet ein mood-file mittels ``cairo``    |
    +-------------------+-------------------+-----------------+-------+---------------------------------------------+
    |                   |                   | *walk.py*       |       | Berechnet vieles mood-files parallel        |
    +-------------------+-------------------+-----------------+-------+---------------------------------------------+
    |                   | *song.py*         |                 |       | Implementierung von ``Song``                |
    +-------------------+-------------------+-----------------+-------+---------------------------------------------+
    |                   | **stopwords/**    |                 |       | Stoppwortimplementierung:                   |
    +-------------------+-------------------+-----------------+-------+---------------------------------------------+
    |                   |                   | *__init__.py*   |       | Implementierung des Stoppwort-Loader        |
    +-------------------+-------------------+-----------------+-------+---------------------------------------------+
    |                   |                   | **data/**       |       | Unterverzeichnis für die Stoppwortlisten    |
    +-------------------+-------------------+-----------------+-------+---------------------------------------------+
    |                   |                   |                 | *de*  | Gemäß ISO 638-1 benannte Dateien;           |
    +-------------------+-------------------+-----------------+-------+---------------------------------------------+
    |                   |                   |                 | *en*  | Pro Zeile ist ein Stoppwort gelistet;       |
    +-------------------+-------------------+-----------------+-------+---------------------------------------------+
    |                   |                   |                 | *es*  | Insgesamt 17 verschiedene Listen.           |
    +-------------------+-------------------+-----------------+-------+---------------------------------------------+
    |                   |                   |                 | *...* |                                             |
    +-------------------+-------------------+-----------------+-------+---------------------------------------------+
    |                   | *testing.py*      |                 |       | Fixtures und Helper für unittests           |
    +-------------------+-------------------+-----------------+-------+---------------------------------------------+

    
Anwendungsbeispiel
==================

Um ein Gefühl für eine Software-Bibliothek zu bekommen eignet sich oft ein
minimales Beispiel gut. Das folgende Beispiel liest *Songs* aus einer
(Pseudo-)Datenbank und erstellt dann Empfehlungen für einen davon:

.. code-block:: python
    :linenos:
    :emphasize-lines: 1,3,11,12,14,21

    from munin.easy import EasySession

    MY_DATABASE = [
        # Artist:           Album:               Title:             Genre:
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


Ist *libmunin* korrekt installiert, so lässt sich dieses Skript als
``minimal.py`` ablegen und folgendermaßen ausführen:

.. code-block:: bash

    $ python minimal.py 
    ('Vogelfrey'  , 'Wiegenfest'       , 'Heldentod'      , 'folk metal'),
    ('Debauchery' , 'Continue to Kill' , 'Apostle of War' , 'brutal death')

Kurze Erläuterung des Beispiels 
-------------------------------

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
  fügen diese der *Session* hinzu (über die ``add`` Operation). zu beachten ist
  dabei: Es wird eine Hashtable übergeben in denen bestimmte Schlüssel (wie
  ``artist``) von der ``EasySession`` vorgegeben sind - erstellt man eine eigene
  Session kann man diese nach Belieben Konfigurieren.
  
  Ein Problem dass man bei der Benutzung der Library hat ist: *libmunin* und der
  Nutzter halten zwei verschiedene Datenbanken im Speicher. Der Benutzer
  verwaltet die Originaldaten mit denen er arbeitet während *libmunin* nur
  normalisierte Daten speichert. Das Problem dabei: Wie soll der User wissen
  welche Empfehlung zu welchen Song in seinen Originaldaten gehört?

  Dazu ist ein Mapping erforderlich das 
  Zu diesem Zwecke geben die Operationen ``add``, ``insert``, ``modify`` und
  ``remove`` eine eindeutige ID zurück die einen von *libmunin's* Songs
  referenziert. Der Benutzer kann diese nutzen um auf eine ID innerhalb *seiner*
  Datenbank zu referenzieren. 

  Im obigen Beispiel wird die von ``add`` zurückgebene ID auf die ID innerhalb
  von *MY_DATABASE* gemappt.

* **Zeile 21:**

  In dieser Zeile geben wir die ersten Empfehlung aus. Wir lassen uns von der
  ``EasySession`` über die Methode ``recommend_from_seed`` zwei Empfehlungen zum ersten
  Song der über ``add`` hinzugefügt wurde geben. Die Empfehlung selbst wird als
  ``Song`` Objekt ausgebene - dieses hat unter anderen eine ID gespeichert mit
  der wir die ursprünglichen Daten finden können.

Dieses und weitere Beispiele finden sich auf der API-Dokumentation im Web
:cite:`5LX`.


Kurze Erläuterung des Outputs
-----------------------------

Der Output ist nicht weiter überraschend: Da sich nur das Genre effektiv
vergleichen lässt und wir uns von dem ersten Song (,, *Trugbild* '') zwei
Empfehlungen geben ließen werden die zwei Songs mit dem ähnlichsten Genre
ausgegeben.

[TODO: Den Mini-Graph einfügen]

Trivia
======

Entwicklungsumgebung
--------------------

Als Programmiersprache wurde *Python* aus folgenden Gründen ausgewählt:

* Exzellenter Support für *Rapid Prototyping* - eine wichtige Eigenschaft bei
  nur knapp 3 Monaten Implementierungs-Zeit.
* Große Zahl an nützlichen Libraries, besonders für den wissenschaftlichen Einsatz.
* Neben *C* die *Lingua Franca* des Autors.

Alle Quellen die während dieses Projektes entstanden sind finden sich auf der
sozialen Code-Hosting Plattform *GitHub* :cite:`Y41`. Der Vorteil dieser Plattform besteht
darin dass sie von sehr vielen Entwicklern besucht werden, die die Software
ausprobieren und möglicherweise verbessern oder zumindestens die Seite für
spätere Projekte bookmarken.  Daher auch Github's Slogan *Social Coding*.

Die dazugehörige Dokumentation wird bei jedem commit automatisch aus den
Sourcen, mittels des freien Dokumentationsgenerators Sphinx, auf der
Dokumentations-Hosting Plattform *ReadTheDocs* gebaut und dort verfügbar
gemacht :cite:`5LX`.

Zudem werden pro Commit unittests auf der Continious-Integration Plattform
*TravisCI* :cite:`JIU` für verschiedene Python-Versionen durchgeführt. Dies hat den Vorteil
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
veröffentlicht :cite:`O6Q`, wo sie mithilfe des folgenden Befehles samt
Python-Abhängigkeiten installiert werden können:

.. code-block:: bash

    $ sudo pip install libmunin

Auf lokaler Seite wird jede Änderungen versioniert, um die Fehlersuche zu
vereinfachen - im Notfall kann man stets auf funktionierende Versionen
zurückgehen. 

Der Quelltext selber wird in *gVim* geschrieben. Dass sich der Python-Quelltext
dabei an die gängigen Konventionen hält wird durch die Zusatzprogramme *PEP8*
und *flake8* überprüft.

Auch dieses Dokument wurde mit einem erweiternten Sphinx erstellt. Dies hat den
Vorteil dass die Arbeit in *reStructuredText* geschrieben werden kann und
einerseits als PDF und als HTML Variante :cite:`8MD` erstellt wird.  

Lines of Code (*LoC*)
---------------------

Was die *Lines of Code* betrifft so verteilen sich insgesamt 4867 Zeilen
Quelltext auf 46 einzelne Dateien. Die im nächsten Kapitel vorgestellte
Demo-Anwendung ist dabei mit eingerechnet. Dazu gesellen sich 2169 Zeilen
Kommentare, die zum größten Teil zur Generation der Online-Dokumentation
genutzt werden.

Dazu kommen einige weitere Zeilen von *reStructuredText* (einer einfachen
Markup-Sprache) die die Gerüst der Onlinedokumentation bilden:

.. code-block:: bash

    $ wc -l $(find . -iname '*.rst')
    2231 insgesamt

Sonstige Statistiken
--------------------

Zudem lassen sich einige Statistiken präsentieren die automatisch aus den
``git log`` entstanden sind:

GitHub Visualisierungen
~~~~~~~~~~~~~~~~~~~~~~~

*GitHub* stellt einige optisch ansprechende und interaktive Statistiken bereit
die beispielsweise viel über den eigenen Arbeitszyklus verraten:

    :cite:`IBL`

``gitstats`` Visualisierungen
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
      
Das kleine Programm ``gitstats`` baut aus dem ``git log`` eine HTML-Seite mit
einigen interessanten Statistiken - wie beispielsweise der absoluten Anzahl von
geschriebenen (und wieder gelöschten) Zeilen:

    :cite:`8MD`

``gource`` Commit-Graph Visualisierungsvideo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``gource`` ist ein Programm das in einem optisch ansprechenden Video zeigt wie
sich das ``git``-Repository mit der Zeit aufbaut:

... TODO ...
