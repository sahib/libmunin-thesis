***************
Zusammenfassung
***************

Was wurde erreicht?
===================

:dropcaps:`Es` wurde eine Softwarebibliothek in Python implementiert, die ein
Musikempfehlungssystem auf Graphen-Basis mit einer flexiblen Schnittstelle
bietet. Das System lernt dabei vom Nutzer mittels expliziten (Vergeben von
Ratings) und impliziten (Beobachtung des Endnutzers und Ableitung von
Assoziationsregeln) Methoden.

Es wurde eine große Anzahl von sogenannten *Providern* zum Normalisieren der
Eingabedaten, sowie eine entsprechend hohe Anzahl von *Distanzfunktionen*
implementiert welche diese Daten vergleichen können.
Im Vergleich zu bestehenden Systemen ist man nicht von Audiodaten abhängig.
Durch die freie Lizenz ist ein weitläufiger Einsatz möglich.

Was hatte das mit Data-Mining zu tun?
=====================================

*Data-Mining* meint landläufig das automatisierte *Abbauen* von unerwarteten
Wissen aus einem großen *Datenberg*. So gesehen ist *libmunin* die *Spitzhacke*
für *Musikdatenbanken*.

Insgesamt wurden hauptsächlich folgende Techniken aus diesem Gebiet genutzt:

* *Warenkorbanalyse* um *Assoziationsregeln* abzuleiten.
* Verschiedene *Distanzfunktionen* und *Fusionierungsverfahren*.
* *Spracherkennung* und *Keyword-Extrahierung*.
* Verschiedenste *Normalisierung* von Eingabedaten.

Welche Anforderungen wurden nicht oder unvollständig erfüllt?
=============================================================

Unabhängigkeit von der Programmiersprache
-----------------------------------------

Momentan ist *libmunin* nur von *Python* aus zu benutzen. Dies ist zum Teil dem
Format geschuldet in dem die internen Daten abgespeichert werden: Dem
Python-spezifischen ``pickle`` Format, welches beliebige Python-Objekte
serialisieren kann, macht es natürlich schwierig Software zu schreiben die
eine serialisierte *Session* einlesen kann ohne dabei auf *libmunin* oder
*Python* zurückzugreifen. 

Davon unabhängig ist *libmunin* momentan durch die Implementierung in Python auf
diese Sprache eingeschränkt. Für solche Probleme gibt es zwei populäre
Lösungsansätze. Der erste ist das Schreiben von *Languagebindings* für die
Zielsprache --- das würde erheblichen Aufwand involvieren wenn mehr als einige
wenige Sprachen unterstützt werden sollen. Die zweite Möglichkeit ist eine
Aufteilung in *Server* (der dann in Python geschrieben wäre) und *Client* (der
in einer beliebigen Programmiersprache geschrieben ist).
Der *Client* könnte dann über ein definiertes Protokoll auf die Funktionen des
Servers zurückgreifen --- das ist beispielsweise die Herangehensweise von MPD.

Ein konkrete Umsetzung dieser Idee könnte relativ einfach mit *D-Bus* [#f1]_
erreicht werden. Der Server würde dabei die API von *libmunin* als
*D-Bus Service* implementieren. Der Client könnte eine der in zahlreichen
Programmiersprachen verfügbaren *DBus-Libraries* nutzen, um im Server Methoden
aufzurufen. Darüber ließe sich auch ein anderes Randproblem lösen: Falls mehrere 
Programme die gleiche Session nutzen wollen --- momentan ist das aus Gründen der 
Nebenläufigkeit noch nicht möglich.

.. rubric:: Footnotes

.. [#f1] Ein unter Unix sehr weit verbreitetes IPC-Framework und Messagebroker,
         bei dem Services in einem *Bus* bereitgestellt werden. Clients können
         dann, ähnlich wie bei RPC, Methoden auf den Services aufrufen.

Einfaches Information Retrieval
-------------------------------

Die Ergebnisse die *libmunin* liefern kann, können nur so gut sein wie die
Eingabedaten. Sind diese falsch oder unzureichend (durch schlechtes Tagging
etwa), wird auch eine gute :term:`Distanzfunktion` nur mittelmäßig genaue
Ergebnisse erzielen. 

Momentan bietet *libmunin* bereits dem Nutzer Möglichkeiten an um fehlende
Songtexte und Genre-Tags aus dem Internet zu besorgen. In der Einleitung dieser
Arbeit wurden aber schon freie Musikmetadatenbanken wie *MusicBrainz* erwähnt
die mittels eines Audiofingerprints die Metadaten eines Stückes nachschlagen
können. 

Glücklicherweise steht mit *beets* :cite:`XAJ` bereits ein entsprechendes,
praktischerweise in Python geschriebenes Tool bereit --- gewissermaßen das
*libhugin* für Musik.  In Zukunft könnte *beets* zusammen mit *libglyr also den
*Information Retrieval* Teil übernehmen, ohne dass *libmunin* das Rad dafür neu
erfinden muss.

Implementierungsdefizite
========================

Performance
-----------

Vermeidung unnötiger Vergleiche
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Der Aufruf von einigen Distanzfunktionen macht nur dann Sinn, wenn bestimmte
Kriterien erfüllt sind. So macht es beispielsweise wahrscheinlich wenig Sinn die
``moodbar`` zweier Songs zu vergleichen wenn sich die Stücklänge um mehr als das
doppelte unterscheidet --- die Daten wären einfach zu unterschiedlich.

Momentan ist es allerdings noch nicht möglich für die ``moodbar``-Distanzfunktion
die Länge des Stückes abzufragen --- da sie nur die für sie relevanten Daten
bekommt, nicht die ganze ``Song``-Instanz.

Beschleunigung des Kaltstarts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Alle Operationen von *libmunin* verlaufen momentan sequentiell. Dabei ließen
sich zumindest einige Teile des *Kaltstartes* optimieren indem eine gewisse
Anzahl von Songtexten (oder anderem *Information Retrieval*) parallel
heruntergeladen werden. Auch das Analysieren von Audiodaten könnte beschleunigt
werden indem ein (bei normalen Festplatten)  oder mehrere (bei SSDs) *Threads*
Audiodaten einliest und diese dann an *Workerthreads* weiterleitet, die die
eigentliche Analyse durchführen.

Korrektheit
-----------

Speicherung
~~~~~~~~~~~

Wie oben erwähnt erfolgt die Speicherung der *Session* mittels Python's
``pickle`` Modul. Dieses serialisiert *rekursiv* die Objekt-Hierarchie,
ausgehend vom *Session* Objekt. Da in *libmunin* der Graph allerdings als
rekursive Datenstruktur implementiert ist ,,verläuft" sich ``pickle`` darin -
zu hohe Rekursionstiefen entstehen bei ausreichend komplexen Graphen. 

Python hat ein eingebautes *Rekursionslimit* welches ein wenig aussagekräftiges
*Segmentation Fault* verhindern soll --- Abstürze beim Speichern der *Session*
sind die Folge. Hier ist Abhilfe nötig.

Korrekte Berechnung des *BPM-Wertes*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Die Berechnung des *Beats-Per-Minute*-Wertes ist momentan in ein separates Tool
ausgelagert. Dieses Tool hat das Problem, dass es bei fehlerhaften Dateien oder
Formaten die es nicht versteht fehlerhafte (beispielsweise Werte *über* 300 bpm)
Werte zurückgibt. 

Denkbare Weiterentwicklungen
============================

Abgesehen von den obigen Defiziten hier noch einige Stichpunktartige Richtungen
in denen die Implementierung verbessert werden kann:

- Verläufe: Manchmal ist es wünschenswert dass die dynamisch erstellte Playlist
  einem gewissen Verlauf folgt. Man denke an eine Party bei der erst schnelle,
  fröhliche Musik gespielt wird, zum Ende hin dann langsame, ruhigere Musik.
- Weitere Empfehlungs-Strategien, wie beispielsweise von rein Genre-basierenden 
  Empfehlungen.
- Justierbarkeit der Gewichtungen während der Laufzeit --- Momentan erfordert die
  Justierung der Gewichtung eine ``rebuild``-Operation.
- ,,Echte" Audio/Mood-Analyse mittels *aubio* :cite:`0FN` oder *MARSYAS* :cite:`HJ7`.
- Optionaler Aufsatz auf *libmunin* der *Social-based music recommendation*
  ermöglicht --- beispielsweise um die Ähnlichkeit von zwei Künstlern durch
  Amazon-Reviews zu bestimmen. Sind diese in der Datenbank nicht vorhanden wird
  die Ähnlichkeit --- wie jetzt schon --- automatisch bestimmt.
- Portierbarkeit auf andere Plattformen, momentan wurde nur Linux getestet.

Abschließendes Fazit
====================

*libmunin* ist ein solide Fundament für weitere Entwicklungen --- und so flexibel
dass mit entsprechenden *Providern* und *Distanzfunktionen* sogar
Empfehlungs-Systeme für andere Dokumente wie Videos, Bücher oder Filmen möglich
wären.

Noch ist der Einsatz relativ kompliziert und erfordert, auch für kundige
Entwickler, einiges an Einarbeitungszeit --- zuviel für etwas das einfach nur im
Hintergrund arbeiten sollte. Auch die erstellten Empfehlungen sind --- subjektiv
gesehen --- noch teilweise verbesserungswürdig. Besonders die momentane
Audioanalyse ist sehr primitiver Natur und bietet einiges an Potenzial an
Verbesserungen. Es wird momentan mehr auf *Masse* statt auf *Klasse* gesetzt und
oft ist einiges an *,,Kaffeesatzleserei"* enthalten.

Da das Projekt auch nach Abschluss dieser Arbeit, im Rahmen von *Moosecat*
weiter entwickelt werden soll, hofft der Autor mit der Zeit mehr Richtung
*Klasse* zu gehen --- dann wäre das Projekt eine echte Alternative für viele der
in der Einleitung genannten Projekte.
