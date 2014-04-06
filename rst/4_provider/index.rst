#########################
Algorithmen bei Providern
#########################


Einleitung
===========

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

TODO: Colors!

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

TODO(?) Missing: DiscogsGenre.

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


Schlüsselphrasen--Extrahierung
==============================

Problemstellung
---------------

Eine Idee bei *libmunin* ist es auch die Liedtexte eines Liedes einzubeziehen,
um Lieder, die änhlichen *Themen* behandeln näher beieinander im Graphen zu
gruppieren. Sollten zwei Lieder nicht die selben Themen behandeln, so soll sich
zumindest die gleiche Sprache sich positiv auf die Distanz auswirken.

Um die Themen effizient zu vergleichen extrahiert *libmunin* aus den Liedtexten
die wichtigsten *Schlüsselphrasen* mittels des Keyword--Providers. Diese Phrasen
sollen den eigentlichen Inhalt möglichst gut approximieren, ohne dabei schwer
vergleichbar zu sein.

Der RAKE Algorithmus
--------------------

Zur Extrahieren von Schlüsselwörtern aus Texten gibt es eine Vielzahl von
Algorithmen.  Der verwendete Algorithmus zur Schlüsselphrasen--Extrahierung ist
bei *libmunin* der relativ einfach zu implementierende RAKE--Algorithmus
(vorgestellt in :cite:`berry2010text`). Zwar könnte man mit anderen Algorithmen
hier bessere Ergebnisse erreichen, diese sind aber schwerer zu implementieren
(was die Anpasspartkeit verschlechtert) und sind in den meisten Fällen von
sprachabhängigen Corpora (Wortdatenbanken) abhängig. 

*Beschreibung des RAKE--Algorithmus:*

1) Aufteilung des Eingabetextes in Sätze anhand von Interpunktion und
   Zeilenumbrüchen.
2) Extrahierung der *Phrasen* aus den Sätzen.  Ein *Phrase* ist hier definiert
   als eine Sequenz von Nichtstoppwörtern.  Um Stoppwörter zu erkennen muss eine
   von der Sprache abhängige Stoppwortliste geladen werden. Zu diesem Zweck hat
   *libmunin* 17 Stoppwortlisten in verschiedenen Sprachen eingebaut. Die
   Sprache selbst wird durch das Python Modul ``guess-language-spirit`` (TODO:
   LINK) anhand verschiedener Sprachcharakteristiken automatisch erraten. 
3) Berechnung eines *Scores* für jedes Wort in einem Phrase aus dem *Degree* und
   der *Frequenz* eines Wortes:

      :math:`degree(word) = len(phrase) - 1`

      :math:`freq(word) = \sum count(word) \forall word \in corpus`

      :math:`score(word) = \frac{degree(word) + freq(word)^{1.6}}{freq(word)}`

4) Für jeden Phrase wird nun ein *Score* berechnet. Dieser ist definiert als die
   Summe aller Wörter--*Scores* innerhalb des Phrases. Die derart bewerteten
   Phrasen werden absteigend sortiert als *Schlüsselphrasen* ausgegeben.
   *Schlüselphrasen* mit einem *Score* kleiner :math:`2.0` werden ausgesiebt.

Es wurde zudem einige Änderungen zum in :cite:`berry2010text` vorgestellten
Algorithmus vorgenommen, um diesen besser auf kleine Dokumente wie Liedtexte
abzustimmen:

- Im Original werden Sätze nicht anhand von Zeilenumbrüchen aufgebrochen.  Die
  meisten Liedtexte sind bestehen aus einzelnen Versen, die nicht durch Punkte
  getrennt sind, sondern durch eine neue Zeile abgegrenzt werden.
- Um die Ergebnisse leichter vergleichen zu können werden die einzelnen Wörter
  nach dem Extrahieren noch auf ihren Wortstamm reduziert. Dabei wird der
  sprachsensitive *Snowball--Stemmer* verwendet (link). 
- Im Original wird der *Wort--Score* als :math:`\frac{degree(word)}{freq(word)}`
  berechnet. Der von *libmunin* berechnete *Score* gewichtet die Wortfrequenz
  stärker. Der Exponent von :math:`1.6` wurde willkürlich nach einigen Tests
  gewählt: Mit diesem Exponent erscheint der Schlüsselphrase *Yellow Submarine*
  an erster Stelle im Liedtext von *,,Yellow Submarine"* der *Beatles*.
- Da sich viele Ausdrücke in Liedtexten wiederholen kamen während der
  Entwicklung viele Schlüsselphrasen in verschiedenen Variationen mehrmals vor.
  Oft waren diese dann eine Untermenge einer anderen Schlüsselphrase (Beispiel:
  *Yellow* und *Submarine* sind ein Teil von *Yellow Submarine*). Daher werden
  in einem nachgelagerten Schritt diese redundante Phrasen entfernt.
  
*Vergleich der einzelnen Schlüsselphrasenmengen:*

Die einzelnen Mengen von Schlüsselphrasen werden unter der Prämisse verglichen,
dass exakte Übereinstimmungen selten sind.

- Zu einem Drittel geht der Vergleich der Sprache in die Distanz ein. Ist die
  Sprache gleich so wird hier eine Teildistanz von :math:`1.0` angeommen,
  andernfalls ist die Gesamtdistanz :math:`0.0`, da dann auch ein Vergleich der
  einzelnen Schlüsselphrasen nicht mehr sinnvoll ist.
- Die restlichen zwei Drittel errechnen sich aus der Übereinstimmung der
  Schlüsselphrasen. Für zwei Schlüsselphrasen *A* und *B* errechnet sich die
  Distanz folgendermaßen:

  .. math::

      1 - \frac{\vert A\cup B\vert}{max(\vert A\vert, \vert B\vert)}

  Alle Schlüsselphrasen werden damit untereinander verglichen. Die minimalste
  dabei gefundene Distanz ist die finale Teildistanz.

Ergebnisse
----------

.. figtable::
   :spec: r l | r l
   :label: table-keywords
   :alt: Extrahierte Schlüsselphrasen aus verschiedenen Liedern.
   :caption: Extrahierte Schlüsselphrasen aus dem Volkslied 
             ,,Das Wandern ist des Müllers Lust“ (links) und dem
             Beatles--Song ,,Yellow Submarine“ (rechts).
              

   ============== ============================ ============== ================
   Score          Schlüsselphrasen *(Wandern)* Score          Schlüsselphrasen *(Yellow Submarine)*
   ============== ============================ ============== ================
   :math:`9.333`  *gerne  stille  stehn*       :math:`22.558` *yellow  submarin*
   :math:`5.778`  *wandern*                    :math:`20.835` *full  speed  ahead  mr*
   :math:`5.442`  *müllers  lust*               :math:`8.343` *live  beneath*
   :math:`5.247`  *müde  drehn*                 :math:`5.247` *band  begin*
   :math:`5.204`  *niemals  fiel*               :math:`3.297` *sea*
   :math:`5.204`  *herr  meister*               :math:`3.227` *green*
   :math:`5.204`  *frau  meisterin*             :math:`2.797` *captain*
   :math:`5.074`  *muntern  reihn*              :math:`2.551` *sail*
   :math:`5.031`  *schlechter  müller*          :math:`2.551` *blue*
   :math:`5.031`  *wanderschaft  bedacht*       :math:`2.551` *cabl*
   :math:`3.430`  *wasser*                      :math:`2.551` *life*
   :math:`3.430`  *steine*                      :math:`2.516` *sky*
   :math:`2.016`  *tanzen*                      :math:`2.516` *aye*
   :math:`2.016`  *frieden*                     :math:`2.016` *friend*
   :math:`2.016`  *gelernt*                     :math:`2.016` *aboard*
   :math:`2.016`  *schwer*                      :math:`2.016` *boatswain*
   ============== ============================ ============== ================
    
.. figtable::
   :spec: l | l
   :label: table-lyrics-wandern
   :alt: Liedtext des Volksliedes ,,Das Wandern ist des Müllers Lust“.
   :caption: Liedtext des Volksliedes ,,Das Wandern ist des Müllers Lust“.

   ===================================== ==================================
   Das Wandern ist des Müllers Lust,     Das sehn wir auch den Rädern ab,  
   Das Wandern!                          Den Rädern!                       
   Das muß ein schlechter Müller sein,   |br|
   Dem niemals fiel das Wandern ein,     Die gar nicht gerne stille stehn,
   Das Wandern.                          Die Steine selbst, so schwer sie sind,
   |br|                                  Die Steine!
   Vom Wasser haben wir’s gelernt,       Sie tanzen mit den muntern Reihn
   Vom Wasser!                           Und wollen gar noch schneller sein,
   Das hat nicht Rast bei Tag und Nacht, Die Steine.
   Ist stets auf Wanderschaft bedacht,   |br|                                      
   Das Wasser.                           O Wandern, Wandern, meine Lust,
   |br|                                  O Wandern!
   Die sich mein Tag nicht müde drehn,   Herr Meister und Frau Meisterin,
   Die Räder.                            Laßt mich in Frieden weiter ziehn
   *(oben rechts weiter)*                Und wandern.
   ===================================== ==================================
    
In Abb. :num:`table-keywords` sind die extrahierten Schlüsselphrasen aus zwei
Liedern aufgelistet. 

Zur Referenz ist unter Abb. :num:`table-lyrics-wandern` der Liedtextes des
Volkliedes ,,Das Wandern ist des Müllers Lust" abgedruckt. Der Text von
*,,Yellow Subarmine"* wird aus möglichen lizenzrechtlichen Gründen hier nicht
abgedruckt.

Wie man in Abb. :num:`table-keywords` sieht, werden längere phrasen automatisch
besser bewertet --- deren *Score* berechnet sich ja aus der Summe ihrer Wörter.
Auch sieht man, dass viele unwichtige Wörter wie *aboard* trotz Stoppwortlisten
noch in das Ergebniss aufgenommen werden.

    
Probleme
--------

Teilweise liefert diese Provider--Distanzfunktions--Kombination bereits
interessante Ergebnisse. So werden die beiden staatskritischen, deutschen Texte
*,,Hey Staat"* von *Hans Söllner* und *,,Lieber Staat"* von *Farin Urlaub* mit
einer relativ niedrigen Distanz von gerundet :math:`0.4` bewertet.

Doch nicht bei allen Texten funktioniert die Extrahierung so gut. Nimmt man den
Ausdruck *,,God save the Queen!"*, so wird *RAKE* diesen nicht als gesamten
Schlüsselphrase erkennen. Stattdessen werden zwei einzelne Phrasen generiert: 
*,,God save"* und *,,Queen"*, da *the* ein einglisches Stoppwort ist. 

Andererseits entstehen auch oft Schlüsselphrasen, die entweder unwichtig *(,,mal
echt")*, sinnentfremdet () oder stark kontextspezifisch () sind. Da ein Computer
den Text nicht verstehen kann, lässt sich das kaum vermeiden.

Auch gemischtsprachige Liedtexte lassen sich nur schwer untersuchen, da immer
nur eine Stoppwortliste geladen werden kann. Für Liedtexte mit starkem Dialekt
(wie von *Hans Söllner*) greift auch die normale hochdeutsche Stoppowortliste
nicht.

Moodbar
=======

Problemstellung
---------------

Die ursprünglich als Navigierungshilfe in Audioplayern gedachte Moodbar (siehe
:cite:`wood2005techniques` für genauere Informationen) wird in *libmunin* neben
der Beats--Per--Minute Bestimmung als einfache Form der
Audioanalyse eingesetzt. Kurz zusammengefasst wird dabei ein beliebiges
Audiostück zeitlich in 1000 Blöcke unterteilt. Für jeden dieser Blöcke wird ein
Farbwert (als RGB--Tripel) bestimmt. Der Rotanteil bestimmt dabei den Anteil
niedriger Frequenzen, der Grünanteil die mittleren Frequenzen und der Blauanteil
die hohen Frequenzen. Die Farbe Türkis deutet daher auf hohe und mittlere
Frequenzen in einem Block hin --- E--Gitarren haben häufig diese Farbe in der
Moodbar. Akustikgitarren erscheinen dafür meist in einem dunklem Rot.

Die Namensgebung des Verfahrens ist ein wenig irreführend. Man kann hier
keineswegs die subjektive Stimmung in einem Lied herauslese. Lediglich die
Bestimmung einzelner Instrumente ist als Annäherung möglich. Nach Meinung des
Autors sollte man das Verfahren daher eher *,,frequencebar"* oder ähnliches
nennen. Um aber auf die Einführung eines neuen Begriffes zu verzichten wird die
Namensgebung des Erfinders verwendet.

.. figure:: figs/mood_avril.*
    :alt: Beispiel--Moodbar von ,,Avril Lavigne -  Knockin' on Heaven's Door“
    :width: 100%
    :align: center

    Beispiel--Moodbar von ,,Avril Lavigne - Knockin' on Heaven's Door“.  Ein
    Lied bei dem hauptsächlich eine Akustikgitarre (rot) und Gesang (grünlich)
    im Vordergrund steht. Der Gesang setzt etwa bei 10% ein. Die Grafik wurde
    durch ein eigens zu diesem Zwekc geschriebenes Script gerendert. Deutlich
    sichtbar sind die einzelnen Pausen zwischen den Akkorden.

Vergleich von Moodbars
----------------------

Das Vergleichen verschiedener Moodbars gestaltet sich aufgrund der hohen 
Länge der einzelnen RGB--Vektoren als schwierig. In einem vorgelagerten
Analyseschritt wird daher versucht, die markanten Merkmale der einzelnen
Vektoren zu extrahieren. Dieser Analyseschritt wird dabei durch den
Moodbar--Provider getätigt.
 
Vor der eigentlichen Verarbeitung wird jeder Farbkanal in einzelne Blöcke
aufgeteilt, von der jeweils das arithmetische Mittel gebildet wird. So wird der
ursprüngliche 1000 Werte lange Vektor in momentan 20 einzelne, *handlichere*
Werte aufteilt. Bei einer durchschnittlichen Liedlänge von 4 Minuten entspricht
das immerhin 12 Sekunden pro Block, was für gewöhnliche Lieder ausreichend
sollte.

Nach einigen subjektiven Tests haben sich folgende Merkmale als *vergleichbar*
erwiesen:

* **Differenzsumme:** Für jeden Farbkanal wird die Summe der Differenzen zu den
  jeweiligen vorherigen Blockwert gebildet:

  .. math::

    \sum_{i=1}^{\vert C\vert} \vert C_{i} - C_{i-1}\vert \text{\,\,\,(C ist der Farbkanal)}

  Dieser Wert soll die grobe *,,Sprunghaftigkeit"* des Liedes beschreiben.
  Ändern sich die Werte für diesen Farbkanal kaum, so ist der Wert niedrig. 
  Liegen hohe Änderungen zwischen jedem Block vor, so steigt dieser Wert bis zu
  seinem Maximalen Wert von :math:`(20 - 1) \times 255 = 4845`.

* **Histogramm:** Für jeden Farbkanal wird eine Häufigkeitsverteilung, also ein
  Histogramm, abgespeichert. Jeder Farbwert wird dabei auf einen von 5 möglichen
  Bereichen, die jeweils 51 Werte umfassen, aufgeteilt. 
  So wird für jeden Farbkanal eine relativ einfach zu vergleichende Verteilung
  der Frequenzen abgespeichert.

* **Dominaten Farben:** Wie bereits erwähnt, ist es manchmal möglich bestimmte
  Instrumente visuell anhand deren charakteristischen Farbe zu erkennen. Das
  kann man sich beim Vergleichen zu Nutze machen, denn ähnliche Instrumente
  (ergo bestimmte, charakteristische Farben) deuten auf ähnliche Musikstile hin.
  Der Moodbar--Provider teilt daher jeden Farbkanal in 15er--Schritten in
  einzelne Bereiche auf. Jede Farbkombination wird dann einem dieser Bereich
  zugeordnet. Die 15 am häufigsten zusammen vorkommenden Tripel werden
  abgespeichert.
* **Schwarzanteil:** Gesondert werden sehr dunklen Farben behandelt. Haben
  alle Farbkanäle eines RGB--Tripels einen Wert kleiner 30, so wird die Farbe
  nicht gezählt, sondern auf einen *Schwarzanteil*--Zähler aufaddiert. 
  Geteilt durch 1000 ergibt sich daraus der Anteil des Liedes, das 

* **Durschnittliches Minimun/Maximum:** Für jeden Block wird das Minimum/Maximum
  aller 3 Farbkanäle bestimmt. Die Summe über jeden so bestimmten Wert, geteilt
  durch die Anzahl der Blöcke ergibt das durschnittliche Minimun/Maximum. Die
  Werte, die zwischen 0 und 255 liegen, sagen aus, in welchem Bereich sich die
  Frequenzen im Lied für gewöhnlich bewegen. 

.. figtable::
    :spec: l | r | l
    :label: table-moodbar-list
    :caption: Auflistung der einzelnen Werte die der Moodbar--Provider
              ausliest und deren dazugehörige Distanzfunktion, sowie deren
              Gewichtung in der Gesamtdistanz. ,,a“ und ,,b“ sind Skalare, mit
              Ausnahme der Histogramm--Eingabewerte. Dort sind ,,a“ und ,,b“ 
              die einzelnen Farbkanäle als Vektor. Zur Bildung der Gesamtdistanz
              werden die einzelnen Werte über einen gewichteten Mittelwert
              verschmolzen.
    :alt: Auflistung der einzelnen Moodbar--Merkmale.

    ==================================== ====================== ====================
    Name                                 Gewichtung             *ungewichtete* Distanzfunktion :math:`d(a, b)`
    ==================================== ====================== ====================
    *Differenzsumme*                     :math:`13,5\%`         :math:`1 - \sqrt{\frac{\vert a - b\vert}{50}}`                                               
    *Histogramm*                         :math:`13,5\%`         :math:`1 - \frac{\sum_{x}^{\vv{a} - \vv{b}}\vert x\vert}{5 \times 255}`  
    *Dominante Farben*                   :math:`63,0\%`         :math:`\frac{\vert a \cup b\vert}{max(\vert a \vert, \vert b \vert)}`                        
    *Schwarzanteil*                      :math:`5,0\%`          :math:`1 - \sqrt{\frac{\vert a - b\vert}{50}}`                                              
    *Durchschnittliches Minimum/Maximum* :math:`5,0\%`          :math:`1 - \sqrt{\frac{\vert a - b\vert}{255}}` 
    |hline| |nbsp|                       :math:`\sum 100\%`                                                                                                   
    ==================================== ====================== ====================

In :num:`table-moodbar-list` wird eine Auflistung der einzelnen Werte gegeben,
die der Moodbar--Provider generiert. Daneben werden auch die entsprechenden
Gewichtungen und Distanzfunktionen gegeben, mit dem die
Moodbar--Distanzfunktion, die einzelnen Werte verrechnet.

Am subjektiv *vergleichbarsten* erwiesen sich die dominanten Farben in einem
Lied. Die zwischenzeitlich aufgekommene Idee bestimmte markante Farbwertbereiche
bestimmten Instrumenten automatisch zuzuordnen erwies sich als unpraktikabel und
extrem ungenau.

Probleme
---------

.. _fig-mood-yellow-submarine:

.. figure:: figs/mood_yellow_submarine.*
    :alt: Diesselbe Moodbar bei unterschiedlichen Encoding der Audiodaten.
    :width: 100%
    :align: center

    Diesselbe Moodbar bei unterschiedlichen Encoding der Audiodaten. Oben das
    Beatles--Lied ,,Yellow Submarine“ als FLAC enkodiert, darunter dasselbe Lied
    mit relativ stark komprimierter MP3--Enkodierung. Die von libmunin
    berechnete Distanz ist hier etwa 0.01.

.. _fig-mood-rammstein-tier:

.. figure:: figs/mood_rammstein_tier.*
    :alt: Moodbar einer Live und einer Studioversion von ,,Rammstein --- Tier“
    :width: 100%
    :align: center

    Moodbar einer Live und einer Studioversion von ,,Rammstein --- Tier“. Oben
    die Studioversion, unten die Liveversion.  Hier ist die von libmunin
    errechnete Distanz immerhin bei 0.32. 

Das Hauptproblem ist, dass das Verfahren ursprünglich nicht zum Vergleichen von
Audiodaten ausgelegt war und vom Autor lediglich dafür *,,missbraucht"* wurde.
Wichtige Informationen wie die eigentliche Stimmung in dem Lied (von dunkel bis
positiv) bis hin zur Rhythmus des Liedes.. Lediglich die durchschnittliche
Geschwindigkeit wird vom BeatsPerMinute--Provider erfasst.  Daher ist der
Moodbar--Provider momentan eher als *Notbehelf* zu sehen.

Zudem ist die Geschwindigkeit der Audioanalyse eher dürftig. Geht das 
Analysieren des RGB--Vektors an sich vergleichsweise schnell, so ist die
Generierung desselben zeitlich aufwendig. Bei MP3--enkodierten Dateien dauerst
dies, je nach Größe, bis zu 4 Sekunden. Die Dauer variiert dabei je nach Format.
FLAC--enkodierte Dateien brauchen oft lediglich die Hälfte dieser Zeit. In
beiden Fällen ist die Anwendung bei einer mehreren zehntausend Lieder
umfassenden Sammlung aufwendig.

Vorteile sind hingegen:

- **Robustheit:** Wie man in :num:`fig-mood-yellow-submarine` sieht, ist das
  Verfahren relativ umempfdindlich gegen verschieden Enkodierungen. Selbst Live
  und Studioversionen zeigen gut vergleichbare Resultate (siehe Abb.
  :num:`fig-mood-rammstein-tier`).
- **Geringerer Speicherverbrauch:** Obwohl für die Implementierung die relativ
  speicherhungrige Sprache Python benutzt wurde, nutzt der Moodbar--Provider
  lediglich etwa 540 Bytes pro Analysedatensatz. Da Python die Zählen -10 bis
  255 im Speicher hält und der Moodbar--Provider nur Zahlen in diesem Bereich
  erzeugt reichen hier 8 Byte für eine Referenz auf einen Integer aus. 
