*****************************
Allgemeine Entwicklerhinweise
*****************************

In diesem Kapitel werden einleitend einige allgemeine Hinweise gegeben, die man
bei der Entwicklung mit und von *libmunin* beachten sollte.

In den darauf folgenden Kapiteln wird detailliert der Aufbau des Graphen, sowie 
einige ausgewählte Distanzfunktionen und Provider detailliert beleuchtet.
Zum Ende hin wird auch auf den Mechanismus eingegangen den *libmunin* zum Lernen
nutzt.

Zur Nuztung von *libmunin*
==========================

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

Zur Erweiterung von *libmunin*
==============================

Hinweise zum Schreiben von Distanzfunktionen
--------------------------------------------

- Distanzfunktionen sollten versuchen die genannten Eigenschaften einzuhalten.
- Distanzfunktionen bestehen oft aus einer einzelnen Metrik und einem
  Fusionierungsverfahren.
- *Überspezifische* Distanzfunktionen sollten vermieden werden.
  In anderen Worten: Unähnliche Objekte sollten auch bestraft werden. 

  .. code-block:: python

     from munin.distance import DistanceFunction

     class MyDistanceFuntion(DistanceFunction):
         def do_compute(self, A, B):
             # A und B sind, der Konsistenz halber, immer Tupel..
             # Daher müssen wir diese erst ,,entpacken".
             a, b = A[0], B[0]
             return abs(a - b) / max(a, b)

  .. code-block:: python

     from munin.distance import DistanceFunction

     class MyDistanceFuntion(DistanceFunction):
         def do_compute(self, A, B):
             diff = abs(A[0] - B[0])
             if diff > 3:
                return 1.0  # Zu unterschiedlich.

             return diff / 3

- Manchmal ist eine Eingrenzung des Bereichs nicht so einfach möglich, vor allem
  wenn komplexere Daten im Spiel sind. Dann empfiehlt es sich zu Untersuchen in
  welchem Bereich sich die berechnete Distanz bewegt.  Sollte sie sich
  beispielsweise immer im Bereich zwischen :math:`0.3` und :math:`0.7` bewegen,
  so ist es empfehlenswert diesen Bereich zu *dehnen*.  In :num:`fig-stretch`
  werden mit der Funktion :math:`f(x) = -2\frac{2}{3}x^{3} + 4x^{2} -
  \frac{1}{3}x` Distanzen unter :math:`0.5` verbessert und darüber
  verschlechtert.

  .. _fig-stretch:

  .. figure:: figs/scale.*
     :alt: Skalierungsfunktion der Distanzfunktion
     :align: center
     :width: 100%

     Skalierungsfunktion der Distanzfunktion
    
- Defintion der :term:`Distanzfunktion` einhalten.

Hinweise zum Schreiben von neuen Providern
------------------------------------------

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
  
  
.. _ref-playlist-compare:

Vergleich verschiedener Playlisten
==================================

.. figtable::
   :alt: Vergleich verschiedener Playlisten  
   :spec: r | l l r 
   :label: table-playlists
   :caption: Vergleich verschiedener, je 15 Lieder langen Playlisten.
             Die Playlist im oberen Drittel wurde mittels des Seedsongs (01)
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
ist an erster Stelle der willkürlich ausgewählte Seedsong, der zum Generieren
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
  relativ langsame Seedsong (*Mirage* besitzt hier tatsächlich ein änhliches
  Konzept) besitzt eine dunke Stimmung und harte E--Gitarren. Die von *Mirage*
  vorgeschlagenen Songs schlagen hier tatsächlich sehr passend von der Stimmung
  her. Die von *libmunin* vorgeschlagenen Songs sind in Punkt Audiodaten bei
  weitem nicht so übereinstimmend. Was aber auffällig ist, ist dass größtenteils
  deutsche Titel (wie der Seedsong) vorgeschlagen werden. Auch führt das
  *Parody* in der Genre--Beschreibung dazu, dass ebenfalls lustig oder ironisch 
  gemeinte Lieder vorgeschlagen werden. Zwar ist die Stimmung im Seedsong
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
   :alt: Auflistung des Ressourcenverbrauchs verschiedener Operationen
   :spec: l | r 
   :label: table-specs
   :caption: Auflistung des Ressourcenverbrauchs verschiedener Operationen.

   ========================================== ==========================
   **Operation**                              **Ressourcenverbrauch**  
   ========================================== ==========================
   *Speicherverbrauch*                        77.5 MB    
   *Speicherplatz der Session (gepackt)*      0.9 MB     
   *Speicherplatz der Session (ungepackt)*    2.5 MB     
   *Zeit für den Kaltstart:*                  53 Minuten (33 Minuten Liedtexte + 20 Minuten Audioanalyse)
   |hline| ``rebuild``                        44 Sekunden
   ``add``                                    ~1ms
   ``insert``                                 164ms
   ``remove``                                 54ms
   ``modify``                                 219ms
   ========================================== ==========================

Wie man sieht, sollte noch unbedingt Zeit investiert werden um den *Kaltstart*
zu beschleunigen. Auch die ``modify``--Operation könnte durchaus noch optimiert
werden. 
