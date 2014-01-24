********
Einstieg
********

Zitierbeispiel: :cite:p:`collada`.

.. figure:: figs/munin_startup.*
    :alt: Allgemeine Benutzung
    :width: 75%
    :align: center

    Allgemeine Benutzung von libmunin

Ziele
=====

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

Einsatzszenarien
================

Denkbare Einsatzszenarien wären:

    1. Einsatz in Mediaplayern für große lokale Musiksammlungen.
    2. Einsatz bei music streaming plattformen als backend.
    3. Einsatz bei music verkäufern - um ähnliche artikel vorzuschlagen.
    4. Einsatz bei DJ Software um eine Auswahl für die nächsten Stücke zu erzeugen.
    5. ...

http://de.wikipedia.org/wiki/Empfehlungsdienst

Vorhandene Alternativen
=======================

- **mirage**

  http://hop.at/mirage/

    - am ehesten mit libmunin vergleichbar. 
    - mirage nutzt nur audiodaten.
    - in banshee integriert
    - weniger für große datenmengen ausgelegt.

- **mufin audiogen**

    http://www.mufin.com/products/audiogen/

    - kommerziell
    - enorm viele features 
    - behauptet keinen ,,Kaltstart'': Daten werden auf Servern vorberechnet.

Webseiten:

- http://www.tastekid.com/
- http://musicovery.com/


Anforderungen
=============

- Schnelle empfehlungen 
- Infinite Iterators
- Empfehlungen basierent auf vielen Attributen.
- Handling von enormen Datenmengen (Memverbrauch mal messen)


Implementierungsziele
=====================

- ...
- ...
- Implementierung einer Demoanwendung die als Frontend für libmunin funktioniert
  und ihre daten von mpd, via libmoosecat holt. libmoosecat ist eine vom Autor 
  seit August 2012 vom Autor entwickelte library um einen vollständigen mpd
  client mit erweiterten features zu implementieren (wie einer proxy datenbank,
  erweiterter query syntax u.v.m). 
- Datenbeschaffung via libglyr/discogs.


.. admonition:: Exkurs zu moosecat

   Moosecat ist ein vom Auto seit 2012 entwickelter MPD-Client. Im Gegensatz zu
   den meisten, etablierten Clients hält er eine Zwischendatenbank die den
   Zustand des Servers spiegelt. Dadurch wird die Netzwerklast und die Startzeit
   reduziert und interessante Feature wie Volltextsuche wird möglich.

Übersicht
=========

.. figure:: figs/integration.*
    :alt: Integrationsübersicht
    :width: 100%
    :align: center

    Wie integriert sich libmunin in seine Umgebung?

.. figure:: figs/arch.*
    :alt: Architekturübersicht.
    :width: 100%
    :align: center

    Grobe Übersicht über die architektur.

.. figure:: figs/provider_process.*
    :alt: Attributverarbeitung
    :width: 75%
    :align: center

    Ablauf bei der Verarbeitung eines einzelnen Attributes.

.. figtable::
    :caption: Mean size of progressive format as a fraction of the
              original across all test models, shown as a function of the
              progressive stream downloaded and texture resolution.
    :alt: Mean Size of Progressive Format
    :spec: r r r r r r r

    ===========  ====  ====  ====  ====  ====
    Progressive  128   256   512   1024  2048
    ===========  ====  ====  ====  ====  ====
             0%  0.53  0.63  0.81  1.03  1.35
            25%  0.65  0.75  0.97  1.16  1.45
            50%  0.74  0.85  1.02  1.26  1.58
            75%  0.79  0.95  1.11  1.34  1.70
           100%  0.88  0.99  1.20  1.44  1.82
    ===========  ====  ====  ====  ====  ====

Entwicklungsumgebung
====================

Alle Quellen die während dieses Projektes entstanden sind finden sich auf
der sozialen Code-Hosting Plattform Github. User können dort interessante 
Projekte *starren* - bis jetzt hat *libmunin* für seine recht kurze Lebensspanne 
ein recht hohe Zahl von *Stars*: 15.

Die dazugehörige Dokumentation wird bei jedem commit automatisch aus den
Sourcen, mittels des freien Dokumentationsgenerators Sphinx,
auf der Dokumentations-Hosting Plattform *ReadTheDocs* gebaut und dort
verfügbar gemacht: https://libmunin.rtfd.org

Zudem werden pro commit unittests auf der Continious-Integration Plattform
*TravisCI* für verschiedene Python-Versionen durchgeführt.
Dies hat den Vorteil dass fehlerhafte Versionen aufgedeckt werden,
selbst wenn man vergessen hat die unittests lokal durchzuführen.

Schlägt der Build fehl so färben sich kleine Buttons in den oben genannten
Diensten rot und man wird per Mail benachrichtigt. TOOD: ref down.

.. figure:: figs/travis_badge.png
    :align: center
    :alt: Screenshot der Statusbuttons auf der Github-Seite.


Versionen die bekannterweise stabil laufen werden auf PyPi (Python Package
Index) veröffentlicht, wo sie mithilfe des folgenden Befehles samt
Python-Abhängigkeiten installiert werden können:

.. code-block:: bash

    $ sudo pip install libmunin
