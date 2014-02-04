***************
Zusammenfassung
***************

.. epigraph::


   *Human beings, who are almost unique in having the ability to learn from the
   experience of others, are also remarkable for their apparent disinclination
   to do so.*

   -- *Douglas Adams, ,,Last Chance to See''*


Ausblick
========

Mögliche Weiterentwicklungen
============================

Performance
-----------

- Optimierungen um unnötige vergleiche zu verringern, beispiels nur moodbar
  vergleichen wenn länge des stückes ähnlich ist.

  Ein Beispiel:

    Ein Vergleich der Moodbar-Informationen ist nur dann sinnvoll wenn die Länge
    der zu Vergleichenden Songs sich nicht um mehr als eine Minute
    unterscheiden. Vergleicht man trotzdem erhält man vermutlich:ta
  
- Prinzipiell ist libmunin so generell angelegt dass es sogar für jegliche daten
  bei denen es sehr viele dokumente gibt und diese sich als hashtable
  repräsentieren lassen.

Features
--------

- Suchengine für natürliche Sprache wie in :cite:p:`knees2007music`
- Beziehen und Nutzen weiterer Metadaten (wie Producer, Band-Member)
- Auch "disklikes" berücksichtigen (zB. songs die immer gleich geskippt wurden)?
- Gemeinsame Nachbarn betrachten bei mehreren Seedsongs.
- Similar Artist/Album/Genre...
- Einbeziehung der duration als provider/distanz (statistisch untersuchen)
- Echte audionanylse mittels aubio. https://github.com/piem/aubio 
  oder https://github.com/marsyas/marsyas
- Echte mood analyse.
- (Amazon) artist/album reviews mit einbeziehen, keyword-extraction.
- Sprache, Intros und Audio intelligent unterscheiden.
- Dbus Service:

    - Problem: Nutzung von libmunin von anderen Sprachen aus.
    - Problem: Mehrere Programme wollen Session nutzen.

- Overlays - dynamische playlisten mit statischen mischen
- Fortlaufende dynamische playlisten

Convinience / Korrektheit
-------------------------

- Bessere Speicherung der Session auf die Platte - momentan pickle, erfordert 
  hohe Rekursionstiefe, sprengt für große Sessions den Stack.
- Schnellerer Analyseschritt durch parallelisiertes fetchen von lyrics und 
  beschleunigter audioanalyse.
- Die resultate können nur so gut sein wie die input daten.
  Es wäre wünschenswert eine "bridge" zwischen libmunin und beets zu schreiben:

    http://beets.radbox.org/

  Beets ist gewißermaßen das libhugin-anaylse für musik 

Fazit
=====

Generell ist *libmunin's* architektur nicht nur für Musikstücke tauglich,
sondern für alle Anwendungsfälle bei denen viele Dokumente miteinander
vergleichen zu sind und diese sich durch einface Key-Value Mappings abbilden
lassen.

So wäre mit *libmunin* auch ein Bücher- oder Video-Empfehlungssystem möglich - 
sofern man entsprechende Provider und Distanzfunktionen implementiert.
