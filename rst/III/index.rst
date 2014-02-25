###########
Algorithmen
###########

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
nutzen wurde lediglich der Code nach *Python3* portiert. 


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
