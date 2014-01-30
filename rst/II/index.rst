********
Einstieg
********

.. figure:: figs/munin_startup.*
    :alt: Allgemeine Benutzung
    :width: 75%
    :align: center

    Allgemeine Benutzung von libmunin

Ziele
=====

Ziel ist ein System das folgende Fähigkeiten besitzt:

- Erstellung dynamischer, fortlaufender Playlisten.
- Lernfähigkeit.
- Mögliche "Aufsätze": Erst lookup in von user vorgegebener recommendation db,
                       dann erst automatisch via libmunin.
- Stark anpassbare API, da diese alle möglichen spezialfälle abdecken muss,
  und auf die unterschiedlichen formate der musiksammlungen eingestellt sein
  muss.

Zielgruppe
==========

(Auf Opensource gedanke eingehen)

- In früher Phasen: Hauptsächlich interessierte entwickler mit viel geduld.
- Erster interessierter Entwickler wird der Entwickler von moosecat sein.
- Möglichkeit: in mopidy einbauen, dort wird auch ein dynamic playlist 
  feature "gesucht".
- Sobald in "Otto-normal-player": Auch normale anwender mittels DBUS Service und
  cli tool. Momentan eher sperrig benutzbar. 

Primär sind allerdings experimentierfreudige Entwickler die Zielgruppe

Einsatzszenarien
================

Denkbare Einsatzszenarien wären:

    1. Einsatz in Mediaplayern für große lokale Musiksammlungen.

        Manche Leute haben fei echt das Problem dass die Musiksammlung zu groß
        ist - und sie oft nur eine kleine Gruppe davon hören. Hier wäre eine
        dynanmische Playlist die je nach Lust und Laune bestimmte passende Bands
        vorschlägt.

        TODO: ernst. 

    2. Einsatz bei music streaming plattformen als backend.

        Music streaming plattformen wie last.fm, pandora, spotify.

    3. Einsatz bei music verkäufern - um ähnliche artikel vorzuschlagen.
    4. Einsatz bei DJ Software um eine Auswahl für die nächsten Stücke zu erzeugen. 
    5. Einsatz bei webradios.
    6. Einsatz in sozialen Netzwerken.
    7. ...weitere Einsatzmöglichkeiten sind denkbar.

http://de.wikipedia.org/wiki/Empfehlungsdienst

Vorhandene Alternativen
=======================

- **mirage**

    - Freie, in C# implementierte Bibliothek für Music Recommendations.
    - Wird im freien Mediaplayer Banshee eingesetzt (der ebenfalls in C# geschrieben ist). 
    - am ehesten mit libmunin vergleichbar. 
    - mirage nutzt nur audiodaten.
    - in banshee integriert
    - weniger für große datenmengen ausgelegt.

  Website: http://hop.at/mirage/

- **mufin audiogen**

    http://www.mufin.com/products/audiogen/

    - kommerziell
    - enorm viele features 
    - behauptet keinen ,,Kaltstart'': Daten werden auf Servern vorberechnet.

Webseiten:

- http://www.tastekid.com/

- http://musicovery.com/

  .. bietet aber im gegensatz zu *tastekid* auch streaming an ..


Anforderungen
=============

Aus den oben genannten Zielen und Einsatzszenarien können 
*Anforderungen* abgeleitet werden die das fertige System erfüllen muss. 

Dabei wird zwischen **technischen Anforderungen** und **weichen Anforderungen**
unterschieden - erstere sind atomar, sprich sie können ganz oder gar nicht
erfüllt werden, letztere können partiell erfüllt werden.

Technische Anforderungen
------------------------

#. Ausstellen von Empfehlungen muss performant möglich sein.

    Da später sehr viele Anfragen, unter Umständen gleichzeitig, an das System
    gestellt werden darf auch eine Abfrage von 100 Empfehlungen nicht länger 
    als eine Sekunde dauern.

    Die eigentliche Arbeit muss daher in einem vorgelagerten Analyse-Schritt 
    erfolgen und die daraus gewonnenen Kenntnisse in einer geeigneten
    Datenstruktur gespeichert werden.

#. Empfehlungen bilden eine Kette.

    Wird eine Anfrage an das System gestellt so wird ein Iterator zurückgegeben
    der alle dem System bekannten Songs nach Relevanz absteigend sortiert ausgibt. 

#. Handhabung großer Datenmengen.

    Groß definiert sich hierbei durch das Einsatzszenario. Bei privaten
    Musiksammlungen beträgt die maximale Größe die problemlos unterstützt werden
    soll bis zu 40.000 Lieder. 
    
    Größere Datenmengen, wie sie vlt. bei Webradios vorkommen, sollen auch unterstützt
    werden. Hier ist allerdings dann ein höherer Rechenaufwand gerechtfertigt.

Weiche Anforderungen
--------------------

#. Die bereitgestellte API muss auf die stark variierende Qualität und Form von
   Musiksammlungen eingestellt sein. 

     Viele existierende Musiksammlungen sind unterschiedlich gut mit Metadaten 
     (*Tags*) versorgt. So sind manche Tags gar nicht erst vorhanden oder sind
     je nach Format und verwendeten Tagging-Tool/Datenbank anders benannt.

     Auch soll das fertige System mit Szenarien zurecht kommen wo lediglich die 
     Metadaten der zu untersuchenden Songs zur Verfügung stehen, aber nicht die
     eigentlichen Audio-Daten. Dies kann beispielsweise vorteilhaft in Fällen
     sein bei denen man die Lieder nicht selbst besitzt aber Zugriff auf
     Musikdatenbanken wie Musicbrainz [#f1]_

#. Das System soll von mehreren Programmiersprachen aus benutzbar sein.

     Dieses Ziel könnte entweder durch verschiedene Languagebindings erreicht
     werden, oder alternativ durch eine Server/Client Struktur mit einem
     definierten Protokoll in der Mitte.

     Portabilität ist für das erste zweitrangig.
     Für den Prototypen sollen lediglich unixoide Betriebssysteme, im speziellen
     Arch Linux, unterstützt werden.

.. rubric:: Footnotes

.. [#f1] Eine frei verfügbare Musikmetadatendatenbank: http://musicbrainz.org/


Implementierungsziele
=====================

- ...
- ...
  und ihre daten von mpd, via libmoosecat holt. libmoosecat ist eine vom Autor 
  seit August 2012 vom Autor entwickelte library um einen vollständigen mpd
  client mit erweiterten features zu implementieren (wie einer proxy datenbank,
  erweiterter query syntax u.v.m). 
- Datenbeschaffung via libglyr/discogs.
- Implementierung einer Demoanwendung die als Frontend für libmunin funktioniert

.. admonition:: Exkurs zu ``moosecat``:

   Moosecat ist ein vom Auto seit 2012 entwickelter MPD-Client. Im Gegensatz zu
   den meisten, etablierten Clients hält er eine Zwischendatenbank die den
   Zustand des Servers spiegelt. Dadurch wird die Netzwerklast und die Startzeit
   reduziert und interessante Feature wie Volltextsuche wird möglich.


Entwicklungsumgebung
====================

Alle Quellen die während dieses Projektes entstanden sind finden sich auf
der sozialen Code-Hosting Plattform Github. User können dort interessante 
Projekte *starren* - bis jetzt hat *libmunin* für seine recht kurze Lebensspanne 
ein recht hohe Zahl von *Stars*: 15. (TODO: srsly?)


Die dazugehörige Dokumentation wird bei jedem commit automatisch aus den
Sourcen, mittels des freien Dokumentationsgenerators Sphinx,
auf der Dokumentations-Hosting Plattform *ReadTheDocs* gebaut und dort
verfügbar gemacht: https://libmunin.rtfd.org

Zudem werden pro Commit unittests auf der Continious-Integration Plattform
*TravisCI* für verschiedene Python-Versionen durchgeführt.
Dies hat den Vorteil dass fehlerhafte Versionen aufgedeckt werden,
selbst wenn man vergessen hat die unittests lokal durchzuführen.

Schlägt der Build fehl so färben sich kleine Buttons in den oben genannten
Diensten rot und man wird per Mail benachrichtigt. TOOD: ref down.

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

Der Quelltext selber wird in gVim geschrieben. Dass sich der Python-Quelltext
dabei an die gängigen Konventionen hält wird durch die Zusatzprogramme *PEP8* und
*flake8* überprüft.
