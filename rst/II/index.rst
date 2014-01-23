********
Einstieg
********

Zitierbeispiel: :cite:p:`collada`.


Alternativen
============

- mirage

  http://hop.at/mirage/

    - am ehesten mit libmunin vergleichbar. 
    - mirage nutzt nur audiodaten.
    - in banshee integriert
    - weniger für große datenmengen ausgelegt.

- mufin 

    http://www.mufin.com/usecase/music-recommendation/

    - kommerziell
    - enorm viele features 
    - v.a. kein aufwendiger analyse step

Webseiten:

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

.. figure:: figs/munin_startup.*
    :alt: Allgemeine Benutzung
    :width: 75%
    :align: center

    Allgemeine Benutzung von libmunin

.. figtable::
    :label: table-cc-file-size
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

- readthedocs
- travisci
- github
- pypi
