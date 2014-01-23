*********
Übersicht
*********

Motivation
==========

- Existierende Plattformen wie last.fm, spotify, pandora, rhapsody, youtube!
- allerdings serverseitige infrastruktur
- Oft werden ähnliche musikstücke empfohlen -> wirtschaftlich relevant.
- Keine (na gut, eine) allgemeine bibliothek um musik empfehlungen aus einer
  daternbank abzuleiten
- viele existierende tools nutzen einfach online-dienste um empfehlungen zu
  treffen - was nicht schlecht sein muss. 
- Vereinzelt systeme die allein auf der "mood" arbeiten.
- libmunin soll viele attribute und quellen vereinen, und dabei so flexibel
  sein überall eingebaut werden zu können.

http://de.wikipedia.org/wiki/Empfehlungsdienst

Massenhaft Arbeiten auf dem Gebiet:

http://scholar.google.de/scholar?q=music+recommendation+engine

- Die Tatsache dass der Autor einen MPD Client schreibt und so ein feature sich
  wünscht trägt natürlich zur motivation bei.
- Deswegen soll die library auch nach Abschluss dieser Arbeit weiterentwickelt 
  werden.

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

- Einsatz in Mediaplayern für große lokale Musiksammlungen.
- Einsatz bei music streaming plattformen als backend.
- Einsatz bei music verkäufern - um ähnliche artikel vorzuschlagen.
- Einsatz bei DJ Software um eine Auswahl für die nächsten Stücke zu erzeugen.

Änderungen zum Expose
=====================

- Andere Programmiersprache: Python - bleibt auch so.
- Keine Distanzmaxtrix mehr.
- C (auch mit ++) wäre zu aufwendig geworden.

Namensgebung
============

.. epigraph::

    In Norse mythology, Hugin (from Old Norse “thought”)
    and Munin (Old Norse “memory” or “mind”)
    are a pair of ravens that fly all over the world Midgard,
    and bring information to the god Odin.

    -- http://en.wikipedia.org/wiki/Huginn_and_Muninn

Der Name *Munin* war bereits vergeben an ein Monitoring Tool, deswegen wurde die
library *libmunin* benannt. Das hat den witzigen Nebeneffekt dass eine
kommerzielle namens *mufin* eine freie Alternative erhält.
