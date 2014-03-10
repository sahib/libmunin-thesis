***********************
Demonstrationsanwendung
***********************

Intro
=====

:dropcaps:`Abseits` der Bibliothek wurde eine, auf dem freien
Oberflächen--Framework :math:`\text{GTK+-}3.0` basierende, GUI-Anwendung
entwickelt.  Wie eingangs erwähnt, dient diese nicht nur zum *Showoff*, sondern
auch zur gezielten Fehlersuche.

Die Anwendung, die den ebenfalls nordischen Namen *Naglfar* erhielt, stellt
einen MPD-Client bereit. Im Hintergrund werkelt dabei *Moosecat*.  Vor der
ersten Benutzung muss gemäß Abb. :num:`fig-startup` eine Session aufgebaut
werden. Dies erledigt das Skript ``coldstart.py`` (siehe
:ref:`coldstart-example` im *Angang C*). Dies kann durch das Ziehen der
Liedtexte und der Audioanalyse beim ersten Lauf sehr lange dauern --- bis zu
zwei Stunden. Danach sind allerdings die Liedtexte zwischengelagert und der
zweite Lauf dauert dann nur noch wenige Minuten. 

Nach dem ``coldstart.py`` die *Session* auf die Platte geschrieben hat, kann die
eigentliche Anwendung gestartet werden. Diese verbindet sich zuallererst mit
einem MPD-Server der auf *localhost* unter Port *6601* lauscht. Dort  beschafft
sich die Anwendung alle Metadaten, um die *Playlist* und *Database*-Ansicht zu
befüllen.  Danach wird besagte *Session* geladen. Nach der Initialisierung der
*GUI* ist die Anwendung nun bereit benutzt zu werden.

Damit zwischen den von *libmunin* herausgegebenen Empfehlungen und den internen
Songs unterschieden werden kann, generiert ``coldstart.py`` eine Hashtabelle, die
zwischen den *ID* von *libmunin's* Songs und den Dateipfaden innerhalb der
Musikdatenbank eine Beziehung herstellt. Diese Hashtabelle wird in der Session
gespeichert. Die Musikdatenbank selbst besteht dabei aus *666* ausgewählten
Liedern aus der privaten Musiksammlung des Autors.

Anwendungsübersicht
===================

In Abb. :num:`fig-demo-overview` wird eine Übersicht über die GUI der Anwendung
gegeben. Detailliertere Ansichten werden unter :ref:`demo-pics` gezeigt.  Im
Folgenden wird nun eine textuelle Übersicht über die *Features* der Anwendung
gegeben.

Ansichten
---------

Die Anwendung ist in unterschiedliche *Ansichten* (englisch *Views*) aufteilt,
die jeweils in unterschiedlichen Reitern stecken. Im Folgenden wird eine Übersicht
über alle *Views* gegeben:

* **Database:** Siehe Abb. :num:`fig-demo-database`.
   
  Anzeige der gesamten Musikdatenbank durch die Spalten ``Artist``, ``Album``,
  ``Titel``, ``Datum`` und ``Genre``. Jede Zeile entspricht dabei einem Song. 
  Ein Rechtsklickmenü auf einen beliebigen Song fördert ein Kontextmenü zu Tage
  (siehe Abb. :num:`fig-demo-context-menu`), dass mehrere Möglichkeiten
  bietet, um die Playlist mit Empfehlungen zu befüllen (entsprechend Kapitel
  :ref:`list-of-recom-strategies`).  Im Folgenden ist :math:`N` die Anzahl
  der gewünschten Empfehlungen, die im Empfehlungszähler (siehe
  Nr. 5 in Abb. :num:`fig-demo-overview`) eingestellt ist.
  
  * **Ausgewählten Song als Seedsong nehmen:** Erstellt :math:`N`
    Empfehlungen basierend auf dem selektierten Song und reiht sie in die Playlist
    ein. 
  
  * **Playlist säubern und ausgewählten Song als Seedsong nehmen:** Wie oben,
    leert aber vor dem Einreihen die Playlist.
  
  * **Suche einen Seedsong mit einem bestimmten Attribut:** Sucht einen
    Seedsong nach bestimmten Kriterien, die der Nutzer im Eingabefeld oben
    rechts angeben kann. Dort kann ein *Suchbegriff* in der folgenden Form
    angegeben werden::
    
        <attribut>: <wert>[, <attribut>: <wert>, ...]
    
    Folgendes Beispiel findet alle Songs mit dem Künstler *,,Billy Talent"* **und**
    dem Genre *,,Rock"*::
    
        genre: rock, artist: Billy Talent
    
    Werden mehrere Suchergebnisse gefunden, so werden alle als Seedsongs
    genutzt, um in die Playlist :math:`N` neue Songs einzureihen.
    
    Diese Funktionalität ist momentan relativ eingeschränkt, da nur exakte
    Treffer funktionieren. Ist das *Genre* also als *,,rock / pop"* getaggt, so
    wird die Suche erfolglos verlaufen.
  
  * **Lasse libmunin einen Seedsong auswählen:** *libmunin* wählt automatisch
    einen Seedsong nach folgenden Kriterien (gemäß Kapitel
    :ref:`list-of-recom-strategies`):
    
    1. Nutze die Seedsongs, die in der am besten bewertesten Regel vorkommen.
    2. Falls keine Regel vorhanden, nutze den meist abgespielten Song als
       Seedsong.
    3. Schlägt auch das fehl wird ein zufälliger Song ausgewählt.
    
    In allen Fällen werden dann :math:`N` Empfehlungen in die Playlist
    eingereiht.
  
  * **Erstelle eine komplett zufällige Playlist:** Reiht :math:`N` neue,
    komplett zufällig aus der Datenbank gewählte, Songs in die Playlist ein.
    Nützlich um die komplett zufällige Playlist mit einer von *libmunin* erstellten
    Playlist zu vergleichen. Der Seed für die ``random()``-Funktion ist dabei immer
    gleich, daher erstellt dies nach einem Neustart stets dieselbe Liste.
  
  .. _fig-demo-context-menu:
  
  .. figure:: figs/demo_context_menu.png
      :alt: Das Kontextmenu in der Playlist und Database Ansicht
      :width: 30%
      :align: center
  
      Die Einträge des Kontextmenüs in der Playlist und Database Ansicht 

**Playlist:** Siehe Abb. :num:`fig-demo-playlist`.

Wie die *Database--Ansicht*, zeigt aber lediglich die Songs an, die empfohlen
wurden. Sonst ist diese Ansicht funktionsidentisch mit der *Database--Ansicht*.

**Graph:** Siehe Abb. :num:`fig-demo-graph`.

In der *Graphenansicht* kann ein Plot von *libmunin's* Graphen begutachtet werden.
Dies ist oft nützlich, um nachzuvollziehen welche Empfehlungen aus welchen Grund
gegeben wurden, da man im Graphen die Nachbarn eines Seedsongs betrachten
kann.

**Rules:** Siehe Abb. :num:`fig-demo-rules`.

In einer Liste werden alle bekannten Assoziationsregel
angezeigt. Dabei wird neben beiden Seiten der Regel auch der *Supportcount*
und das *Rating* der Regel angezeigt. Beide werden hier nicht näher erklärt.

**Examine:** Siehe Abb. :num:`fig-demo-examine`.

Hier werden alle Attribute des momentan spielenden Songs angezeigt.  Es wird die
von *libmunin* normalisierte Form angezeigt, als auch, falls verfügbar, der
Originalwert.  Zudem wird die ``moodbar`` (falls vorhanden) oben im Fenster
geplottet.

**History:** Siehe Abb. :num:`fig-demo-history`.

Neben einer chronologischen Auflistung aller Songs die in letzter Zeit
gehört wurden (Begrenzung auf 1000 Stück), werden hier auch die zuletzt 
ausgestellten Empfehlungen (Begrenzung auf 10 Stück) angezeigt.
Letzteres ist für das Debugging der Filterfunktion nützlich.

Weitere Steuerlemente
---------------------

Aus Gründen der Vollständigkeit werden hier, die unter Abb.
:num:`fig-demo-overview` gezeigten Elemente noch erklärt.

2. **Seedsong:** Zeigt mit einem roten Kreis den zuletzt ausgewählten
   Seedsong an.  Falls es mehrere Seedsongs gab, wird nur der erste
   markiert.

3. **Current Song:** Ein dreieckiges Icon, das den aktuell spielenden (oder
   pausierten) Song anzeigt.

4. **Playlist:** Die Playlist--Ansicht, wie bereits oben gezeigt.

5. **Empfehlungszähler:** Die Anzahl an Empfehlungen, die ein Klick im
   Kontextmenü liefert.

6. **Filter:** Togglebutton (:math:`$,,\sout{a}”$` als Icon) der anzeigt, ob
   der Filtermodus aktiviert ist.  Ist er aktiv, so darf sich in einer dynamisch
   erstellten Playlist der Künstler nur alle drei Stücke wiederholen, der selbe
   Künstler *und* das selbe Album nur alle fünf Stücke.

7. **Mininmaler Höranteil:** Ein Klick auf den Button fördert einen Slider zu
   Tage auf dem man eine Prozentzahl einstellt. Diese legt fest, welcher Anteil
   eines Liedes (in Prozent) *mindestens* angehört werden muss, damit er zur
   Historie hinzugefügt wird.
   
   Um diese Funktionalität zu realisieren, musste *Moosecat* um diese
   Funktionalität erweitert werden.

8. **Attributsuche:** Eingabe einer Folge von Attribut--Werte--Paaren die ein
   Seedsong bei der Attributsuche  haben sollte.

9. **Rating:** Ein spezielles Steuerelement, in den man das *Rating* des aktuell
   spielenden Songs setzen kann. Beim Erstellen der *Session* durch
   ``coldstart.py`` wird ein ungesetztes *Rating* von ,,:math:`0`" angenommen.
   
   Zum Setzen klickt man einfach ins Feld, die Seite links vom Cursor wird dann
   eingefärbt.  Es ist möglich etwas links vom ersten Stern zu klicken, um das
   Rating auf ,,0" (und damit *ungesetzt*) zurückzusetzen.
   
   Ein Ändern des Ratings hat ein Neuzeichnen des Graphen in der Graphen--Ansicht
   zufolge. Dies liegt daran, dass das Ändern des Ratings mittels der
   ``modify``--Operation erfolgt. Diese fügt den Song an einer möglicherweise
   anderen Stelle im Graphen wieder ein.

10. **Playcount:** Zeigt an wie oft ein Lied bereits gehört wurde. Ein Lied gilt
    als nicht gehört, wenn prozentuell nur ein kleiner Teil als der gesetzte
    minimale Höranteil angehört wurde.
   
    Zur optischen Vorhebung ist es mit einer Fortschrittsanzeige hinterlegt.
    Sobald man 100 mal ein Lied hört, zeigt diese vollen Füllstand an.

11. **Volumebar** Regler für die Lautstärke. 

12. **Title Label:** Zeigt das aktuell spielende Lied mit Titel, Album und
    Künstler an.

13. **Modebuttons:** Umschalten zwischen *Random* (nächstes Lied ist zufällig),
    *Single* (höre nach diesem Lied auf zu spielen), *Repeat* (spring zum Anfang
    der Playlist nach dem letzten Lied) und *Consume* (Lösche das Lied aus der
    Playlist nach dem Abspielen).

14. **Seekbar:** Ermöglicht das wahlfreie Hin- und Herspringen innerhalb des
    aktuellen Liedes.  Übersprungene Abschnitte eines Liedes fließen nicht in
    den *Höranteil* ein. Doppelt gehörte Parts schon.  Daher sind Werte
    :math:`\ge 100\%` möglich.

15. **Playbuttons:** Die ,,üblichen" Kontrollen eines Musicplayers zum
    *Pausieren/Abspielen* (an momentaner Stelle anhalten/weiterspielen),
    *Stoppen* (Anhalt und zum Anfang der Playlist springen), *Nächstes* und
    *Vorheriges* Lied .

16. **Suche:** Erlaubt das Filtern der Playlist oder Datenbank.
   
    Suchbegriffe können einfacher Natur wie *,,beat"* (Findet alles das
    *,,beat"* im Künstler-, Album- oder Titel--Tag beeinhaltet) sein. Oder auch
    eher komplizierter Natur: *,,(genre:rock + y:2001..2003) | artist:Beat"*
    (Findet alles das *,,rock"* im Genre hat und in den Jahren *2001* bis
    einschließlich *2003* released wurde, oder dessen Künstler ein Wort enthält,
    das mit ,,Beat" beginnt).
     
    *Anmerkung:* Die ,,Such--Engine" dahinter ist in *Moosecat* implementiert.
    Die Suche kann mit :kbd:`Strg-f` oder :kbd:`/` *(Slash)* aktiviert und mit
    :kbd:`Esc` wieder versteckt werden.

.. _fig-demo-overview:

.. figure:: figs/demo_overview.*
    :alt: Übersicht über die Demoanwendung
    :width: 80% 
    :align: center
    
    Übersicht über die Demonanwendung.
