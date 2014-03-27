###########
Algorithmen
###########


Einleitung
-----------

Im Folgenden werden einige ausgewählte Paare aus Provider und Distanzfunktionen
näher betrachtet. Nicht alle in der Projektarbeit vorgestellten Provider werden
erläutert, das würde auch den Umfang dieser Arbeit übersteigen. Zudem sind die
meisten Provider eher einfacher Natur --- die Lektüre des jeweiligen Quelltextes
sagt oft mehr als der separate Text. Daher werden im Folgenden nur die
erklärungsbedürftigen Paare näher betrachtet.


Genre-Normalisierung und Vergleich
===================================

Problemstellung
---------------

Der Vergleich einzelner Genres ist eine schwierige Angelegenheit, da es,
zumindest im Bereich der Musik, keine standardisierte Einteilung von Genres
gibt. Ein Computer könnte höchstens erkennen wie ähnlich zwei
Genre Beschreibungen als Zeichenketten sind. Daher ist es nötig, dass die
einzelnen Genre-Eingaben anhand einer Sammlung von zusammengestellten Genre Daten
normalisiert werden.

Zusammenstellung der Gernedatenbank
-----------------------------------

Genres können, wie in einem Baum, in Genres (*rock*, *pop*), Unter-Genres
(*country* rock, *japanese* pop), Unter-Unter-Genres (*western* country rock) -
und so weiter - aufgeteilt werden. So lassen sich alle Genres und ihre
jeweiligen Unter-Genres als Baum darstellen. Als imaginären Wurzelknoten nimmt
man das allumfassende Genre *Music* an - einfach weil *Music* sich hinter fast
jedes Genre schreiben lässt ohne den Sinn zu verändern.

Dieser Baum kann dann genutzt werden um beliebige Genres anhand dieses Baums zu
normalisieren.

Die eigentliche Schwierigkeit besteht nun darin eine repräsentative Sammlung von
Genres in diesen Baum einzupflegen - bei der hohen Zahl der existierenden Genres
kann man diese nur schwerlich manuell einpflegen.

Existierende Datenbanken wie, das sonst sehr vollständige, *MusicBrainz* liefern
laut ihren FAQ keine Genre-Daten:

.. epigraph::

   WHY DOES MUSICBRAINZ NOT SUPPORT GENRE INFORMATION?

   *Because doing genres right is very hard.
   We have thought about how to implement genres,
   but we haven't completely settled on the right approach yet.*

   -- https://musicbrainz.org/doc/General_FAQ

Also musste man sich nach anderen Quellen umschauen. Das vom
*DiscogsGenre*-Provider verwendete *Discogs* bietet zwar relative detaillierte
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
kontinuierlich von den Betreiber erweitert. 

Die Suche bei Wikipedia gestaltet sich etwas schwieriger. Tatsächlich wurde
diese Quelle erst nachträglich nach einer Analyse des Quelltextes von *beets*
(https://gist.github.com/sampsyo/1241307) eingebaut. *beets* hat ebenfalls das
Problem das Genre zu normalisieren - also muss dort ein entsprechender
Mechanismus eingebaut sein. Dieser beruht, ähnlich wie hier, ebenfalls auf einem
Baum [#f2]_. Um diese Quelle in *libmunin* zu nutzen wurde lediglich der Code
nach *Python3* portiert. Von der englischen Wikipedia werden folgende Seiten
*gescraped,* und die darin befindlichen Genres in eine Datei geschrieben: 

- List of popular music genres
- List of styles of music: A-F
- List of styles of music: G-M
- List of styles of music: N-R
- List of styles of music: S-Z

Von Wikipedia kommen 1527 Einträge. Diese werden mit den Einträgen von *,,The
Echonest''* verschmolzen. Nach einer Entfernung von Dubletten ist die finale
Genre-Liste 1876 Einträge lang.

Überführung der Genreliste in einem Genrebaum
---------------------------------------------

.. subfigstart::

.. _fig-tree-input:

.. figure:: figs/tree_input.*
    :alt: Genreliste als Eingabe vor dem Prozessieren
    :width: 70%
    :align: center
    
    Genreliste als Eingabe vor dem Prozessieren.

.. _fig-tree-init:

.. figure:: figs/tree_init.*
    :alt: Initialisierungsschritt
    :width: 100%
    :align: center
    
    Initialisierungsschritt: Vergabe von IDs und Zuordnung zu Wurzelknoten.

.. _fig-tree-first:

.. figure:: figs/tree_first.*
    :alt: Der Genrebaum nach der ersten Iteration
    :width: 100%
    :align: center
    
    Der Genrebaum nach der ersten Iteration, ,,swedish alternative'' noch nicht
    aufgebrochen.

.. _fig-tree-final:

.. figure:: figs/tree_final.*
    :alt: Der fertige Genrebaum als Ausgabe.
    :width: 100%
    :align: center
    
    Der nach zwei Iterationen fertige Genrebaum.

.. subfigend::
    :width: 0.6
    :alt: Aufbau des Genrebaums in 4 Schritten.
    :label: fig-tree
 
    Der Baum wird aus der Eingabe unter :num:`fig-tree-input` erzeugt indem erst
    alle Genres dem Wurzelknoten ,,music'' unterstellt werden
    (:num:`fig-tree-init`). Danach wird der Baum rekursiv (hier in zwei
    Schritten, :num:`fig-tree-first` und :num:`fig-tree-final`)
    immer weiter vertieft. 

Nachdem eine Liste von Genres nun vorhanden ist muss diese noch in einem Baum
wie in :num:`fig-tree-final` gezeigt überführt werden. 
Begleitend werden dazu die unter :num:`fig-tree-input` gezeigte Genre-Liste als
Beispieleingabe. verwendet.

Der Baum sollte dabei folgende Kriterien erfüllen:

- Der Pfad von einem Blattknoten (*,,Swedish''*) zum Wurzelknoten (*,,music''*)
  sollte dabei das ursprüngliche Genre, mit dem optionalen Suffix *music*
  ergeben *(,,swedish-pop-music'')*.
- Jeder Knoten erhält eine Integer-ID die für jeden Tiefenstufe von 0 wieder
  anfängt. So hat der Knoten *music* immer die ID 0, bei der nächsten Ebene wird
  die ID nach alphabetischer Sortierung vergeben, *pop* bekommt daher die 0,
  *reggae* die 1, *rock* die 2. 

Das Umwandeln selbst geschieht folgendermaßen:

- Es wird manuell der Wurzelknoten *music* angelegt.
- Alle Genres in der Genreliste werden diesem Knoten als Kinder hinzugefügt.
  (siehe Abbildung :num:`fig-tree-init`)
- Dann wird rekursiv folgende Prozedur erledigt: 

  1. Gehe über alle Kinder des Wurzelknoten und breche dabei das *letzte Element*
     Wort des *Genres* ab (*western country rock* wird zu *western country* und
     *rock*). 
  2. Der letzte Teil wird als Schlüssel in einer Hashmap gespeichert, mit dem
     Rest als dazugehöriger Wert. Dies entledigt sich, aufgrund der Natur von
     Hashmaps, eventueller Dupletten.
  3. Die Liste der Kinder des Wurzelknotens wird zu einer leeren Liste
     zurückgesetzt.
  4. Die Schlüssel der Hashmap werden als neue Kinder gesetzt, die dazugehörigen
     Werte als deren Kinder.
  5. Iteriere über die neuen Kinder, jedes Kind wird als neuer Wurzelknoten
     angenommen und es wird von 1) an begonnen. Der Rekursionsstopp ist erreicht
     wenn keine Aufteilung des Genres in letztes Element und Rest mehr möglich
     ist.

- In unserem Beispiel ist der Baum bereits nach zwei Iterationen fertig
  (:num:`fig-tree-final`). In :num:`fig-tree-first` ist der Baum nach der ersten
  Iteration zu sehen.
    
- Nach dem manuellen Aufbau werden noch einige halbautomatische Aufräumarbeiten
  erledigt:

  1.  die fehlenden ,,Musik''-Genres *,,vocal''* und *,,speech''* werden
      manuell eingefügt.
  2.  Bei dem momentanen Vorgehen landen unter Umständen weitere ,,*music*''
      auf der ersten Ebene. Diese werden bereinigt.
  3.  Alle Genres die auf *,,core''* enden werden aufgebrochen und dem Knoten
      *,,core''* auf erster Ebene hinzugefügt.

Der resultierende Baum ist im Anhang :ref:`genre-graph-vis` in verschiedenen
Detailstufen visualisiert.  Er besitzt auf der ersten Ebene 1044 Unter-Genre. Die
tiefste Verschachtelung erreicht das Genre *,,New Wave of new Wave''* mit einer
Tiefe von 5.

Matching von Genres
-------------------

Die Normalisierung des Genres ist nun mit dem aufgebauten Baum recht einfach.
Zuerst muss das Eingabegenre in Subgenres aufgeteilt werden - oft sind mehrere
Genres in einem einzelnen String zusammengefasst, die durch bestimmte Zeichen
getrennt sind. Ein Beispiel: 

    *,,Rock, Reggae / Alternative Rock, Ska, Punk''*
    
Jedes dieser Subgenres wird dann mittels eines regulären Ausdruckes in einzelne
Wörter aufgeteilt. Die Wörter werden noch in die kleingeschriebene Form
gebracht. In der Python-Listen Syntax sähe das obige Beispiel dann so aus:

:: 

    [['rock'], ['reggae'], ['alternative', 'rock'], ['ska'], ['punk']]

Die einzelnen Wortlisten können jetzt in *Pfade* umgewandelt werden.
Dazu wird folgendermaßen vorgegangen:

* Es wird eine leere Liste von Pfaden angelegt.
* Es wird eine Liste mit Wahrheitswerten angelegt, die genauso lang ist wie die
  Wortliste. Die Wahrheitswerte werden auf *False* initialisiert.
  Diese *Maske* wird genutzt um bereits gefundene Wörter ,,ab zu haken''.
* Es wird eine leere *,,results''* Liste angelegt. 
* Dann wird eine rekursive Suche nach passenden *Pfaden* mit dem Wurzelknoten
  *music* gestartet:

  1) Schaue ob der momentane Wurzelknoten Kinder enthält die auch in der
     Wortliste vorkommen. Wenn das entsprechende Wort noch nicht in der *Maske*
     abgehakt wurde, wird es in eine temporäre Liste *,,children''* aufgenommen. 
  2) Wenn *,,children''* leer ist und die *,,results''* Liste nicht leer, so
     wird die letzere zur Pfadliste hinzugefügt.

  3) Es wird über jedes Kind in der *,,children''* Liste iteriert. Bei jeder
     Iteration wird:

     A) Eine Kopie der *,,results''* Liste wird erstellt, bei der die ID des
        Kindes am Ende hinzugefügt wurde.
     B) Eine Kopie der *Maske* wird erstellt, in der das vom Kind repräsentierte
        Wort *,,abgehakt''* (der entsprechende Index wird auf *True* gesetzt)
        wird.
     C) Das Kind wird als neuer Wurzelknoten angenommen und es wird wie bei 1)
        weitergemacht.  Der Rekursionsstopp ist dann erreicht wenn die
        *,,children''* Liste leer ist.

  4) Nach dem Rekursionsstopp stehen alle validen Pfade in der Pfadliste.

Das Bedarf vermutlich eines Beispiels. Nehmen wir das Subgenre *,,alternative
rock''* zur Demonstration her. 

.. figure:: figs/tree_match_example.*
    :alt: Beispielablauf des Matching Algorithmusses 
    :width: 100%
    :align: center

    Beispiel-Ablauf des ,,Matching'' an der Eingabe ,,alternative rock''. In den
    Knoten ist die jeweils die momentante Maske eingetragen, an den Kanten das
    aktuelle Ergebniss.


Die passenden Pfade sind in diesem Fall also *alternative* und *alternative rock*.
Es ist zu bemerken dass *rock* zwar ebenfalls ein valider Pfad ist, aber 
als eine Untermenge von *alternative rock* nicht in der Ergebnismenge ist.

.. _single-dist:

Vergleichen der unterschiedlichen Genre-Pfade-Mengen
----------------------------------------------------

Um zwei einzelne Pfade miteinander zu Vergleich wird wie im Folgenden
vorgegangen:

- Zähle die Anzahl an Punkten in denen sich der Pfad überdeckt. 
- Teile die Anzahl durch die Länge des längeren beider Pfade.
- Die daraus gewonnene Ähnlichkeit wird von :math:`1.0` abgezogen um die Distanz
  zu erhalten.

In *libmunin* sind zwei Distanzfunktionen erhalten welche diese Methode nutzt um
zwei Mengen mit Genrepfaden zu vergleichen.

``GenreTree``: Vergleicht jeden Genrepfad in den Mengen *A* und *B* mittels oben
genannter Methode miteinander. Die minimalste Distanz wird zurückgegeben.  Als
Optimierung wird frühzeitig abgebrochen wenn eine Distanz von :math:`0.0`
erreicht wird.

Diese Distanzfunktion eignet sich für eher kurze Genre-Beschreibungen wie sie in
vielen Musiksammlungen vorkommen. Meist ist dort ein Lied als *rock* oder
*metal* eingetragen, ohne Unterscheidung von Subgenres. Deshalb geht diese
Distanzfunktion davon aus wenige Übereinstimmungen zu finden - sollten welche
vorkommen werden diese gut bewertet.

Setzt man voraus, dass *d* die unter :ref:`single-dist` erwähnte
Distanzunktion ist,  so berechnet sich die finale Distanz durch:

.. math::

   D(A, B) = \argmin\!\bigg(\displaystyle\sum\limits_{a \in A}{\displaystyle\sum\limits_{b \in B} d(a, b)}\bigg)


``GenreTreeAvg``: Seien *A* und *B* zwei Mengen mit Genrepfaden. *A* ist dabei
die größere Menge und *B* die kleinere, falls die Mengen eine unterschiedliche
Mächtigkeit besitzen.

.. math:: 

   D(A, B) = \frac{\displaystyle\sum\limits_{a \in A} \argmin\!{\Bigg(\displaystyle\sum\limits_{b \in B} d(a, b)\Bigg)}}{\vert A\vert}


Diese Distanzfunktion eignet sich für *,,reichhaltig''* befüllte
Genrebeschreibungen bei denen auch ein oder mehrere Unter-Genres vorhanden sind.
Ein Beispiel dafür wäre: ``country rock / folk / rockabilly``. Die
Distanzfunktion geht also davon aus zumindest teilweise Überdeckungen in den
Daten vorzufinden.

Je nach Daten die es zu verarbeiten gilt, kann der Nutzer der Bibliothek eine
passende Distanzunktion auswählen.

Probleme
--------

Insgesamt funktioniert dieser Ansatz relativ gut, die meisten Genre werden
zufriedenstellend in Pfade normalisiert die performant verglichen werden können.

Folgendes Problem wird allerdings noch nicht zufriedenstellend gelöst:
Es wird davon ausgegangen, dass Genres die ähnlich sind auch ähnlich heißen -
eine Annahme die zwar oft, aber nicht immer wahr ist. So sind die Genres
*Alternative Rock* und *Grunge* sehr ähnlich - der obige Ansatz würde hier
allerdings eine Distanz von :math:`0.0` liefern. Auch Genres wie *,,rock'n'roll*
würde ähnlich schlechte Resultate liefern.

Eine mögliche Lösung wäre eine Liste von ,,Synonymen'' Genres die
Querverbindungen im Baum erlauben würden. 

Allerdings wäre eine solche Liste von Synonymen relative schwer automatisch zu
erstellen. 

.. rubric:: Footnotes

.. [#f1] Der *API Key* wurde in der URL gekürzt da man angehalten ist diesen
   nicht zu veröffentlichen. 

.. [#f2] Anmerkung: Die Idee entstand allerdings ohne Kenntnis von *beets*.


Keword Extraction
=================

Problemstellung
---------------


RAKE zitieren/erklären.
Änderungen zum Default-Algorithmus.

Probleme
---------

Moodbar
=======

Problemstellung
---------------

Probleme
---------
