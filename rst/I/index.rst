*********
Übersicht
*********

Motivation
==========

- Existierende Plattformen wie last.fm, spotify, pandora, rhapsody
- allerdings serverseitige infrastruktur
- Oft werden ähnliche musikstücke empfohlen -> wirtschaftlich relevant.
- Keine (na gut, eine) allgemeine bibliothek um musik empfehlungen aus einer
  daternbank abzuleiten
- viele existierende tools nutzen einfach online-dienste um empfehlungen zu
  treffen.
  (was nicht schlecht sein muss)

- Vereinzelt systeme die allein auf der stimmung arbeiten:

- libmunin soll viele attribute und quellen vereinen, und dabei so flexibel
  sein überall eingebaut werden zu können - zudem noch keine 
  direkte Verbindung von Datamining und Music Information Retrieval.

- viele verschiedene Ideen: Artist reviews analysieren...


http://de.wikipedia.org/wiki/Empfehlungsdienst

Massenhaft Arbeiten auf dem Gebiet:

http://scholar.google.de/scholar?q=music+recommendation+engine&hl=de&as_sdt=0&as_vis=1&oi=scholart&sa=X&ei=WnTaUqqiNYzQsgbUw4HAAg&ved=0CEAQgQMwAA

Wenige (sinnvolle) websites:

- http://www.tastekid.com/
- http://musicovery.com/

Noch weniger allgemeine libraries:

- http://hop.at/mirage/

Ziele
=====

- Erstellung dynamischer, fortlaufender Playlisten.
- Lernfähigkeit.
- Aufsatz über library möglich, beispielsweise erst lookup in recommendation
  database, dann automatisch via libmunin.

Zielgruppe
==========

- In früher Phasen: Hauptsächlich interessierte entwickler mit viel geduld.
- Erster interessierter Entwickler wird der Entwickler von moosecat sein.
- Möglichkeit: in mopidy einbauen, dort wird auch ein dynamic playlist 
  feature "gesucht".
- Sobald in "Otto-normal-player": Auch normale anwender mittels DBUS Service und
  cli tool. Momentan eher sperrig benutzbar. 
