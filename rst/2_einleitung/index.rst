********
Einstieg
********

Begriffserklärungen
====================

.. glossary::

    Playlist

      Dynamische

    Tags

      In Audiofiles können bei den meisten Formaten Metadaten abgelegt
      werden. Dies wird oft genutzt um häufig gebrauchte Daten wie den *Artist*,
      *Album* und *Title*, aber auch komplexere Daten wie das *Coverart*,
      abzuspeichern. Tags können von geeigneten Tools wie Musicplayern
      ausgelesen werden.

    Assoziationsregel

      Eine Assoziationsregel verbindet zwei Mengen *A* und *B* von Songs
      miteinander. Sie besagen, dass wenn eine der beiden Mengen miteinander
      gehört wird, dann ist es *wahrscheinlich*, dass auch die andere Menge
      daraufhin angehört wird.

      Die Güte jeder Regel wird durch ein *Rating* beschrieben, welche grob die
      generelle Anwendbarkeit beschreibt.

      Sie werden aus dem Verhalten des Nutzers abgeleitet. Dazu wird jedes Lied
      zwischengespeichert, das der Nutzer anhört.

      *Anmerkung:* Im Allgemeinen Gebrauch sind Assoziationsregeln nur in eine
      Richtung definiert.  In *libmunin* sind die Regeln aus Gründen der
      Einfachkeit allerdings *bidirektional.*  So gilt nicht nur, dass man
      wahrscheinlich die Menge *B* hört, wenn man *A* gehört hat (:math:`A
      \rightarrow B`), sondern auch umgekehrt (:math:`A \leftrightarrow B`).

    Distanzfunktion
    
      Eine Distanzfunktion ist im Kontext von *libmunin* eine Funktion, die 
      zwei Songs als Eingabe nimmt und die Distanz zwischen
      diesen berechnet.

      Dabei wird jedes Attribut betracht, welches in beiden Songs
      vorkommt. Für diese wird von der Maske eine
      spezialisierte Distanzfunktion festgelegt, die weiß wie diese
      zwei bestimmten Werte sinnvoll verglichen werden können. Die so
      errechneten Werte werden, gemäß der Gewichtung in der Maske, zu
      einem Wert verschmolzen.

      Fehlen Attribute in einen der beiden Songs, wird für diese jeweils eine
      Distanz von 1 angenommen. Diese wird dann ebenfalls in die gewichtete
      Oberdistanz eingerechnet.

      Die folgenden Bedingungen müssen sowohl für die allgemeine
      Distanzfunktion, als auch für die speziellen Distanzfunktionen gelten.
      :math:`D` ist dabei die Menge aller Songs, :math:`d` eine Distanzfunktion:
 
      * *Uniformität* |hfill| :math:`0 \leq d(i, j) \leq 1\forall i,j \in D \;\;\;\text{(1)}`
      * *Symmetrie* |hfill| :math:`d(i, j) = d(j, i) \forall i,j \in D \;\;\;\text{(2)}`
      * *Identität* |hfill| :math:`d(i, i) = 0.0 \forall i \in D \;\;\;\text{(3)}`
      * *Dreiecksungleichung* |hfill| :math:`d(i, j) \leq d(i, x) + d(x, j) \forall i,j,x \in D \;\;\;\text{(4)}`

      .. subfigstart::

      .. _fig-trineq:

      .. figure:: figs/trineq.*
          :alt: Stuff
          :width: 100%
          :align: center
    
          Ohne Einhaltung von Gleichung (4)

      .. _fig-trineq_fixed:

      .. figure:: figs/trineq_fixed.*
          :alt: Stuff
          :width: 100%
          :align: center
    
          Mit Einhaltung von Gleichung (4)

      .. subfigend::
          :width: 0.49
          :alt: Schematische Darstellungen der einzelnen Basisiterationen.
          :label: fig-trineqs
 
          Die Beziehung dreier Songs untereinander. Die Dreiecksungleichung
          besagt, dass der direkte Weg von A nach B kürzer sein sollte als der
          Umweg über C. Die einzelnen Attribute ,,a“ und ,,b“ sind gleich stark
          gewichtet.  Wenn keine Straftwertung für leere Werte gegeben wird, so
          sind die Umwege manchmal kürzer.

      Im Kontext von *libmunin* sind nicht alle Eigenschaften wichtig, doch
      werden diese Eigenschaften trotzdem aus Gründen der Konsistenz
      eingehalten. Beispielsweise werden Werte die nicht gesetzt worden sind,
      mit einer (Teil-)Distanz von :math:`1.0` *,,bestraft"* um die Eigenschaft
      der *Dreiecksungleichung* einzuhalten. Wie das konkret aussieht, sieht man
      in Abbildung :num:`fig-trineqs`.

Allgemeine Hinweise für Entwickler
==================================

Zu Beginn sollen einige allgemeine Hinweise stichpunktartig gegeben werden, was
bei der Arbeit mit *libmunin* zu beachten ist.

- Die Qualität der Empfehlungen kann nur so gut sein wie die Qualität der
  Eingabedaten. Da in den meisten Fällen die Metadaten zu den einzelnen Liedern
  aus den *Tags* der Audiodateien kommen, empfiehlt es sich diese vorher mit 
  Musiktaggern einheitlich zu pflegen. Der Autor empfiehlt hierfür Picard,
  welches im Hintergrund auf Musicbrainz zugreift. (TODO Links.)
  Für schwerer zu besorgende Daten kann unter anderem auf libglyr, beets oder
  dem eingebauten PlyrLyrics--Provider und DiscogsGenre--Provider.
- Sollten Anwendungsentwickler je nach Einsatzzweck eine spezialisierte
  Session--Maske verwenden. 
- Welche Lieder man zu *libmunin's History* hinzufügt, sollte ebenfalls
  abgewogen werden. Fügt man auch Lieder ein welche vom Nutzer einfach
  übersprungen worden sind. 


Konkrete Hinweise für Entwickler
================================

*Hinweise zum Schreiben von Distanzfunktionen:*

- Distanzfunktionen sollten versuchen die genannten Eigenschaften einzuhalten.
- Distanzfunktionen bestehen oft aus einer einzelnen Metrik und einem
  Fusionierungsverfahren.
- *Vermeidung von überspezifischen Distanzfunktionen:* 
  Distanzfunktionen sollten nicht versuchen auch sehr schlechte Ähnlichkeiten
  noch zu *belohnen*. -> "Stretching"

Don't

.. code-block:: python

   from munin.distance import DistanceFunction

   class MyDistanceFuntion(DistanceFunction):
       def do_compute(self, A, B):
           a, b = A[0], B[0]
           return abs(a - b) / max(a, b)

Dos

.. code-block:: python

   from munin.distance import DistanceFunction

   class MyDistanceFuntion(DistanceFunction):
       def do_compute(self, A, B):
           a, b = A[0], B[0]
           diff = abs(a - b)
           if diff < 3:
              return 1.0  # Zu unterschiedlich.

           return diff / 3

Manchmal ist eine Eingrenzung des Bereichs nicht so einfach möglich, vor allem
wenn komplexere Daten 


- Defintion der :term:`Distanzfunktion` einhalten.

*Hinweise zum Schreiben von neuen Providern:*

- Provider laufen im Gegensatz zu Distanzfunktionen nur einmal. Sie sind als
  Präprozessor verstehen der die vom Nutzer eingegebenen Daten auf möglichst
  einfache und effiziente Vergleichbarkeit optimiert. Die Laufzeit die er dafür
  braucht ist daher im Vergleich zur Distanzfunktion vernachlässigbar.
- Unwichtiges weglassen
- Ist zu erwarten, dass stark redundante Daten eingepflegt werden, dann sollte
  die Provider--interne Kompression genutzt werden. Ein typisches Beispiel dafür
  ist der Künstler--Name. Dieser ist für sehr viele Songs gleich. Daher wäre
  eine separate Speicherung desselben nicht sinnvoll. 

.. code-block:: python

 from munin.provider import Provider

 class MyProvider(Provider):
     def __init__(self):
         # Kompression anschalten, ansonsten muss auf nichts geachtet werden.
         Provider.__init__(self, compress=True)

     # Funktion, die bei jeder einzelnen Eingabe aufgerufen wird.
     def do_compute(self, input_value): 
         return input_value * 2  # Tue irgendwas mit dem Input.


Im Folgenden wird der Aufbau des Graphen näher betrachtet. Danach werden einige
ausgewählte Provider mit den dazugehörigen Distanzfunktionen erläutert.
Anschließend wird noch die Fähigkeit von *libmunin* vom Nutzer automatisch
mittels Assoziationsregeln zu lernen.  Abschließend wird noch auf die Struktur
der gegebenen Empfehlungen eingegangen.

.. _ref-playlist-compare:

Vergleich verschiedener Playlisten
==================================

.. figtable::
   :alt: Vergleich verschiedener Playlisten  
   :spec: r | l l r 
   :label: table-playlists
   :caption: Vergleich verschiedener, je 15 Lieder langen Playlisten.
             Die Playlist im oberen Drittel wurde mittels des Seed--Songs (01)
             erstellt. Die im zweitem Drittel wurde mittels Mirage/Banshee
             erstellt, die letzte komplett zufällig.

   =================== ==================== ===================== ====================
   **Nummer**          **Künstler**         **Titel**             **Genre**
   =================== ==================== ===================== ====================
   **libmunin:**       
   |hline| *01*        *Knorkator*          *Böse*                *Rock/Parody, Heavy Metal*
   |hline| *02*        Letzte Instanz       Egotrip               *Rock/Folk Rock, Goth Rock*
   *03*                Nachtgeschrei        Lass mich raus        *Rock/Folk Rock*
   *04*                Knorkator            Ick wer zun Schwein   *Rock/Parody, Heavy Metal*
   *05*                Finntroll            Svart djup            *Rock/Folk Metal, Black Metal*
   *06*                Heaven Shall Burn    Endzeit               *Rock/Hardcore, Death Metal*
   *07*                In Extremo           Liam                  *Rock/Medieval, Hard Rock*
   *08*                Knorkator            Konflikt              *Rock/Parody, Heavy Metal*
   *09*                Letzte Instanz       Schlangentanz         *Rock/Folk Rock, Goth Rock*
   *10*                Marc-Uwe Kling       Scheißverein          *Folk/Pardoy*
   *11*                Johnny Cash          Heart of Gold         *Folk/Country, Rockabilly*
   *12*                Knorkator            Geh zu ihr            *Rock/Parody, Heavy Metal*
   *13*                In Extremo           Erdbeermund           *Rock/Medieval, Hard Rock*
   *14*                The Rolling Stones   Stealing My Heart     *Rock/Pop Rock, Rock & Roll*
   *15*                Knorkator            Klartext              *Rock/Parody, Heavy Metal*
   |hline| **Mirage:** 
   |hline| *02*        Knorkator            Ganz besond'rer Mann  *Rock/Parody, Heavy Metal*
   *03*                Coppelius            Operation             *Rock/Classic, Medieval Metal*
   *04*                Letzte Instanz       Salve Te              *Rock/Folk Rock, Goth Rock*
   *05*                Apocalyptica         Fisheye               *Rock/Symphonic Rock*
   *06*                Coppelius            I Told You So!        *Rock/Classic, Medieval Metal*
   *07*                Apocalyptica         Pray!                 *Rock/Symphonic Rock*
   *08*                Knorkator            Klartext              *Rock/Parody, Heavy Metal*
   *09*                Devildriver          Black Soul Choir      *Rock/Death Metal*
   *10*                Finntroll            Fiskarens Fiende      *Rock/Folk Metal, Black Metal*
   *11*                Devildriver          Swinging the Dead     *Rock/Death Metal*
   *12*                Knorkator            Es kotzt mich an      *Rock/Parody, Heavy Metal*
   *13*                Heaven Shall Burn    Forlorn Skies         *Rock/Hardcore, Death Metal*
   *14*                Knorkator            Hardcore              *Rock/Parody, Heavy Metal*
   *15*                Rammstein            Roter Sand            *Rock/Industrial, Hard Rock*
   |hline| **Zufall:**
   |hline| *02*        Schandmaul           Drei Lieder           *Rock/Folk Rock*
   *03*                Tanzwut              Götterfunken          *Electronic, Industrial*
   *04*                Finntroll            Suohengen sija        *Ambient*
   *05*                Biermösl Blosn       Anno Domini           *Brass Band, Parody*
   *06*                Finntroll            Mordminnen            *Rock/Folk Metal, Black Metal*
   *07*                The Rolling Stones   Stealing My Heart     *Rock/Pop Rock, Rock & Roll*
   *08*                Die Ärzte            Ein Mann              *Rock/Punk, Pop Rock*
   *09*                Letzte Instanz       Regenbogen            *Rock/Folk Rock, Goth Rock*
   *10*                Billy Talent         White Sparrows        *Rock/Punk, Alternative Rock*
   *11*                Letzte Instanz       Schlangentanz         *Rock/Folk Rock, Goth Rock*
   *12*                Christopher Rhyne    Shadows of the Forest *Classical, Ambient*
   *13*                The Beatles          Eight Days a Week     *Pop/Rock & Roll*
   *14*                Of Monsters and Men  From Finner           *Pop/Folk, Indie Rock*
   *15*                The Cranberries      Dreaming My Dreams    *Rock/Alternative Rock*
   =================== ==================== ===================== ====================


In Abbildung :num:`table-playlists` wird eine Auflistung verschiedener, mit
verschiedenen Methoden erstellten Playlists gegeben. Dies ist insofern
interessant, da die Struktur der von *libmunin* gegebenen Empfehlungen gewissen
Regeln unterliegt die man als Anwendungsentwickler kennen sollte. Zudem ist ein
*subjektiver* Vergleich mit anderen Systemen interessant.

Der ursprüngliche Plan hier auch eine von ``last.fm`` (TODO: link) erstellte
Playlist zu zeigen wurde eingestellt, da man dort die Empfehlungen nicht auf
die hier verwendete Testmusiksammlung aus 666 Songs einschränken konnte. 
Stattdessen wurde die *Konkurrenz* von *libmunin* getestet: *Mirage*
:cite:`schnitzer2007high`. Da *Mirage* momentan nur als Plugin für Banshee
vorhanden ist und nicht als allgemeine Bibliothek verfügbar ist, wurde die 
Testmusikdatenbank auch in Banshee importiert.

Die einzelnen Playlists wurden auf jeweils 15 Songs begrenzt. Darin enthalten
ist an erster Stelle der willkürlich ausgewählte Seed--Song, der zum Generieren
der Playlist genutzt wurde (*Knorkator --- Böse*). Die zufällig erstellte
Playlist wurde als Referenz abgedruckt, damit man die dort fehlende Struktur
sehen kann.

**Auffälligkeiten:**

- Bei *libmunin* wiederholt sich der Künstler *Knorkator* alle 3--4 Stücke,
  da der *Filter* entsprechend eingestellt ist. Daher ist eine Wiederholung des
  Künstlers nur alle 3, und eine Wiederholung des Albums nur alle 5 Stücke
  erlaubt. Bei Mirage scheint lediglich eine direkte Wiederholung des Künstlers
  scheint ausgeschlossen zu sein. Ansonsten wiederholen sich die Künstler
  relativ beliebig. Die zufällige Playlist hat zwar auch keinerlei
  Wiederholungen, aber entbehrt dafür auch jeder Struktur.
- *Mirage* leistet gute Arbeit dabei ähnlich klingende Stücke auszuwählen. Der
  relativ langsame Seed--Song (*Mirage* besitzt hier tatsächlich ein änhliches
  Konzept) besitzt eine dunke Stimmung und harte E--Gitarren. Die von *Mirage*
  vorgeschlagenen Songs schlagen hier tatsächlich sehr passend von der Stimmung
  her. Die von *libmunin* vorgeschlagenen Songs sind in Punkt Audiodaten bei
  weitem nicht so übereinstimmend. Was aber auffällig ist, ist dass größtenteils
  deutsche Titel (wie der Seed--Song) vorgeschlagen werden. Auch führt das
  *Parody* in der Genre--Beschreibung dazu, dass ebenfalls lustig oder ironisch 
  gemeinte Lieder vorgeschlagen werden. Zwar ist die Stimmung im Seed--Song
  düster, doch wird textlich ein lustiges Thema behandelt --- was *Mirage* an
  den Audiodaten natürlich nicht erkennen kann.
  Hier zeigt sich *libmunin's* (momentaner) Fokus auf Metadaten.
  Bei der zufälligen Playlists passen zwar die Genres einigermaßen übereinander,
  doch liegt das eher an dem sehr dehnbaren Begriff *Rock* der bei
  Discogs (TODO: link) für sehr viele Lieder eingepflegt ist.
- Der Kaltstart bei *Mirage* verlief in wenigen Minuten, während der Kaltstart
  bei *libmunin* beim ersten mal für die 666 Songs sehr hohe 53 Minuten
  benötigte, da für jedes Lied ein Liedtext sequentiell automatisch besorgt
  worden ist. Siehe dazu auch Tabelle :num:`table-specs`. Bei der Ausgabe der
  Empfehlungen selber war bei allen Methoden keinerlei Verzögerung zu
  beobachten.

Ressourcenverbrauch
===================

Damit Anwendungsentwickler die Aufwändigkeit einzelner Operation einschätzen
können, wird in Tabelle :num:`table-spec` eine kurze Übersicht über den
Ressourcenverbrauch einzelner Aspekte gegeben.

Die gemessenen Werte beziehen sich stets auf die Testumgebung mit 666 Songs. 

.. figtable::
   :alt: stuff
   :spec: l | r 
   :label: table-specs
   :caption: stuff

   ========================================== ==========================
   **Operation**                              **Ressourcenverbrauch**  
   ========================================== ==========================
   *Speicherverbrauch*                        77.5 MB    
   *Speicherplatz der Session (gepackt)*      0.9 MB     
   *Speicherplatz der Session (ungepackt)*    2.5 MB     
   *Zeit für den Kaltstart:*                  53 Minuten (lyrics + audio)
   |hline| ``rebuild``                        44 Sekunden
   ``add``                                    ~1ms
   ``insert``                                 164ms
   ``remove``                                 54ms
   ``modify``                                 219ms
   ========================================== ==========================

Wie man sieht, sollte noch unbedingt Zeit investiert werden um den *Kaltstart*
zu beschleunigen. Auch die ``modify``--Operation könnte durchaus noch optimiert
werden.
