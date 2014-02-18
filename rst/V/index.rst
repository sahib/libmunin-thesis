***********************
Demonstrationsanwendung
***********************

.. epigraph:: 

   *,,These plus Antithese gleich Hysterese''*

   -- *Einfach Göttlich, Terry Pratchett*

Intro
=====

:dropcaps:`Abseits` der Bibliothek wurde eine, auf dem freien
Oberflächen-Framework :math:`\text{GTK+}-\!3.0` basierende, GUI-Anwendung entwickelt.
Entsprechend :ref:`anf-demo` dient diese nicht nur zum *Showoff*, sondern auch
zur gezielten Fehlersuche.

Die Anwendung, die den ebenfalls nordischen Namen *Naglfar* erhielt, stellt
einen MPD-Client bereit. Im Hintergrund werkelt dabei *Moosecat*.

Vor der ersten Benutzung muss gemäß :num:`fig-startup` eine Session aufgebaut
werden - dies erledigt das Skript ``coldstart.py`` (siehe
:ref:`coldstart-example`) - dies kann durch das Ziehen der Songtexte und der
Audioanalyse beim ersten Lauf sehr lange dauern - bis zu 2 Stunden. Danach sind
allerdings die Songtext zwischengelagert und der zweite Lauf dauert dann nur
noch wenige Minuten. 

Nach dem ``coldstart.py`` die *Session* auf die Platte geschrieben hat, kann die
eigentliche Anwendung gestartet werden. Diese verbindet sich zuallererst mit
einem MPD-Server der auf *localhost:6601* lauscht und besorgt sich dort alle
Metadaten um die *Playlist* und *Database*-Ansicht zu befüllen. Danach wird
besagte *Session* geladen. Nach der Initialisierung der *GUI* ist die Anwendung
nun bereit benutzt zu werden.

Damit zwischen den von *libmunin* herausgegebenen Empfehlungen und den internen
Songs unterschieden werden kann, speichert ``coldstart.py`` ein Mapping ab
zwischen den ID von *libmunin's* Songs zu den Dateipfaden innerhalb der
Musikdatenbank. 

Anwendungsübersicht
===================

.. _fig-demo-overview:

.. figure:: figs/demo_overview.*
    :alt: Übersicht über die Demoanwendung
    :width: 100% 
    :align: center
    
    Übersicht über die Demonanwendung.

In :num:`fig-demo-overview` wird eine Übersicht über die GUI der Anwendung
gegeben. Detailliertere Ansichten werden am Ende des Kapitels gezeigt.

Im Folgenden wird nun eine Übersicht über die *Features* der Anwendung gegeben.

1) Ansichten
------------

*Database* 
~~~~~~~~~~

Siehe Abbildung :num:`fig-demo-database`.
   
Anzeige der gesamten Musikdatenbank durch die Spalten ``Artist``, ``Album``,
``Titel``, ``Datum`` und ``Genre``. Jede Zeile entspricht dabei einem Song. 

Ein Rechtsklickmenü auf einen beliebigen Song fördert ein Kontextmenü zu Tage
(siehe Abbildung :num:`fig-demo-context-menu`), dass mehrere Möglichkeiten bietet 
um die Playlist mit Empfehlungen zu befüllen (TODO referenz).
Im folgenden ist :math:`\lambda` die Anzahl der gewünschten Empfehlungen die im
Empfehlungszähler (siehe :ref:`empfehlungs-zaehler`) eingestellt ist.


Ausgewählter Song als :term:`Seedsong`:
"""""""""""""""""""""""""""""""""""""""

Erstellt :math:`\lambda` Empfehlungen basierend auf dem selektierten Song
und reiht sie in die Playlist ein. 

Playlist säubern und ausgewählter Song als :term:`Seedsong`:
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Wie oben, leert aber vor dem Einreihen die Playlist.

.. _attribute-search:

Suche einen :term:`Seedsong` mit einem bestimmten Attribut:
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Sucht einen :term:`Seedsong` nach bestimmten Kriterien, die der Nutzer im
Eingabefeld oben rechts angeben kann. Dort kann ein *Suchbegriff* in der
folgenden Form angegeben werden::

    <attribut>: <wert>[, <attribut>: <value>, ...]

Folgendes Beispiel findet alle Songs mit dem Artist *,,Billy Talent''* **und**
dem Genre *,,Rock''* ::

    genre: rock, artist: Billy Talent

Werden mehrere Suchergebnisse gefunden so werden alle als Seedsongs genutzt um
in die Playlist :math:`\lambda` neue Songs einzureihen.

Diese Funktionalität ist momentan relativ eingeschränkt da nur exakte Treffer
funktioneren. Ist das *Genre* also als *,,rock / pop''* getaggt, so wird die
Sucher erfolglos verlaufen.

Lasse *libmunin* einen :term:`Seedsong` auswählen:
""""""""""""""""""""""""""""""""""""""""""""""""""

*libmunin* wählt automatisch einen :term:`Seedsong` nach folgenden Kriterien:

* Nutze die Seedsongs, die in der am besten bewertesten Regel vorkommen.
* Falls keine Regel vorhanden, nutze den meist abgespielten :term:`Song` als
  :term:`Seedsong`.
* Schlägt auch das fehl wird ein zufälliger :term:`Song` ausgewählt.

In allen Fällen werden dann :math:`\lambda` Empfehlungen in die Playlist
eingereiht.

Erstelle eine komplett zufällige Playlist:
""""""""""""""""""""""""""""""""""""""""""

Reiht :math:`\lambda` neue, komplett zufällig aus der Datenbank gewählte, Songs in
die Playlist ein.

Nützlich um die komplett zufällige Playlist mit einer von *libmunin* erstellten
Playlist zu vergleichen. Der Seed für die ``random()``-Funktion ist dabei immer
gleich, daher erstellt dies nach einem Neustart stets dieselbe Liste.

.. _fig-demo-context-menu:

.. figure:: figs/demo_context_menu.png
    :alt: Das Kontextmenu in der Playlist und Database Ansicht
    :width: 30%
    :align: center

    Die Einträge des Kontextmenüs in der Playlist und Database Ansicht 

.. _playlist-view:

*Playlist* 
~~~~~~~~~~

Siehe Abbildung :num:`fig-demo-playlist`.

Wie die *Database-Ansicht*, zeigt aber lediglich die Songs an die empfohlen
wurden. Sonst ist diese Ansicht funktionsidentisch mit der *Database-Ansicht*.

*Graph* 
~~~~~~~

Siehe Abbildung :num:`fig-demo-graph`.

Im *Graphen-Ansicht* kann ein Plot von *libmunin's* Graphen begutachtet
werden. Dies ist oft nützlich um nachvollziehen welche Empfehlungen warum
gegeben wurden.

*Rules* 
~~~~~~~

Siehe Abbildung :num:`fig-demo-rules`.

In einer Liste werden alle bekannten :term:`Assoziationsregel`
angezeigt. Dabei wird neben beiden Seiten der Regel auch der Supportcount
und das Rating der Regel angezeigt.

*Examine*
~~~~~~~~~

Siehe Abbildung :num:`fig-demo-examine`.

Hier werden alle Attribute des momentan spielenden Songs angezeigt. 
Es wird die von *libmunin* normalisierte Form angezeigt, also auch, falls
verfügbar, der Originalwert.

Zudem wird die ``moodbar`` (falls vorhanden) oben im Fenster geplottet.

*History* 
~~~~~~~~~~

Siehe Abbildung :num:`fig-demo-history`.

Neben einer chronologischen Auflistung aller Songs die in letzter Zeit
gehört wurden (Begrenzung auf 1000 Stück) werden hier auch die zuletzt 
ausgestellten Empfehlungen (Begrenzung auf 10 Stück) angezeigt.

Letzteres ist für das Debugging der Filterfunktion nützlich.

(2) Seedsong
-------------

Zeigt mit einem roten Kreis den zuletzt ausgewählten :term:`Seedsong` an.
Falls es mehrere Seedsongs gab, wird nur der erste markiert.

(3) Current Song
----------------

Ein dreieckiges Icon das den aktuell spielenden (oder pausierten) Song anzeigt.

(4) Playlist
------------

Die Playlistview. Siehe :ref:`playlist-view`.

.. _empfehlungs-zaehler:

(5) Empfehlungszähler
---------------------

Die Anzahl an Empfehlungen die ein Klick im Kontextmenü liefert.

(6) Filter
----------

Togglebutton (,,durchgestrichenes *a* als Icon'') der anzeigt ob der Filtermodus
aktiviert ist.  Ist er aktiv so darf sich in einer dynamisch erstellten Playlist
der Artist nur alle 3 Stücke wiederholen, der selbe Artist *und* das selbe Album
nur alle 5 Stücke.

(7) Mininmaler Höranteil
------------------------

Ein Klick auf den Button fördert einen Slider zu Tage auf dem man eine
Prozentzahl einstellt. Diese legt fest welcher Anteil eines Liedes (in Prozent)
*mindestens* angehört werden muss damit er zur Historie hinzugefügt wird.

Um diese Funktionalität zu realisieren musste *Moosecat* um diese Funktion
erweitert werden.

(8) Attributsuche
-----------------

Eingabe einer Folge von Attribut-Werte Paaren die ein :term:`Seedsong` 
bei der Attributsuche (:ref:`attribute-search`) haben sollte.

(9) Rating
----------

Spezielles Widget auf den man das *Rating* des aktuell spielenden Songs zu
setzen. Beim erstellen der *Session* durch ``analyse.py`` wird ein *Rating* von
:math:`0` angenommen - also *ungesetzt*.

Zum Setzen klickt man einfach ins Feld, die Seite links vom Cursor wird dann
eingefärbt.  Es ist möglich etwas links vom ersten Stern zu klicken um das
Rating auf ,,0'' (und damit *ungesetzt*) zurückzusetzen.

Ein Ändern des Ratings hat ein Neuzeichnen des Graphen zufolge.

(10) Playcount
--------------

Zeigt an wie oft ein Lied bereits gehört wurde. Ein Lied gilt als nicht gehört
wenn prozentuell nur ein kleiner Teil als der gesetzte minimale Höranteil
angehört wurde.

Zur optischen Vorhebung ist es mit einer Fortschrittsanzeige hinterlegt - sobald
man 100x mal ein Lied hört, zeigt diese vollen Füllstand an.

(11) Volumebar
--------------

Regler für die Lautstärke. 

(12) Title Label
----------------

Zeit das aktuell spielende Lied mit Titel, Album und Artist an.

(13) Modebuttons
----------------

Umschalten zwischen *Random* (nächstes Lied ist zufällig), *Single* (höre nach
diesem Lied auf zu spielen), *Repeat* (spring zum Anfang der Playlist nach dem
letzten Lied) und *Consume* (Lösche das Lied aus der Playlist nach dem
Abspielen).

(14) Seekbar
------------

Ermöglicht das wahlfreie Hin- und Herspringen innerhalb des aktuellen Liedes.
Übersprunge Parts eines Liedes fließen nicht die *Höranteil* ein, 
doppelt gehörte Parts schon - daher sind Werte :math:`\ge 100\%` möglich.

(15) Playbuttons
----------------

Die ,,üblichen'' Kontrollen eines Musicplayers zum Pausieren/Abspielen (an
momentaner Stelle anhalten/weiterspielen), Stoppen (Anhalt und zum Anfang der
Playlist springen), Nächstes und vorheriges Lied .


(16) Suche
----------

Erlaubt das Filtern der Playlist oder Datenbank.

Suchbegriffe können einfacher Natur wie *,,beat''* (Findet alles das *,,beat''*
im Artist, Album oder Titel beeinhaltet) bis hin zu sehr komplizierten
Suchbegriffen wie *,,(genre:rock + y:2001..2003) | artist:Beat*'' (Findet
alles das *,,rock''* im Genre hat und in den Jahren *2001* bis einschließlich 
*2003* released wurde, oder dessen Artist ein Wort enthält, dass mit ,,Beat''
beginnt).
 
*Anmerkung:* Die ,,Such-Engine'' dahinter ist in *Moosecat* implementiert.

Die Suche kann mit :kbd:`Strg-f` oder :kbd:`/` aktiviert und mit :kbd:`Esc`
wieder versteckt werden.

.. _fig-demo-database:

.. figure:: figs/demo_database.png
    :alt: Die Datenbank Ansicht
    :width: 100%
    :align: center

    Die Datenbank Ansicht - Anzeige aller Songs.

.. _fig-demo-playlist:

.. figure:: figs/demo_playlist.png
    :alt: Die aktuelle Playlist
    :width: 100%
    :align: center

    Die aktuelle Playlist, bestehend aus den Empfehlungen.

.. _fig-demo-rules:

.. figure:: figs/demo_rules.png
    :alt: Die Regelansicht
    :width: 100%
    :align: center

    Die momentan bekannten Regeln

.. _fig-demo-graph:

.. figure:: figs/demo_graph.png
    :alt: Die Graphenansicht
    :width: 100%
    :align: center

    Der Graph der hinter den Empfehlungen steckt wird hier geplottet.

.. _fig-demo-history:

.. figure:: figs/demo_history.png
    :alt: Die Ansicht der History
    :width: 100%
    :align: center

    History-Ansicht, die zuletzt gehörten und empfohlenen Songs.

.. _fig-demo-examine:

.. figure:: figs/demo_examine.png
    :alt: Die Ansicht der Examine-Page
    :width: 100%
    :align: center

    Die ,,Examine'' Page - Die Attribute des aktuellen Songs werden angezeigt.
