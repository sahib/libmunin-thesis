******
Design
******

Algorithmik
===========

:dropcaps:`Im` folgenden wird ein Überblick über die Algorithmik, und die dazugehörigen
Datenstrukturen, gegeben die im Kern von *libmunin* steckt. Eine genauere
Beschreibung wird in der Bachelorarbeit erfolgen - dieser Überblick soll
hauptsächlich dazu dienen einen Einblick in die verwendeten Techniken zu geben.

Grundüberlegungen
-----------------

Die *Ähnlichkeit* von je einem Song *A* und *B* lässt sich durch eine
Distanz definieren.

Um die Distanzen zu speichern wird bei vielen Datamining--Projekten eine
Distanzmatrix genutzt --- also eine quadratische Dreiecksmatrix, in der
die Distanzen von jedem Dokument zu jedem anderen gespeichert werden.

Da das System auch für eine sehr hohe Anzahl von Songs funktionieren soll,
schließt sich die Benutzung einer Distanzmatrix allerdings von alleine aus.
Nehmen wir an ein Benutzer möchte seine Musiksammlung mit :math:`40.000` Liedern
importieren, so bräuchten wir soviele Felder in der Matrix:

.. math:: 

    \frac{(40.000^2 - 40.0000)}{2} = 799.980.000

Nimmt man für jedes Feld einen günstig geschätzten Speicherverbrauch von
:math:`4` Byte an, so bräuchte man allein für die Distanzmatrix hier aufgerundet
3 Gigabyte Hauptspeicher --- was selbst für diesen günstig geschätzten Fall
unakzeptabel wäre. Auch eine Sparsematrix (vgl. :cite:`stoer2002introduction`)
wäre hier kaum sinnvoll, da in allen Fällen ja trotzdem etwas weniger als die
Hälfte aller Felder befüllt ist.

Man muss also versuchen, nur eine bestimmte Anzahl von Distanzen für einen Song
zu speichern --- vorzugsweise eine Menge von Songs mit der kleinsten
Distanz. Als geeignete Datenstruktur erscheint hier ein Graph --- die
Knoten desselben sind die Songs und die Kanten dazwischen die Distanzen.

Zur besseren optischen Vorstellung, ist unter :num:`fig-graph-example` ein
Graphen--Plot (erstellt mit ``igraph`` :cite:`IGR`) gezeigt.

.. _fig-graph-example:

.. figure:: figs/graph_example.png
    :alt: Beispielgraph aus generierten Testdaten
    :width: 85%
    :align: center

    Beispielgraph mit 100 Knoten, aus generierten Testdaten. Die Farbe der
    Knoten zeigt grob die ,,Zentralität" des Knoten an. Pro Knoten wurde
    ein Integer zwischen 1-100 willkürlich generiert, diese wurden mit einer
    primitiven Distanzfunktion verglichen. Die Länge der Kanten ist durch das
    Layout bedingt und deutet nicht auf die Distanz hin.


Jedem Attribut eines Songs ist ein Wert zugeordnet. Um eine sinnvolle
Distanzfunktion zu definieren, die zwei Songs miteinander vergleicht, muss man
für jedes spezielle Attribut eine eigene Unter--Distanzfunktion definieren. 
Beispielsweise muss für das Genre eine andere Distanzfunktion definiert sein als
für den Liedtext. 

Um aus den Unter--Distanzfunktion eine gemeinsame Distanz zu erhalten werden die
einzelnen Ergebnisse, durch einen gewichteten Mittelwert in eine einzelne
Distanz zusammenschmolzen.

Graphenoperationen
------------------

Um mit unseren Graphen arbeiten zu können, müssen wir einige Operationen auf ihm
definieren:

* ``rebuild:`` Bevor der Graph benutzt werden kann, muss er natürlich erstmal aufgebaut werden. 
  Der naive Ansatz wäre dabei für jeden Song die Distanzen zu jedem anderen Song
  zu berechnen --- dies hätte einen Aufwand von :math:`O(n^2)` zur Folge. Dies ist
  aus oben genannten Gründen ebenfalls kaum wünschenswert.
  
  Deshalb kann die ``rebuild`` Operation keinen *perfekten*  Graph erzeugen, sondern
  muss für hinreichend große Datenmengen auf eine Approximation zurückgreifen.
  *Perfekt* meint hierbei einen Graphen bei dem jeder Knoten wirklich mit den
  absolut besten Nachbarn verbunden ist.

  Nach dem Aufbau sollte ein ungerichteter Graph dabei herauskommen, in dem
  idealerweise jeder Knoten vom jedem anderen Knoten erreichbar ist --- es sollten
  also keine *Inseln* dabei entstehen. Es gibt keine maximale Anzahl von Nachbarn,
  die ein Song haben darf --- lediglich einen *Richtwert*.

* ``rebuild_stupid:`` Wie ``rebuild``, nutzt aber quadratischen Aufwand, indem es
  jeden Song mit jedem anderen vergleicht. Dies ist für kleine Mengen (:math:`\le
  400`) von Songs verträglich und für *sehr* kleine Mengen sogar schneller ---
  tatsächlich fällt die normale ``rebuild``-Operation tatsächlich auf diese
  zurück, falls die Menge an Songs :math:`\le 200`.
  
  Hauptsächlich für Debugging--Zwecke, um Fehler beim herkömmlichen ``rebuild``
  aufzudecken. 

* ``add:`` Füge einen einzelnen Song zu dem Graphen hinzu, verbinde ihn aber
  noch nicht.  Dies ist die bevorzugte Operation um viele Songs dem Graphen
  hinzuzufügen - beispielsweise beim *Kaltstart* --- da das Verbinden später in
  einem ``rebuild``-Schritt erledigt werden kann.

* ``insert:`` Füge einen einzelnen Song zu dem Graphen hinzu und verbinde ihn.
  Suche dazu erst eine passende Stelle in der er eingepasst wird.

* ``remove:`` Entferne einen einzelnen Song aus dem Graphen und versuche das
  entstandene *Loch* zu flicken, indem die Nachbarn des entfernten Songs
  untereinander verkuppelt werden.

* ``modify:`` Manchmal ist es nötig das Attribut eines einzelnen Songs --- wie
  beispielsweise das stark vom Benutzer abhängige **Rating** --- zu ändern. Dabei
  wird der Song erst mittels ``remove`` entfernt, die Attribute werden angepasst
  und er wird mittels ``insert`` wieder eingefügt. 

* ``fixing:`` Durch das Löschen und Hinzufügen von Songs können *Einbahnstraßen*
  im Graphen entstehen. Durch dem nach gelagerten *fixing*--Schritt werden diese,
  nach bestimmten Regeln, entweder entfernt oder in bidirektionale Verbindungen
  umgebaut.

.. _recom-out:

Ausstellen von Empfehlungen
---------------------------

Das Ausstellen von Empfehlungen wird durch das Traversieren des Graphen
mittels einer Breitensuche (TODO) erledigt. Dabei wird der Ursprung durch ein
sogenannten Seedsong bestimmt. Anschaulich wäre der Seedsong bei einer
Anfrage wie ,,10 ähnliche Songs zu *The Beatles --- Yellow Submarine* " eben
*,,Yellow Submarine"*.

Aus der funktionalen Programmierung wurde dabei das Konzept der *Infinite
Iterators* übernommen: Anstatt eine bestimmte Anzahl von Empfehlungen als Liste
wird ein Versprechen herausgegeben, die Empfehlungen genau dann zu berechnen,
wenn sie gebraucht werden (*Lazy Evaluation*). Dadurch ist auch die Zahl der zu
gebenden Empfehlungen variabel --- was sehr nützlich beim Erstellen einer
dynamischen Playlist ist.

Es können auch mehrere Seedsongs verwendet werden --- dann werden die einzelnen
*Iteratoren* im Reißschlußverfahren verwebt.

Basierend auf dieser Idee ist es möglich, bestimmte Strategien zu implementieren,
die beispielsweise Songs mit dem höchsten Abspielanzahl (*Playcount*), dem
besten Rating oder einen bestimmten Attribut wie *genre=rock* als Seedsongs
auswählt.

.. _recom-filter:

Filtern von Empfehlungen
------------------------

Oft ist es nötig, die gegebenen Empfehlungen noch zusätzlich zu filtern. Das hat
den simplen Grund, dass im Graphen die meisten Alben einzelne *Cluster* bilden -
die Lieder auf einem Album sind meist unter sich sehr ähnlich. Da man aber
vermeiden möchte, dass zu einem Seedsong ein Lied vom selben Album oder
gar selben Künstler empfohlen wird, müssen diese beim Iterieren über den Graphen
ausgesiebt werden.

Dazu werden die zuletzt gegebenen Empfehlungen betrachtet --- ist in
den letzten 5 Empfehlungen der gleiche Künstler bereits vorhanden so wird die
Empfehlung ausgesiebt. 

Lernen durch die Historie
-------------------------

Wie bereits erwähnt, soll *libmunin* Mechanismen bieten um sowohl
*explizit* als auch *implizit* vom Nutzer zu lernen.  Das *implizite* Lernen 
erfolgt dabei durch Assoziationsregeln, die aus der Aufzeichnung des Gehörten
abgeleitet werden.

--- Defintion Assoziationsregel? ---

Nur eine bestimmte Anzahl von Regeln wird gespeichert --- zuviele Regeln würden
*historische Altlasten* immer weiter mitschleppen und der aktuelle Geschmack des
Benutzers würde nicht widergespiegelt werden. Beispielsweise kann man hier einem
Hörer nennen der *libmunin* zwei Jahre lang nutzt und anfangs viel elektronische
*Ambient-Musik* hört, in letzter Zeit aber auf *Klassik* umgesattelt hat. Nach
einiger Zeit sollten also keine Empfehlungen zu elektronischer Musik mehr
kommen.

Integration von *libmunin* in die Umwelt
========================================

Allgemeiner Ablauf
------------------

Eine gut definierte Datenstruktur nützt nichts wenn man nicht weiß wie die
Daten, die aus der *Umwelt* hereinkommen aussehen. Diese müssen schließlich
erstmal in die Form eines Graphen gebracht werden bevor man Empfehlungen
aussprechen kann. Dieser *Prozess* (siehe Abbildung :num:`fig-startup`)
beinhaltet vier Schritte:

* **Kaltstart:** Im Kaltstart müssen mittels *Information Retrieval* Techniken
  fehlende Daten, wie beispielsweise die Songtexte oder die die Audiodaten, aus
  lokalen oder entfernten Quellen besorgt werden. Dies ist Aufgabe des Nutzers -
  *libmunin* bietet hier nur Hilfsfunktionen an.
  Der *Kaltstart* ist nur bei der ersten Benutzung einer Musikdatenbank nötig.
* **Analyse:** Bei der *Analyse* werden die nun vorhandenen Daten untersucht und
  durch sogenannte Provider normalisiert. Die Normalisierung ist nötig,
  um im nächsten Schritt eine einfache und effiziente Vergleichbarkeit der Daten
  zu gewährleisten. 
* **Rebuild:** Dies entspricht der ``rebuild``-Operation.
  In diesem Schritt werden die normalisierten Daten untereinander mittels einer
  passenden Distanzfunktion untersucht. Unter Zuhilfenahme, der dabei
  entstehenden Distanz wird der Graph aufgebaut. 
* **Einsatz:** Durch Traversierung des Graphen können jetzt Ergebnisse abgeleitet 
  werden.

.. _fig-startup:

.. figure:: figs/munin_startup.*
    :alt: Allgemeine Benutzung
    :width: 75%
    :align: center

    Allgemeine Benutzungs--Prozess von libmunin, in 4 Stufen aufgeteilt.

.. _environement:

Die Umgebung
------------

In Abbildung :num:`fig-integration` ist eine Übersicht gegeben in welcher
Umgebung *libmunin* eingesetzt wird. Eine Frage die sich dabei stellt ist: *Wie*
stellen die Nutzer der Bibliothek ihre Musikdatenbank bereit? Und *wie* geben
sie diese in das System ein? 

Dazu bedarf es einer weiteren Eingabe vom Nutzer: Einer Beschreibung wie seine
Musikdatenbank aufgebaut ist, welche *Tags* sie enthält und wie mit diesen Daten
verfahren werden soll. 

Da diese Daten sehr unterschiedlich aufgebaut sind, muss *libmunin* sehr
generisch aufgebaut sein. Der Ansatz ist dabei, zusätzlich vom Nutzer eine
Maske zu verlangen die beschreibt welche möglichen *Tags* (oder
Attribut) ein einzelner Song besitzt Für jedes Attribut kann
dann, nach Baukastenprinzip, ein Provider, eine Distanzfunktion
und eine Gewichtung ausgewählt werden. Letzere beschreibt, wie *wichtig* diese
Attribut aus Sicht des Nutzers in Bezug auf die Ähnlichkeit ist. Der
Provider normalisiert die Werte von einem Attribut auf bestimmte
Art und Weise, während die Distanzfunktion sich um das Vergleichen der
normalisierten Werte nach bestimmten, je auf Art des Attributs spezialisierten
Weise, kümmert.

Nachdem das Format, in Form der Maske, geklärt ist, kann der Nutzer
jeden Song mittels der ``add``-Operation hinzufügen und im Anschluss eine
``rebuild``-Operation triggern.

.. _fig-integration:

.. figure:: figs/integration.*
    :alt: Integrationsübersicht
    :width: 100%
    :align: center

    Integration von libmunin in seine Umwelt. Die Grafik ist in 3
    unterschiedliche, durch Striche getrennte, Bereiche aufgeteilt: Unten
    der Nutzerbereich (Entwickler oder Endanwender die libmunin nutzen), in der
    Mitte die Entwickler von libmunin und oben die externen Ressourcen auf die
    libmunin zugreift.

Wir wissen nun wie unsere interne Datenstruktur auszusehen hat. Wir wissen auch
wie die Daten aussehen die von der Umwelt hereinkommen. Der nächste Schritt
darin, sich Gedanken über den *Layer* zu machen welcher zwischen beiden
vermittelt.

Tatsächlich besteht ein großer Teil von *libmunin* aus diesem *Layer*, der Daten
aus der Umwelt nimmt und in die interne Graphendarstellung transferiert.

In Abbildung :num:`fig-arch` findet sich eine Darstellung von *libmunin* als
,,Whitebox" --- sprich, als Box mit allen Ein- und Ausgängen, sowie der groben
Verarbeitung dazwischen. Dies ist als Zusammenfassung des oben Gesagten zu
werten.

.. _fig-arch:

.. figure:: figs/arch.*
    :alt: Architekturübersicht.
    :width: 100%
    :align: center

    Betrachtung von libmunin als ,,Whitebox'' --- Alle Eingaben (links) und
    Ausgaben (rechts) in einem Bild. In der Box selbst ist die grobe
    Verarbeitung der Daten skizziert.

Entwurf der Software
====================

Da wir jetzt grob wissen aus welchen Komponenten unsere Software besteht, können
wir uns Gedanken darüber machen wie diese einzelnen Teile konkret aussehen.  Im
folgenden werden die *,,Hauptakteure"* der Software vorgestellt:

Übersicht
---------

Unter :num:`fig-class-overview` findet sich eine grobe Übersicht der wichtigsten
Klassen. *Libmunin's* Entwurf basiert --- dort wo es Sinn macht --- auf
Prinzipien der Objektorientierten Programmierung. Einige Teile der
Funktionalität, wie die Graphentraversierung, sind prozedural
implementiert. 

.. _fig-class-overview:

.. figure:: figs/class.*
    :alt: Klassenübersicht
    :width: 100%
    :align: center

    Jeder Node ist eine Klasse in den jeweiligen Teilbereichen der Software.
    Provider und DistanceFunction Unterklassen nur beispielhaft gezeigt.

Grobe Unterteilung
------------------

Wir schauen uns zuerst die einzelnen *Regionen* der Software an, danach
widmen wir uns den einzelnen Komponenten.

Grob ist die Software in fünf unterschiedliche *Regionen* aufgeteilt.
Im Folgenden werden diese Regionen vorgestellt. 

1. **API:** Die API ist die Schnittstelle zum Benutzer hin. Der Nutzer kann
   mittels einer ``Session`` auf alle Funktionen von *libmunin* zugreifen. Dazu
   muss er beim Instanzieren derselben eine ``Maske`` angeben die die
   Musikdatenbank beschreibt.  Alternativ kann die ``EasySession`` genutzt
   werden, die eine vordefinierte ``Maske`` bereitstellt, die für viele
   Anwendungsfälle ausreichend ist.

2. **Provider Pool:** Implementiert eine große Menge vordefinierter Menge von
   Providern, die die gängigsten Eingabedaten (wie Künstler, Album, Lyrics,
   Genre, ...) abdecken.  Manche ``Provider`` dienen auch zum *Information
   Retrieval* und ziehen beispielsweise Songtexte aus dem Internet.  Eine volle
   Liste von verfügbaren Providern wird unter :ref:`provider-list` gegeben. 

   In der Übersicht :num:`fig-class-overview` wurde aus Gründen der
   Übersichtlichkeit exemplarisch nur drei Provider gezeigt.

3. **DistanceFunction Pool:** Implementiert eine Menge vordefinierter
   Distanzfunktionen, welche die Werte der obigen ``Provider`` vergleichen.
   Dabei kommen zwar viele Provider und Distanzfunktion als Paare daher (wie
   beispielsweise der ``GenreTree`` Provider und die ``GenreTree``
   Distanzfunktion), was aber keine Notwendigkeit darstellt - verschiedene
   Provider können beispielsweise dieselbe Distanzfunktion nutzen.

   Eine volle Liste von verfügbaren Distanzfunktionen wird unter
   :ref:`distance-function-list` gegeben. 
   
   In der Übersicht :num:`fig-class-overview` wurde aus Gründen der
   Übersichtlichkeit exemplarisch nur drei Distanzfunktionen gezeigt.
   
   Nutzer der Bibliothek können eigene ``Provider`` oder ``DistanceFunctions``
   implementieren, indem sie von den jeweiligen Oberklassen ableiten.

4. **Songverwaltung:** Hier geschieht alles was mit dem Speichern und
   Vergleichen einzelner Songs zu tun hat. Dies umfasst das Speichern der
   ``Songs`` in der ``Database`` sowie das Verwalten der
   Nachbarschafts--``Songs`` für jeden ``Song`` mit den dazugehörigen
   ``Distance``.

   Der oben erwähnte Graph entsteht durch die Verknüpfungen der Songs untereinander
   und bildet keine eigenständige Klasse.

5. **Regeln und History:** Dieser Teil von *libmunin* ist für das Aufzeichnen
   des Benutzerverhaltens und dem Ableiten von Assoziationsregeln daraus
   zuständig.

Einzelne Komponenten
--------------------

Da UML-Diagramme sich oft in unwichtige Details und akribische
Methodenauflistungen versteigen, wird im folgenden textuell eine Auflistung
aller Klassen und ihrer Aufgabe gegeben. Nur in Einzelfällen werden
Methodennamen gekennzeichnet.

**Session:** Die Session ist das zentrale Objekt für den Nutzer der
Bibliothek.  Es bietet über Proxymethoden Zugriff auf alle Funktionalitäten
von *libmunin* und kann zudem persistent abgespeichert werden. Dies wird durch
das Python--Modul ``pickle`` realisiert --- es speichert rekursiv alle Member
einer ``Session``-Instanz in einem Python-spezifischen Binärformat ---
Voraussetzung hierfür ist, dass alle Objekte direkt oder indirekt an die
``Session``-Instanz gebunden sind. 

Der Speicherort entspricht dem *XDG Standard* :cite:`XDG`, daher wird jede Session
als ``gzip`` gepackt unter ``$HOME/.cache/libmunin/<name>.gz`` gespeichert.  Der
``<name>`` lässt sich der Session beim Instanzieren übergeben.

Die weitere Hauptzuständigkeit einer ``Session`` ist die Implementierung der
Recommendation--Strategien, die den Graphen traversieren.

**Mask:** Ein Hashtable--ähnliches Objekt, das die Namen der einzelnen
Attribut festlegt. Da dies bereits in :ref:`environement` erklärt wurde,
wird hier nochmal ein kurzes praktisches Beispiel gezeigt:

.. code-block:: python

   m = Mask({                              # Mask erwartet als Übergabe ein Dictionary
        'genre': pairup(                   # Verknüpfe Distanzfunktion mit Provider 
            GenreTreeProvider(),           # Instanziere einen Provider
            GenreTreeAvgLinkDistance(),    # Instanziere eine Distanzfunktion
            4                              # Gewichtung des Attributes (beliebiger Wert)
        ),  # [...] Weitere Attribute  
   })
   session = Session(m)                    # Instanziere eine Session mit dieser Maske

Wie man sieht wird als ,,Key" der Name des Attributes festgelegt, und als
,,Value" ein Tupel aus einer ``Provider``-Instanz, aus einer
``DistanceFunction``-Instanz und der Gewichtung dieses Attributes als ``float``.

Wird statt einer ``Provider`` oder ein ``DistanceFunction`` Instanz etwas
anderes übergeben, so wird ein ``DefaultProvider`` (reicht die Werte unverändert
weiter), bzw. eine ``DefaultDistanceFunction`` (vergleicht Werte mit dem
``==``-Operator).

Der Nutzer hat meist selber wenig mit der ``Mask``-Instanz zu tun. Er übergibt
der ``Session`` eine Hashtable die implizit eine ``Mask``-Instanz erzeugt. 

**EasySession:** Wie die normale ``Session``, bietet aber eine bereits
fertigkonfigurierte Maske an, die für viele Anwendungsfälle ausreicht.
In Tabelle :num:`fig-easy-session` ist eine Auflistung, gegeben wie diese im
Detail konfiguriert ist.

.. _fig-easy-session:

.. figtable::
    :caption: Default--Konfiguration der ,,EasySession''.
    :alt: Default--Konfiguration der ,,EasySession''
    :spec: @{}l | l | l | l | l | c

    +--------------+----------------------+------------------+------------------------------+-----------------+--------------------+
    |  Attribut    |  Provider            |  Distanzfunktion | Eingabe                      |  Weight         |  Kompression?      |
    +==============+======================+==================+==============================+=================+====================+
    | ``artist``   | ``ArtistNormalize``  | Default          | Künstler                     | :math:`1\times` | :math:`\checkmark` |
    +--------------+----------------------+------------------+------------------------------+-----------------+--------------------+
    | ``album``    | ``AlbumNormalize``   | Default          | Albumtitel                   | :math:`1\times` | :math:`\checkmark` |
    +--------------+----------------------+------------------+------------------------------+-----------------+--------------------+
    | ``title``    | ``TitleNormalize``   | Default          | Tracktitel                   | :math:`2\times` |                    |
    +--------------+----------------------+------------------+------------------------------+-----------------+--------------------+
    | ``date``     | ``Date``             | ``Date``         | Datums--String               | :math:`4\times` |                    |
    +--------------+----------------------+------------------+------------------------------+-----------------+--------------------+
    | ``bpm``      |  ``BPMCached``       | ``BPM``          | Audiofile--Pfad              | :math:`6\times` |                    |
    +--------------+----------------------+------------------+------------------------------+-----------------+--------------------+
    | ``lyrics``   | ``Keywords``         | ``Keywords``     | Songtext                     | :math:`6\times` |                    |
    +--------------+----------------------+------------------+------------------------------+-----------------+--------------------+
    | ``rating``   | Default              | ``Rating``       | Integer (:math:`\in [0, 5]`) | :math:`4\times` |                    |
    +--------------+----------------------+------------------+------------------------------+-----------------+--------------------+
    |  ``genre``   |  ``GenreTree``       | ``GenreTreeAvg`` | Genre--String                | :math:`8\times` |                    |
    +--------------+----------------------+------------------+------------------------------+-----------------+--------------------+
    |  ``moodbar`` | ``MoodbarAudioFile`` | ``Moodbar``      | Audiofile--Pfad              | :math:`9\times` |                    |
    +--------------+----------------------+------------------+------------------------------+-----------------+--------------------+


**Song:** Speichert fur jedes Attribut einen Wert, oder einen leeren
Wert falls das Attribut nicht gesetzt wurde. Dies ähnelt einer
Hashtable, allerdings werden nur die Werte gespeichert, die ,,Keys" der
Hashtable werden in der ``Maske`` gespeichert und werden nur referenziert. Der
Grund dieser Optimierung liegt in verminderten Speicherverbrauch. 

Eine weitere Kompetenz dieser Klasse ist das Verwalten der Distanzen zu seinen
Nachbarsongs. Er muss Methoden bieten um eine Distanz zu einem Nachbarn
hinzuzufügen oder zu entfernen, Methoden um über alle Nachbarn zu iterieren oder
die Distanz zu einen bestimmten Nachbarn abzufragen 
und eine ``disconnect()`` Methode um den ``Song`` zu entfernt ohne dabei ein
,,Loch" zu hinterlassen.

Tatsächlich gibt es keine eigene ``Graph``--Klasse --- der Graph an sich
wird durch die Verknüpfung der einzelnen Songs in der ``Database`` gebildet --- 
jede ``Song`` Instanz bildet dabei einen Knoten.

Da eine Veränderung von Attributen im Song auch eine Veränderung im Graphen zur
Folge haben kann sind Instanzen der ``Song``--Klasse *Immutable*, sprich nach
ihrer Erstellung kann ihr Inhalt nicht mehr verändern werden. Ist dies trotzdem
vonnöten, kann die ``modify``-Operation eingesetzt werden. Ein praktischer
Einsatzgrund wäre beispielsweise das Ändern  des *Ratings* eines Songs. Es
sollte allerdings erwähnt werden, dass die ``modify`` Operation relativ
aufwendig ist --- schließlich muss der Song entfernt und neu eingefügt werden.

**Distance:** Wie die ``Song``--Klasse, speichert aber statt den Werten von
bestimmten Attributen die Distanz zwischen zwei Attributen. Zusätzlich
wird die gewichtete Gesamtdistanz gespeichert.  Beispielhaft ist das in
:num:`fig-distance-table` dargestellt.

.. _fig-distance-table:

.. figtable::
    :caption: Anschauliche Darstellung der Daten die in einer ,,Distance''
              Instanz gespeichert werden. Im Beispiel mit einer Maske die nur 3
              Attribute hat: date, genre und lyrics. Die Gewichtiungen wurde von
              der ,,EasySession'' übernommen.
    :alt: Beispielhafte Darstellung einer ,,Distance'' Instanz.
    :spec: l | l 

    +--------------------+----------------------------------------------------------------------------------+
    | *Attribut*         | *Unterdistanzen*                                                                 |
    +====================+==================================================================================+
    | ``date``           |  0.9                                                                             |
    +--------------------+----------------------------------------------------------------------------------+
    | ``genre``          |  0.05                                                                            |
    +--------------------+----------------------------------------------------------------------------------+
    | ``lyrics``         | 1.0 (Fehlender Wert --- Berechnung war nicht möglich)                            |
    +--------------------+----------------------------------------------------------------------------------+
    | Gewichtete Distanz | :math:`\frac{4\times0.9 + 8\times0.05 + 6\times1.0}{4 + 8 + 6} = 0.\overline{5}` |
    +--------------------+----------------------------------------------------------------------------------+

Manchmal kann es passieren, dass Distanzen nicht berechnet werden können. Als
Beispiel ist der Vergleich zweier Lieder anhand den Liedtexten - wenn nur einer
davon nicht gefunden werden konnte, muss das Attribut in der ``Distance`` leer
bleiben. In diesem Fall wird eine Unter--Distanz von 1.0 angenommen.

Der Grund warum man nicht nur die gewichtete Gesamtdistanz abspeichert, sondern
auch auch alle Unterdistanzen liegt darin, dass es möglich sein soll
Empfehlungen zu erklären. Durch das Vorhandensein der Unterdistanzen, kann man
später feststellen welches Attribut am stärksten in die Empfehlung mit
eingespielt hat. Zudem wird es möglich, die Gewichtungen in der Maske zur
Laufzeit zu ändern. Statt jede Distanz neu zu berechnen, müssen lediglich die
einzelnen ``Distance``--Instanzen neu gewichtet werden.

**Database:** Die ``Database`` Klasse ist eine logische Abtrennung der
``Session`` um eine einzige, allmächtige ,,Superklasse" zu verhindern. 

Sie hat folgende Aufgaben:

* Implementierung der einzelnen, oben besprochenen Graphenoperationen.
* Zu diesen Zweck hält sie eine Liste von ``Songs``.
* ID-Vergabe für jeden ``Song``.
* Verwaltung der *Playcounts*, also wie oft jeder ``Song`` gespielt wurde.
* Verwaltung der ``ListenHistory``.
* Finden von Songs mit bestimmten Attributen.

**History:** Oberklasse für ``RecommendationHistory`` und ``ListenHistory``.
Implementiert die gemeinsame Funktionalität, Songs die zeitlich hintereinander
zur ``History`` hinzugefügt werden in *Gruppen* einzuteilen. Gruppen beinhalten
maximal eine bestimmte Anzahl von Songs, ist eine *Gruppe* voll so wird eine
neue angefangen.  Vergeht aber eine zu lange Zeit seit dem letzten Hinzufügen
wird ebenfalls eine neue *Gruppe* begonnen. Jede abgeschlossene *Gruppe* wird in
der ``History`` abgespeichert. 

Das Ziel der zeitlichen Gruppierung ist eine Abbildung des Nutzerverhaltens.
Die Annahme ist hierbei, dass große zeitliche Lücken zwischen zwei Liedern auf 
wenig zusammenhängende Songs hindeuten. Zudem bilden die einzelnen *Gruppen* eine
Art ,,Warenkorb" der dann bei der Ableitung von Regeln genutzt werden kann.

**RecommendationHistory:** Implementiert den unter :ref:`recom-filter` erwähnten
Mechanismus zum Filtern von Empfehlungen.

**ListenHistory:** Unterklasse von ``History``.  Speichert die chronologische
Reihenfolge von gehörten Songs. 

Oft werden vom Endnutzer viele Lieder einfach übersprungen. Diese wenig
repräsentativen Lieder sollten nicht zur ``ListenHistory`` hinzugefügt werden.
Der Nutzer der Bibliothek sollte daher darauf achten, dass nur Lieder
hinzugefügt werden, die auch zu einem gewissen Anteil auch angehört wurden.

**RuleGenerator:** Analysiert die Gruppen innerhalb einer ``History`` und leitet
daraus mittels einer Warenkorbanalyse Assoziationsregeln ab. Diese werden danach
im ``RuleIndex`` gespeichert. 

**RuleIndex:** Speichert und indiziert die vom ``RuleGenerator`` erzeugten
Assoziationsregeln. Die Regeln werden beim Traversieren genutzt um zusätzliche
Seedsongs auszuwählen. Daher muss es möglich sein Abfragen wie ,,*Gib mir alle
Regeln die Song X betreffen*" effizient abzusetzen. 

Zudem *,,vergisst"* der Index Regeln die Songs betreffen die nicht mehr in der
``ListenHistory`` vorhanden sind.

**Provider:** Die Oberklasse von der jeder konkreter ``Provider`` ableitet:
Jeder Provider bietet eine ``do_process()`` Methode die von den Unterklassen
überschrieben wird. Zudem bieten viele Provider als *,,Convenience"* eine
``do_reverse()`` Methode um für Debuggingzwecke den Originalwert vor der
Verarbeitung durch den Provider anzuzeigen.

Provider können, mittels eines speziellen Providers, zu einer Kette
zusammengeschaltet werden. Siehe dazu auch: ``Composite`` unter
:ref:`provider-list`.

Oft kommt es vor dass die Eingabe für einen Provider viele Dupletten
enthält --- beispielsweise wird derselbe Künstler--String für viele Songs eingepflegt. 
Diese redundant zu speichern wäre bei großen Sammlungen unpraktisch daher bietet
jeder Provider die Möglichkeit einer primitiven Kompression* Statt den Wert
abzuspeichern wird eine bidirektionale Hashtable mit den Werten als Schlüssel
und einer Integer--ID auf der Gegenseite. Dadurch wird jeder Wert nur einmal
gespeichert und statt dem eigentlichen Wert wird eine ID herausgegeben.

**DistanceFuntion:** Die Oberklasse von der jede konkrete ``DistanceFunction``
ableitet: Jede Distanzfunktion bietet eine ``do_compute()`` Methode die von den
Unterklassen überschrieben wird.

Um die bei den Providern mögliche Kompression wieder rückgängig zu machen muss
die Distanzfunktion den Provider kennen.
