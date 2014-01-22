*****
Fazit
*****

Ausblick
========


Mögliche Weiterentwicklungen
============================


Performance
-----------

- Optimierungen um unnötige vergleiche zu verringern, beispiels nur moodbar
  vergleichen wenn länge des stückes ähnlich ist.
- Prinzipiell ist libmunin so generell angelegt dass es sogar für jegliche daten
  bei denen es sehr viele dokumente gibt und diese sich als hashtable
  repräsentieren lassen.

Features
--------

- Einbeziehung der duration als provider/distanz (statistisch untersuchen)
- Echte audionanylse mittels aubio. https://github.com/piem/aubio 
- Echte mood analyse.
- Amazon artist/album reviews mit einbeziehen, keyword-extraction.
- Sprache, Intros und Audio intelligent unterscheiden.
- Dbus Service:

    - Problem: Nutzung von libmunin von anderen Sprachen aus.
    - Problem: Mehrere Programme wollen Session nutzen.

- Overlays - dynamische playlisten mit statischen mischen
- Fortlaufende dynamische playlisten

Convinience / Korrektheit
-------------------------

- Schnellerer Analyseschritt durch parallelisiertes fetchen von lyrics und 
  beschleunigter audioanalyse.
- Die resultate können nur so gut sein wie die input daten.
  Es wäre wünschenswert eine "bridge" zwischen libmunin und beets zu schreiben:

    http://beets.radbox.org/

  Beets ist gewißermaßen das libhugin-anaylse für musik 
