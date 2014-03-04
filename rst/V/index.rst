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
einen MPD-Client bereit. Im Hintergrund werkelt dabei *Moosecat*.

Vor der ersten Benutzung muss gemäß :num:`fig-startup` eine Session aufgebaut
werden --- dies erledigt das Skript ``coldstart.py`` (siehe
:ref:`coldstart-example` im *Angang C*) --- dies kann durch das Ziehen der
Songtexte und der Audioanalyse beim ersten Lauf sehr lange dauern --- bis zu 2
Stunden. Danach sind allerdings die Liedtext zwischengelagert und der zweite
Lauf dauert dann nur noch wenige Minuten. 

Nach dem ``coldstart.py`` die *Session* auf die Platte geschrieben hat, kann die
eigentliche Anwendung gestartet werden. Diese verbindet sich zuallererst mit
einem MPD-Server der auf *localhost* unter Port *6601* lauscht und besorgt sich
dort alle Metadaten um die *Playlist* und *Database*-Ansicht zu befüllen. Danach
wird besagte *Session* geladen. Nach der Initialisierung der *GUI* ist die
Anwendung nun bereit benutzt zu werden.

Damit zwischen den von *libmunin* herausgegebenen Empfehlungen und den internen
Songs unterschieden werden kann, generiert ``coldstart.py`` eine Hashtable, die
zwischen den *ID* von *libmunin's* Songs und den Dateipfaden innerhalb der
Musikdatenbank eine Beziehung herstellt. Diese Hashtable wird in der Session
gespeichert.

Anwendungsübersicht
===================

In :num:`fig-demo-overview` wird eine Übersicht über die GUI der Anwendung
gegeben. Detailliertere Ansichten werden am Ende des Kapitels gezeigt.

Im Folgenden wird nun eine Übersicht über die *Features* der Anwendung gegeben.

Ansichten
---------

Die Anwendung ist in unterschiedliche *Ansichten* (englisch *Views*) aufteilt
die jeweils in unterschiedlichen Tabs stecken. Im folgenden wird eine Übersicht
über alle *Views* gegeben:

* **Database:** Siehe Abbildung :num:`fig-demo-database`.
   
  Anzeige der gesamten Musikdatenbank durch die Spalten ``Artist``, ``Album``,
  ``Titel``, ``Datum`` und ``Genre``. Jede Zeile entspricht dabei einem Song. 
  
  Ein Rechtsklickmenü auf einen beliebigen Song fördert ein Kontextmenü zu Tage
  (siehe Abbildung :num:`fig-demo-context-menu`), dass mehrere Möglichkeiten
  bietet um die Playlist mit Empfehlungen zu befüllen (entsprechend
  :ref:`list-of-recom-strategies`).  Im folgenden ist :math:`N` die Anzahl
  der gewünschten Empfehlungen, die im Empfehlungszähler (siehe
  Nr. 5 in :num:`fig-demo-overview`) eingestellt ist.
  
  * **Ausgewählter Song als Seedsong:** Erstellt :math:`N`
    Empfehlungen basierend auf dem selektierten Song und reiht sie in die Playlist
    ein. 
  
  * **Playlist säubern und ausgewählter Song als Seedsong:** Wie oben,
    leert aber vor dem Einreihen die Playlist.
  
  * **Suche einen Seedsong mit einem bestimmten Attribut:** Sucht einen
    Seedsong nach bestimmten Kriterien, die der Nutzer im Eingabefeld oben
    rechts angeben kann. Dort kann ein *Suchbegriff* in der folgenden Form
    angegeben werden::
    
        <attribut>: <wert>[, <attribut>: <value>, ...]
    
    Folgendes Beispiel findet alle Songs mit dem Künstler *,,Billy Talent"* **und**
    dem Genre *,,Rock"* ::
    
        genre: rock, artist: Billy Talent
    
    Werden mehrere Suchergebnisse gefunden so werden alle als Seedsongs genutzt um
    in die Playlist :math:`N` neue Songs einzureihen.
    
    Diese Funktionalität ist momentan relativ eingeschränkt da nur exakte Treffer
    funktioneren. Ist das *Genre* also als *,,rock / pop"* getaggt, so wird die
    Sucher erfolglos verlaufen.
  
  * **Lasse libmunin einen Seedsong auswählen:** *libmunin* wählt
    automatisch einen Seedsong nach folgenden Kriterien:
    
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

**Playlist:** Siehe Abbildung :num:`fig-demo-playlist`.

Wie die *Database--Ansicht*, zeigt aber lediglich die Songs an die empfohlen
wurden. Sonst ist diese Ansicht funktionsidentisch mit der *Database--Ansicht*.

**Graph:** Siehe Abbildung :num:`fig-demo-graph`.

Im *Graphen--Ansicht* kann ein Plot von *libmunin's* Graphen begutachtet
werden. Dies ist oft nützlich um nachvollziehen welche Empfehlungen warum
gegeben wurden.

**Rules:** Siehe Abbildung :num:`fig-demo-rules`.

In einer Liste werden alle bekannten Assoziationsregel
angezeigt. Dabei wird neben beiden Seiten der Regel auch der Supportcount
und das Rating der Regel angezeigt.

**Examine:** Siehe Abbildung :num:`fig-demo-examine`.

Hier werden alle Attribute des momentan spielenden Songs angezeigt.  Es wird die
von *libmunin* normalisierte Form angezeigt, also auch, falls verfügbar, der
Originalwert.  Zudem wird die ``moodbar`` (falls vorhanden) oben im Fenster
geplottet.

**History:** Siehe Abbildung :num:`fig-demo-history`.

Neben einer chronologischen Auflistung aller Songs die in letzter Zeit
gehört wurden (Begrenzung auf 1000 Stück) werden hier auch die zuletzt 
ausgestellten Empfehlungen (Begrenzung auf 10 Stück) angezeigt.

Letzteres ist für das Debugging der Filterfunktion nützlich.

Weitere Steuerlemente
---------------------

Aus Gründen der Vollständigkeit werden hier, die unter :num:`fig-demo-overview`
gezeigten Elemente noch erklärt.

2. **Seedsong:** Zeigt mit einem roten Kreis den zuletzt ausgewählten
   Seedsong an.  Falls es mehrere Seedsongs gab, wird nur der erste
   markiert.

3. **Current Song:** Ein dreieckiges Icon das den aktuell spielenden (oder
   pausierten) Song anzeigt.

4. **Playlist:** Die Playlist--Ansicht, wie bereits oben gezeigt.

5. **Empfehlungszähler:** Die Anzahl an Empfehlungen die ein Klick im
   Kontextmenü liefert.

6. **Filter:** Togglebutton (:math:`$\sout{a}$` als Icon) der anzeigt ob
   der Filtermodus aktiviert ist.  Ist er aktiv so darf sich in einer dynamisch
   erstellten Playlist der Künstler nur alle 3 Stücke wiederholen, der selbe
   Künstler *und* das selbe Album nur alle 5 Stücke.

7. **Mininmaler Höranteil:** Ein Klick auf den Button fördert einen Slider zu
   Tage auf dem man eine Prozentzahl einstellt. Diese legt fest welcher Anteil
   eines Liedes (in Prozent) *mindestens* angehört werden muss damit er zur
   Historie hinzugefügt wird.
   
   Um diese Funktionalität zu realisieren musste *Moosecat* um diese
   Funktionalität erweitert werden.

8. **Attributsuche:** Eingabe einer Folge von Attribut--Werte Paaren die ein
   Seedsong bei der Attributsuche  haben sollte.

9. **Rating:** Spezielles Widget auf den man das *Rating* des aktuell spielenden
   Songs zu setzen. Beim erstellen der *Session* durch ``analyse.py`` wird ein
   *Rating* von :math:`0` angenommen --- also *ungesetzt*.
   
   Zum Setzen klickt man einfach ins Feld, die Seite links vom Cursor wird dann
   eingefärbt.  Es ist möglich etwas links vom ersten Stern zu klicken um das
   Rating auf ,,0" (und damit *ungesetzt*) zurückzusetzen.
   
   Ein Ändern des Ratings hat ein Neuzeichnen des Graphen in der Graphen--Ansicht
   zufolge.

10. **Playcount:** Zeigt an wie oft ein Lied bereits gehört wurde. Ein Lied gilt
    als nicht gehört wenn prozentuell nur ein kleiner Teil als der gesetzte
    minimale Höranteil angehört wurde.
   
    Zur optischen Vorhebung ist es mit einer Fortschrittsanzeige hinterlegt ---
    sobald man 100x mal ein Lied hört, zeigt diese vollen Füllstand an.

11. **Volumebar** Regler für die Lautstärke. 

12. **Title Label:** Zeit das aktuell spielende Lied mit Titel, Album und
    Künstler an.

13. **Modebuttons:** Umschalten zwischen *Random* (nächstes Lied ist zufällig),
    *Single* (höre nach diesem Lied auf zu spielen), *Repeat* (spring zum Anfang
    der Playlist nach dem letzten Lied) und *Consume* (Lösche das Lied aus der
    Playlist nach dem Abspielen).

14. **Seekbar:** Ermöglicht das wahlfreie Hin- und Herspringen innerhalb des
    aktuellen Liedes.  Übersprunge Parts eines Liedes fließen nicht die
    *Höranteil* ein, doppelt gehörte Parts schon --- daher sind Werte :math:`\ge
    100\%` möglich.

15. **Playbuttons:** Die ,,üblichen" Kontrollen eines Musicplayers zum
    *Pausieren/Abspielen* (an momentaner Stelle anhalten/weiterspielen),
    *Stoppen* (Anhalt und zum Anfang der Playlist springen), *Nächstes* und
    *Vorheriges* Lied .

16. **Suche:** Erlaubt das Filtern der Playlist oder Datenbank.
   
    Suchbegriffe können einfacher Natur wie *,,beat"* (Findet alles das *,,beat"*
    im Artist, Album oder Titel--Tag beeinhaltet) bis hin zu sehr komplizierten
    Suchbegriffen wie *,,(genre:rock + y:2001..2003) | artist:Beat"* (Findet
    alles das *,,rock"* im Genre hat und in den Jahren *2001* bis einschließlich
    *2003* released wurde, oder dessen Künstler ein Wort enthält, dass mit
    ,,Beat" beginnt).
     
    *Anmerkung:* Die ,,Such--Engine" dahinter ist in *Moosecat* implementiert.
    
    Die Suche kann mit :kbd:`Strg-f` oder :kbd:`/` *(Slash)* aktiviert und mit
    :kbd:`Esc` wieder versteckt werden.

.. raw:: latex

    \newpage

.. _fig-demo-overview:

.. figure:: figs/demo_overview.*
    :alt: Übersicht über die Demoanwendung
    :width: 80% 
    :align: center
    
    Übersicht über die Demonanwendung.

.. -------------------------------

.. _fig-demo-database:

.. only:: html

   .. figure:: figs/demo_database.png
       :alt: Die Datenbank Ansicht
       :width: 100%
       :align: center

       Die Datenbank Ansicht --- Anzeige aller verfügbaren Songs mit folgenden
       Tags: Artist, Album, Title, Datum, Genre sowie dem Playcount.

.. only:: latex

   .. figure:: figs/demo_database270.png
       :alt: Die Datenbank Ansicht
       :width: 93%
       :align: center

       Die Datenbank Ansicht --- Anzeige aller verfügbaren Songs mit folgenden
       Tags: Artist, Album, Title, Datum, Genre sowie dem Playcount.

.. -------------------------------

.. _fig-demo-playlist:

.. only:: html

   .. figure:: figs/demo_playlist.png
       :alt: Die aktuelle Playlist
       :width: 100%
       :align: center

       Die aktuelle Playlist, bestehend aus den zuvor erstellten Empfehlungen.
       Der Seedsong ist durch einen roten Kreis gekennzeichnet.

.. only:: latex

   .. figure:: figs/demo_playlist270.png
       :alt: Die aktuelle Playlist
       :width: 93%
       :align: center

       Die aktuelle Playlist, bestehend aus den zuvor erstellten Empfehlungen.
       Der Seedsong ist durch einen roten Kreis gekennzeichnet.

.. -------------------------------

.. _fig-demo-rules:

.. only:: html

   .. figure:: figs/demo_rules.png
       :alt: Die Regelansicht
       :width: 100%
       :align: center

       Eine Auflistung der momentan bekannten Regeln. Angezeigt werden: Beide
       Mengen der Regel, der Supportcount und das Rating.

.. only:: latex

   .. figure:: figs/demo_rules270.png
       :alt: Die Regelansicht
       :width: 93%
       :align: center

       Eine Auflistung der momentan bekannten Regeln. Angezeigt werden: Beide
       Mengen der Regel, der Supportcount und das Rating.

.. -------------------------------

.. _fig-demo-graph:

.. only:: html

   .. figure:: figs/demo_graph.png
       :alt: Die Graphenansicht
       :width: 100%
       :align: center

       Der Graph der hinter den Empfehlungen steckt wird hier in 3500x3500px
       geplottet. Eine Interaktion ist nicht möglich.

.. only:: latex

   .. figure:: figs/demo_graph270.png
       :alt: Die Graphenansicht
       :width: 93%
       :align: center

       Der Graph der hinter den Empfehlungen steckt wird hier in 3500x3500px
       geplottet. Eine Interaktion ist nicht möglich.

.. -------------------------------

.. _fig-demo-history:

.. only:: html

   .. figure:: figs/demo_history.png
       :alt: Die Ansicht der History
       :width: 100%
       :align: center

       History--Ansicht: die zuletzt gehörten (links) und kürzlich empfohlenen
       (rechts) Songs werden aufgelistet.

.. only:: latex

   .. figure:: figs/demo_history270.png
       :alt: Die Ansicht der History
       :width: 93%
       :align: center

       History--Ansicht: die zuletzt gehörten (links) und kürzlich empfohlenen
       (rechts) Songs werden aufgelistet.

.. -------------------------------

.. _fig-demo-examine:

.. only:: html

   .. figure:: figs/demo_examine.png
       :alt: Die Ansicht der Examine--Page
       :width: 100%
       :align: center

       Die ,,Examine" Page --- Die Attribute des aktuellen Songs werden angezeigt.
       Zudem wird die ,,moodbar" --- falls vorhanden --- mittels cairo :cite:`CRO`
       gerendert.

.. only:: latex

   .. figure:: figs/demo_examine270.png
       :alt: Die Ansicht der Examine--Page
       :width: 93%
       :align: center

       Die ,,Examine" Page --- Die Attribute des aktuellen Songs werden angezeigt.
       Zudem wird die ,,moodbar" --- falls vorhanden --- mittels cairo :cite:`CRO`
       gerendert.
