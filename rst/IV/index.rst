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

Features
--------

- Einbeziehung der duration als provider/distanz (statistisch untersuchen)
- Echte audionanylse mittels aubio. https://github.com/piem/aubio 
- Echte mood analyse.
- Sprache, Intros und Audio intelligent unterscheiden.

Convinience / Korrektheit
-------------------------

- Schnellerer Analyseschritt durch parallelisiertes fetchen von lyrics und 
  beschleunigter audioanalyse.
- Die resultate können nur so gut sein wie die input daten.
  Es wäre wünschenswert eine "bridge" zwischen libmunin und beets zu schreiben:

    http://beets.radbox.org/

  Beets ist gewißermaßen das libhugin-anaylse für musik 
