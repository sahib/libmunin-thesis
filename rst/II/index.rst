**********
Einleitung
**********

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

Schaubild


Analyse (aufwendig) -> Graph -> Recommendations.


Entwicklungsumgebung
====================

- readthedocs
- travisci
- github
- pypi
