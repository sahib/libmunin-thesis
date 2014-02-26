###########
Algorithmen
###########


.. epigraph::

    Ich verstehe nichts von Musik. In meinem Fach ist das nicht nötig.

    -- Elvis Presley (1935-77), gen. "King of Rock 'n' Roll", amerik. Sänger

Genre Splitting
===============

Problemstellung
---------------

Das Vergleich einzelner Genres ist eine schwierige Angelegenheit da es,
zumindestens im Bereich der Musik, keine standardisierte Einteilung von Genres
gibt. Daher ist es nötig, dass die einzelnen Genre-Eingaben anhand einer
Sammlung von zusammengestellten Genredaten normalisiert werden.

Zusammenstellung der Gernedatenbank
-----------------------------------

Genres können, wie in einem Baum, in Übergenres (*rock*, *pop*), Untergenres
(*country* rock, *japanese* pop), Unter-Untergenres (*) (und so weiter)
aufgeteilt werden. So lassen sich alle Genres unter ihre jeweiligen Untergenres
als Baum darstellen. Als, meist imaginären, Wurzelknoten nimmt man das
allumfassende Genre *Musik* an. 


.. digraph:: foo

    size=4; 
    node [shape=record];

    "music (#0)"  -> "rock (#771)"
    "music (#0)"  -> "alternative (#14)"
    "music (#0)"  -> "reggae (#753)"
    "rock (#771)" -> "alternative (#3)"


Die eigentliche Schwierigkeit besteht nun darin eine repräsentative Sammlung von
Genres in diesen Baum einzupflegen - zudem kann man dies bei der hohen Zahl der
existierenden Genres (Beispiel bringen?) diese nur schwerlich manuell
einpflegen.

Existierende Datenbanken wie, das sonst so vollständige, *MusicBrainz* liefern
laut ihren FAQ keine Genredaten:

.. epigraph::

   **Why does MusicBrainz not support genre information?**

   *Because doing genres right is very hard.
   We have thought about how to implement genres,
   but we haven't completely settled on the right approach yet.*

   -- https://musicbrainz.org/doc/General_FAQ

Also musste man sich nach anderen Quellen umschauen. Das vom
*DiscogsGenre*-Provider verwendete Discogs bietet zwar relative detaillierte
Informationen, teilt aber die Genres hierarchisch in zwei Ebenen auf, dem
*Genre* (*rock*) und dem Subgenre (*blackened death metal*) - eine zu grobe
Einteilung.

Dafür fallen zwei andere Quellen ins Auge: *Wikipedia* - fast jede Band 
ist dort vertreten und eben auch mit detaillierter Genre Information - sowie
*The Echonest* - einem Unternehmen welches verschiedene Dienste rund um
Musikmetadaten anbietet, darunter auch eine Liste von den ihnen bekannten
Genres. 

Mit diesen zwei Quellen sollte man einen repräsentativen Durchschnitt aller
Genres bekommen. Zuerst muss man allerdings an die Daten herankommen. Bei
*The Echonest* ist dies, nachdem man sich einen *API Key* registriert hat
relativ einfach [#f1]_: 

    http://developer.echonest.com/api/v4/artist/list_genres?api_key=XXXformat=json

Die Liste enthält, zum Zeitpunkt des Schreibens, 898 konkrete Genres und wird
kontinuierlich erweitert. 

TODO: APi key in glossar aufnehmen


Die Suche bei Wikipedia gestaltet sich etwas schwieriger. Tatsächlich wurde
diese Quelle erst nachträglich nach einer Analyse des Quelltextes von *beets*
(https://gist.github.com/sampsyo/1241307)
eingebaut. *beets* hat ebenfalls das Problem das Genre zu normalisieren - also
muss dort ein entsprechender Mechanismus eingebaut sein. Dieser beruht, ähnlich
wie hier, ebenfalls auf einem Baum [#f2]_. Um diese Quelle in *libmunin* zu
nutzen wurde lediglich der Code nach *Python3* portiert. Von wikipedia werden
folgende Seiten gescraped, und die darin befindlichen genres in eine datei
geschrieben: 

    - TODO: wiki sites

.. _zerlegung:

Überfuehrung der genre-listen in einem genre-baum
-------------------------------------------------


Nachdem eine Liste von Genres nun vorhanden ist muss diese noch in einem Baum
wie oben gezeigt ueberfuehrt werden. Dazu wird jedes genre in der liste anhand
von eines regulaeren ausdruck (todo: fussnote) in einzelne woeerter zerlegt. 

... todo


Matching von Genres
-------------------

um Normalisieren des Genres wird folgendermaßen vorgegangen:

- Wie in :ref:`zerlegung` wird das Eingabegenre in einzelne Wörter aufgebrochen.
- TODO


Als Resultat kommt jeweils eine Liste von möglichen Pfaden heraus die das
Eingabegenre anhand der bekannten Genre beschreiben: 

TODO


Vergleichen der unterschiedlichen Genre-Pfade-Mengen
----------------------------------------------------

.. _single-dist:

Um zwei einzelne Pfade miteinander zu vergleich wird folgenderndermaßen
vorgegangen:

- Zähle die Anzahl an Punkten in denen sich der Pfad überdeckt. 
- Teile die Anzahl durch die Länge des längeren beider Pfade.
- Die daraus gewonnene Ähnlichkeit wird von :math:`1.0` abgezogen um die Distanz
  zu erhalten.

In *libmunin* sind zwei Distanzfunktionen erhalten welche diese Methode nutzt um
zwei Mengen mit Genrepfaden zu vergleichen:

GenreTree
~~~~~~~~~

Vergleicht jeden Genrepfad in der einen Menge mit dem in der anderen Menge
mittels oben genannter Methode. Die minimalste Distanz wird zurückgegeben. 
Als Optimierung wird frühzeitig abgebrochen wenn eine Distanz von :math:`0.0`
erreicht wird.

Diese Distanzfunktion eignet sich für eher kurze Genre-Beschreibungen wie sie in
vielen Musiksammlungen vorkommen. Meist ist dort ein Lied als *rock* oder
*metal* eingetragen, ohne Unterscheidung von Subgenres. Deshalb geht diese
Distanzfunktion davon aus wengie Übereinstimmungen zu finden - sollten welche
vorkommen werden diese gut bewertet.

GenreTreeAvgLink
~~~~~~~~~~~~~~~~

Seien *A* und *B* zwei Mengen mit Genrepfaden. *A* ist dabei die größere Menge
und *B* die kleinere falls die Mengen eine unterschiedliche Mächtigkeit
besitzen.

Setzt man vorraus, dass *d* die unter :ref:`single-dist` erwähnte
Distanzunktion ist,  so berechnet sich die
finale Distanz durch:

.. math:: 

   D(A, B) = \frac{\displaystyle\sum\limits_{a=0}^{|A|} \argmin\!{\bigg(\displaystyle\sum\limits_{b=0}^{|B|} d(a, b)\bigg)}}{\vert A\vert}


Diese Distanzfunktion eigent sich für *,,reichhaltig''* befüllte
Genrebeschreibungen bei denen auch ein oder mehrere Untergenres vorhanden sind.
Ein Beispiel dafür wäre: ``country rock / folk / rockabilly``. Die
Distanzfunktion geht also davon aus zumindestens teilweise Überdeckungen in den
Daten vorzufinden.

Je nach Daten die es zu verarbeiten gilt, kann der Nutzer der Bibliothek eine
passende Distanzunktion auswählen.

Probleme
--------

Insgesamt funktioniert dieser Ansatz relativ gut, die meisten Genre werden
zufriedenstellend in Pfade normalisiert die performant verglichen werden können.

Folgendes Problem wird allerdings noch nicht zufriedenstellend gelöst:
Es wird davon ausgegangen, dass genres die ähnlich sind auch ähnlich heißen -
eine Annahme die zwar oft, aber nicht immer wahr ist. So sind die Genres
*Alternative Rock* und *Grunge* sehr ähnlich - der obige Ansatz würde hier
allerdings eine Distanz von :math:`0.0` liefern. 


.. rubric:: Footnotes

.. [#f1] Der *API Key* wurde in der URL gekürzt da man angehalten ist diesen
   nicht zu veröffentlichen. 

.. [#f2] Anmerkung: Die Idee entstand allerdings ohne Kenntnis von *beets*.

ZSIUEIVVZGJVJVWIS&

Keword Extraction
-----------------

KeywordExtraction - KeywordSelection - KeywordDistance

Rule Generation
---------------


Graph Generation
----------------

add, rebuild, fix_graph

distance_add
------------

"max_neighbors Dilemma"


Graphenoperationen
------------------

insert, remove, modify

Graphentraversierung
--------------------

Infinite Iteratos - konzept aus funktionalen Programmiersprachen wie Haskell

Sieving Algorithm
-----------------

Erklärung & Configuration.


Various Providers
-----------------

Erwähnenswerte Algorithmik hinter den anderen Providern.

levenshtein, bpm, moodbar, wordlist distance, normalize provider, stemming
