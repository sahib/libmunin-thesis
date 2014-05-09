*****************************
Allgemeine Entwicklerhinweise
*****************************

:dropcaps:`In` diesem Kapitel werden einleitend einige allgemeine Hinweise
gegeben, die man bei der Entwicklung mit und von *libmunin* beachten sollte.
Statt wie in der API--Referenz :cite:`5LX` auf die einzelnen Methoden und
Klassen von *libmunin* einzugehen, sollen hier ,,Best Practices"
vermittelt werden.

Zur Nuztung von *libmunin*
==========================

Die Qualität der Empfehlungen kann nur so gut sein, wie die Qualität der
Eingabedaten. Da in den meisten Fällen die Metadaten zu den einzelnen Liedern
aus den Tags der Audiodateien kommen, empfiehlt es sich, diese vorher
mit Musiktaggern einheitlich zu pflegen. Der Autor empfiehlt hierfür *Picard*
:cite:`picard`, welches im Hintergrund auf *Musicbrainz* :cite:`3A3` zugreift.
Für schwerer zu besorgende Daten, wie Liedtexte, kann unter anderem auf
libglyr :cite:`9XU`, beets :cite:`XAJ` oder dem eingebauten
``PlyrLyricsProvider`` (sucht im Web nach Liedtexten) und
``DiscogsGenreProvider`` (sucht bei Discogs :cite:`DISCOGS` nach der
Genrebezeichnung) zurückgegriffen werden.

Welche Lieder man zu *libmunin's Historie* hinzufügt, sollte 
abgewogen werden. Fügt man auch Lieder ein, welche vom Nutzer einfach
übersprungen worden sind, so sind die erstellten Regeln nicht repräsentativ.
Es sollten nur Lieder hinzugefügt werden, welche mehr als :math:`50\%` 
angehört worden sind. 

Um das Format der Musiksammlung zu spezifizieren, muss der Nutzer der
Bibliothek bei einer neuen Sitzung eine Maske angeben. In dieser werden die
Provider und Distanzfunktionen für die einzelnen Attribute eines Songs
festgelegt. Mit der ``EasySession`` bietet *libmunin* aber eine Sitzung mit
vorgefertigter Maske. Anwendungsentwickler sollten aber nach Möglichkeit eine
eigene, für ihre Zwecke konfigurierte, Session--Maske verwenden. Zwar ist der
Einsatz der vorgefertigten ``EasySession`` deutlich einfacher, doch ist diese
mehr für den schnellen Einsatz gedacht.  Zudem sollte es dem Endanwender möglich
gemacht werden, die Gewichtungen der einzelnen Attribute zu ändern.

Der Begriff der Distanzfunktion
===============================

Eine Distanzfunktion ist im Kontext von *libmunin* eine Funktion, die zwei
Songs als Eingabe nimmt und die Distanz zwischen diesen berechnet. |br|
Dabei wird jedes Attribut betracht, welches in beiden Songs vorkommt. Für
diese wird von der Maske eine spezialisierte Distanzfunktion festgelegt,
die weiß wie diese zwei bestimmten Werte sinnvoll verglichen werden
können. Die so errechneten Werte werden, gemäß der Gewichtung in der
Maske, zu einem Wert verschmolzen. |br| Fehlen Attribute in einen der
beiden Songs, wird für diese jeweils eine *,,Straf"*--Distanz von
:math:`1` angenommen. Diese wird dann ebenfalls in die gewichtete
Oberdistanz eingerechnet.
Die folgenden Bedingungen müssen sowohl für die allgemeine
Distanzfunktion als auch für die speziellen Distanzfunktionen gelten.
:math:`D` ist dabei die Menge aller Songs, :math:`d` eine Distanzfunktion.
Beim Schreiben von Distanzfunktionen sollte versucht werden, alle dieser
Eigenschaften zu erfüllen. Technisch nötig sind dabei nur die Bedingungen 
1--3.
 
.. subfigstart::

.. _fig-trineq:

.. figure:: figs/trineq.*
     :width: 95%
     :align: center
    
     Ohne Einhaltung der Dreiecksungleichung.

.. _fig-trineq_fixed:

.. figure:: figs/trineq_fixed.*
     :width: 95%
     :align: center
    
     Mit Einhaltung der Dreiecksungleichung.

.. subfigend::
     :width: 0.49
     :alt: Darstellung der Dreiecksungleichung
     :label: fig-trineqs
 
     Die Beziehung dreier Songs untereinander. Die Dreiecksungleichung
     besagt, dass der direkte Weg von A nach B kürzer oder gleich lang sein
     sollte als der Umweg über C. Die einzelnen Attribute ,,a“ und ,,b“
     sind gleich stark gewichtet.  Wenn keine Straftwertung für leere Werte
     gegeben wird, so sind die Umwege manchmal kürzer.




I. *Uniformität:* :math:`\;0 \leq d(i, j) \leq 1 \;\;\forall\;\; i,j \in D`

   *Aussage:* Die errechneten Werte sollten sich immer zwischen und
   einschließlich :math:`0` und :math:`1` befinden. *libmunin* schneidet
   Werte auf diesen Bereich zu. 

II. *Symmetrie:* :math:`\;d(i, j) = d(j, i) \;\;\forall\;\; i,j \in D` 

   *Aussage:* Die Reihenfolge, in der die Songs der Distanzfunktion
   übergeben werden, darf keine Auswirkung auf das Ergebnis haben. 
   Diese Eigenschaft wird von *libmunin* nicht überprüft --- eine
   Nichteinhaltung würde zu falschen Kanten im Graphen führen.

III. *Identität:* :math:`\;d(i, i) = 0 \;\;\forall\;\; i \in D`

     *Aussage:* Wird zweimal der selbe Song übergeben, so muss die Distanz
     immer :math:`0` betragen. Autoren von Distanzfunktionen sollten dies
     testen.  Werte :math:`\neq 0` deuten auf fehlerhafte Distanzfunktionen
     hin. 

IV. *Dreiecksungleichung:* :math:`\;d(i, j) \leq d(i, x) + d(x, j) \;\;\forall\;\; i,j,x \in D, i \neq j \neq x`

    *Aussage:* In einer Dreiecksbeziehung zwischen drei Songs muss der direkte Weg
    zwischen zwei Songs immer kürzer oder gleich lang wie der Umweg über
    den dritten Song sein. Dies ist in Abbildung :num:`fig-trineqs` gezeigt. 
    Diese Eigenschaft ist nötig, damit man annehmen kann, dass direkte
    Nachbarn ähnlicher sind als indirekte Nachbarn. 


Zur Erweiterung von *libmunin*
==============================

Oft ist es von Interesse neue Distanzfunktionen und Provider für eigene Zwecke
zu schreiben. Beispielsweise könnte man ein Paar aus Provider und
Distanzfunktion verfassen um die einzelnen Mitglieder einer Band automatisch aus
dem Netz zu besorgen und mit anderen Bands zu vergleichen, um Relationen zu
finden.  Im Folgenden werden einige Beispiele gegeben und Stolperfallen
aufgelistet.

Hinweise zum Schreiben von Distanzfunktionen
--------------------------------------------

Wenn eine Distanzfunktion eine Menge von Elementen vergleichen muss,
so besteht dieselbe oft aus einem *Fusionierungsverfahren* und einer weiteren
Metrik, die die einzelnen Elemente untereinander vergleicht. Ein
Fusionierungsverfahren verschmilzt mehrere Teildistanzen auf definierte Weise
zu einer Gesamtdistanz.  Als Beispiel kann man hier den Vergleich von zwei
Mengen von Wörtern nennen.  Einzelne Wörter kann man relativ einfach auf
Ähnlichkeit untersuchen [#f1]_.  Ein
simples Fusionierungsverfahren wäre hier, jedes Wort aus der einen Menge mit
jedem Wort aus der anderen Menge zu vergleichen und den Durchschnitt der
Einzeldistanzen als Ergebnis anzunehmen. Ein anderes Fusionierungsverfahren
nimmt statt dem Durchschnitt die kleinste gefundene Distanz. Hier gibt
es kein richtig oder falsch. Je nach Einsatzzweck, muss ein passendes Verfahren
gewählt werden.  Der dazugehörige Wikipedia--Artikel bietet, unter dem Punkt
Fusionierungsalgorithmen, einen guten Überblick über weitere Verfahren:
:cite:`wiki:fusion`.
  
Distanzfunktionen sollten schlechte Werte abstrafen und gute belohnen. Während
der Entwicklung hat sich gezeigt, dass simple Distanzfunktionen, die auch für
gar nicht mehr ähnliche Werte eine Distanz errechnen, die :math:`\neq 1,0`
ist, zu qualitativ schlechten Verbindungen im Graphen führen. Man sollte daher
den Bereich, in denen man eine Distanz :math:`< 1,0` vergibt, einschränken. 

.. _fig-stretch:

.. figure:: figs/scale.*
   :alt: Skalierungsfunktion der Distanzfunktion
   :align: center
   :width: 70%
  
   Die blaue Kurve zeigt die skalierten Werte der Distanzfunktion in Blau.
   Werte unter 0,5 werden etwas herabgesetzt, schlechtere Werte über 0,5
   werden erhöht.  Zur Referenz ist die ursprüngliche Gerade in Grün gegeben.


Im folgendem Beispiel wird dies nicht getan und in der nachfolgenden
Version verbessert:  

.. code-block:: python

   from munin.distance import DistanceFunction

   # Eine Distanzfunktion, die beispielsweise ein Rating von 1-5 vergleicht.
   # Leite von der Distanzfunktions-Oberklasse ab:
   class WrongDistanceFuntion(DistanceFunction):
       def do_compute(self, A, B):
           # A und B sind, der Konsistenz halber auch bei einzelnen Werten immer Tupel
           # Daher müssen wir diese erst "entpacken".
           a, b = A[0], B[0]

           return abs(a - b) / max(a, b)  # Teile Differenz durch Maximum aus beiden:

   class CorrectDistanceFuntion(DistanceFunction):
       def do_compute(self, A, B):
           diff = abs(A[0] - B[0])
           if diff > 3:
              return 1,0    # Zu unterschiedlich.
           return diff / 4  # Verteile auf [0, 0.25, 0.5, 0.75]

Manchmal ist eine Eingrenzung des Bereichs nicht so einfach möglich, vor allem
wenn komplexere Daten im Spiel sind. Dann empfiehlt es sich, die Verteilung der
Distanz auf den Bereich zwischen :math:`0,0` und :math:`1,0` zu untersuchen.
Sollte sich die Distanz beispielsweise gehäuft im Bereich zwischen :math:`0,3`
und :math:`0,7` bewegen, so ist es empfehlenswert diesen Bereich zu dehnen.
In Abbildung :num:`fig-stretch` werden mit der Funktion [#f2]_  :math:`f(x) =
-2\frac{2}{3}x^{3} + 4x^{2} - \frac{1}{3}x` Distanzen unter :math:`0,5`
verbessert und darüber verschlechtert. 

Hinweise zum Schreiben von neuen Providern
------------------------------------------

Provider laufen im Gegensatz zu Distanzfunktionen nur einmal. Sie sind als
Präprozessor zu verstehen, der die vom Nutzer eingegebenen Daten auf möglichst
einfache und effiziente Vergleichbarkeit optimiert. Die Laufzeit, die er dafür
braucht, ist daher im Vergleich zur Distanzfunktion vernachlässigbar.  Daher
sollte gut abgewogen werden, wieviele Daten man dem Provider produzieren lässt.
Im Zweifelsfall, empfiehlt es sich, Unnötiges wegzulassen. Ist zu erwarten,
dass stark redundante Daten eingepflegt werden, dann sollte die
provider--interne Kompression genutzt werden. Ein typisches Beispiel dafür ist
der Künstlername. Dieser ist für sehr viele Songs gleich. Daher wäre eine
separate Speicherung desselben nicht sinnvoll. Intern bildet eine
bidirektionale Hashtabelle [#f3]_ (mittels des Python--Pakets ``bidict``
:cite:`bidict`) gleiche Werte auf einen Integer--Schlüssel ab.
Dies wird im folgenden Python--Beispiel gezeigt:

.. code-block:: python

   from munin.provider import Provider
  
   class DoublingProvider(Provider):   # Leite von der Provider-Oberklasse ab.
       def __init__(self): 
           # Kompression anschalten, ansonsten muss auf nichts geachtet werden.
           Provider.__init__(self, compress=True)
       
       def do_compute(self, input_value):  # Wird bei jeder Eingabe aufgerufen.
           return input_value * 2  # Tue irgendwas mit dem Input.
  
  
.. _ref-playlist-compare:

Vergleich verschiedener Playlisten
==================================

Eine *Playlist,* zu deutsch *Wiedergabeliste*, ist eine Liste einzelner
Lieder, die nacheinander abgespielt werden. Die Zusammstellung einer
Playlist erfüllt oft einen gewissen Zweck. So stellt man für gewöhnlich
Lieder in einer *Playlist* zusammen, die eine gemeinsame Stimmung oder
eine andere Gemeinsamkeit *(,,Favorit")* besitzen. Im Folgenden wird die 
subjektive Qualität der Playlisten bezüglich der Ähnlichkeit der einzelnen
Stücke beurteilt.

In Abbildung :num:`table-playlists` wird eine Auflistung verschiedener, mit
unterschiedlichen Methoden erstellter  Playlisten gegeben. Dies ist 
interessant, da die Struktur der von *libmunin* gegebenen Empfehlungen gewissen
Regeln unterliegt, die man als Anwendungsentwickler kennen sollte. Zudem ist der
subjektive Vergleich mit anderen Systemen interessant.

Der ursprüngliche Plan, hier auch eine von ``last.fm`` :cite:`9NT` erstellte
Playlist zu zeigen wurde eingestellt, da man dort die Empfehlungen nicht
auf die hier verwendete Testmusiksammlung aus 666 Songs einschränken konnte.
Stattdessen wurde eine Alternative zu *libmunin* getestet: *Mirage*
:cite:`schnitzer2007high`. Da *Mirage* momentan nur als Plugin für Banshee
vorhanden ist und nicht als allgemeine Bibliothek verfügbar, wurde die
Testmusikdatenbank auch in Banshee importiert.
Die Testmusikdatenbank selbst besteht aus einigen ausgewählten Alben des Autors.
Viele allgemein gebräuchliche Genres werden dabei abgedeckt, obwohl der
Schwerpunkt beim Genre *Rock* und *Metal* liegt.
Die einzelnen Playlisten wurden auf jeweils 15 Songs begrenzt. Darin enthalten
ist an erster Stelle der willkürlich ausgewählte Seedsong, der zum
Generieren der Playlist genutzt wurde (*Knorkator --- Böse*). Die zufällig
erstellte Playlist wurde als Referenz abgedruckt, damit man die dort fehlende
Struktur sehen kann.

**Auffälligkeiten:**

Bei *libmunin* wiederholt sich der Künstler *Knorkator* alle 3--5 Stücke,
da der *Filter* entsprechend eingestellt ist. Daher ist eine Wiederholung des
Künstlers nur alle drei und eine Wiederholung des Albums nur alle fünf Stücke
erlaubt. Bei Mirage scheint lediglich eine direkte Wiederholung des Künstlers
ausgeschlossen zu sein. Ansonsten wiederholen sich die Künstler
beliebig. Die zufällige Playlist hat zwar auch keinerlei
Wiederholungen, aber entbehrt dafür auch jeglicher Struktur.

*Mirage* leistet gute Arbeit dabei, ähnlich klingende Stücke auszuwählen. Der
tempomäßig vergleichsweise langsame Seedsong (*Mirage* besitzt hier tatsächlich ein
ähnliches Konzept) besitzt eine dunkle Stimmung und harte E--Gitarren. Die von
*Mirage* vorgeschlagenen Songs sind hier tatsächlich sehr passend zu dieser
Stimmung. Die von *libmunin* vorgeschlagenen Songs sind in Punkt
Audiodaten, bei weitem nicht so übereinstimmend. Was aber auffällig ist, ist
dass größtenteils deutsche Titel (wie der Seedsong) vorgeschlagen werden. Auch
führt das *Parody* in der Genre--Beschreibung dazu, dass ebenfalls lustig oder
ironisch gemeinte Lieder vorgeschlagen werden. Zwar ist die Stimmung im
Seedsong düster, doch wird textlich ein Thema ironisch behandelt --- was
*Mirage* an den Audiodaten natürlich nicht erkennen kann.  Hier zeigt sich
*libmunin's* (momentaner) Fokus auf Metadaten.  Bei der zufälligen Playlist
stimmen die Genres einigermaßen überein, doch liegt das eher an dem
sehr dehnbaren Begriff *Rock*, der bei
Discogs :cite:`DISCOGS` für sehr viele Lieder eingepflegt ist.

Der Kaltstart bei *Mirage* verlief in wenigen Minuten, während der Kaltstart
bei *libmunin* beim ersten Mal für die 666 Songs im Vergleich dazu sehr lange
(etwa 53 Minuten) benötigte. Größtenteils liegt das daran, dass für jedes Lied
ein Liedtext sequentiell automatisch besorgt wird. Siehe dazu auch
Tabelle :num:`table-specs`.  Bei der Ausgabe der Empfehlungen selber, war bei
allen Methoden keinerlei Verzögerung zu beobachten.

Ressourcenverbrauch
===================

Damit Anwendungsentwickler die Aufwändigkeit einzelner Operation einschätzen
können, wird in Tabelle :num:`table-specs` eine kurze Übersicht über den
Ressourcenverbrauch einzelner Aspekte gegeben.
Die gemessenen Werte beziehen sich stets auf die Testumgebung mit 666 Songs. 

.. figtable::
   :alt: Auflistung des Ressourcenverbrauchs verschiedener Operationen
   :spec: l | r 
   :label: table-specs
   :caption: Auflistung des Ressourcenverbrauchs verschiedener Operationen.

   ============================================ ==========================
   **Operation**                                **Ressourcenverbrauch**  
   ============================================ ==========================
   *Speicherverbrauch*                          77,5 MB    
   *Speicherplatz der Session  (gzip--gepackt)* 0,9 MB     
   *Speicherplatz der Session (ungepackt)*      2,5 MB     
   *Zeit für den Kaltstart*                     53 Minuten *(63% Liedtextsuche + 37% Audioanalyse)*
   |hline| ``rebuild``                          44 Sekunden
   ``add``                                      87ms
   ``insert``                                   164ms
   ``remove``                                   54ms
   ``modify``                                   219ms
   ============================================ ==========================


Wie man sieht, sollte noch unbedingt Zeit investiert werden um den *Kaltstart*
zu beschleunigen. Auch die ``modify``--Operation könnte durchaus noch optimiert
werden. Wie allen anderen Geschwindigkeitsangaben in dieser Arbeit, beziehen 
sich diese auf den Rechner des Entwicklers und sind daher nur untereinander
vergleichbar.


.. figtable::
   :alt: Vergleich verschiedener Playlisten  
   :spec: r | l l r 
   :label: table-playlists
   :caption: Vergleich verschiedener, je 15 Lieder langen Playlisten.
             Die Playlist im oberen Drittel wurde mittels des Seedsongs (01)
             erstellt. Die im zweitem Drittel wurde mittels Mirage/Banshee
             erstellt, die letzte wurde komplett zufällig generiert.

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
   *10*                Marc-Uwe Kling       Scheißverein          *Folk/Parody*
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

.. rubric:: Footnotes

.. [#f1] Etwa mit der Levenshtein--Distanzfunktion :cite:`brill2000improved` und
   der Python--Bibliothek ``pyxDamerauLevenshtein``
   :cite:`pyxdameraulevenshtein`.

.. [#f2] Die Werte der Funktion können leicht unter 0 und über 1 gehen. Um den
   Begriff der Distanz einzuhalten, werden die Werte auf den Bereich 
   :math:`[0, 1]` zugeschnitten.

.. [#f3]  Eine Hashtabelle ist eine Datenstruktur, die eine effiziente Abbildung
   von eindeutigen Schlüsselwerten auf beliebige Werte möglich macht. 
   Der Aufwand für den Zugriff auf einzelne Werte ist dabei konstant.
   
