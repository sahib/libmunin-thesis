Graphenoperationen
==================

Eine grobe Übersicht über die einzelnen Graphenoperationen und ihrer
Zuständigkeiteb wurde bereits in der Projektarbeit gegeben. Im Folgenden  
wird detailliert auf ihre Funktionsweise eingegangen.

``rebuild:`` Aufbau des Graphen
-------------------------------

Bevor irgendeine andere Operation ausgeführt werden kann muss mittels der
``rebuild``--Operation der Graph aufgebaut
werden. Wie bereits erwähnt in der Projektarbeit erwähnt, kann der Graph
aufgrund von einer Komplexität von :math:`O(n2)` nicht einfach durch das
Vergleichen aller Songs untereinander erfolgende. Daher muss eine Lösung mit
subquadratischen Aufwand gefunden werden. Vorzugsweise eine, bei der
Rechenaufwand gegen die Qualität der Approximation abgewägt werden kann. 
So kann der Nutzer entscheiden wie lange er *libmunin* rechnen lassen will.

Der Ausgangszustand der ``rebuild``--Operationen ist eine Liste von Songs die
vom Nutzer bereitgestellt wird. Jeder Song darin soll nun so im Graphen
platziert werden, dass er im Bestfall die ähnlichsten Songs als Nachbarn
hat. 

Jeder Song speichert seine Nachbarn mit der dazugehörigen Distanz.
Soll ein neuer Nachbar hinzugefügt werden, so wird geprüft ob die Distanz zu
diesem neuen Song besser ist als die zum schlechtesten vorhandenen Nachbar.
Ist dies der Fall, so wird die Entfernung zu diesem schlechtesten Nachbarn *in
eine Richtung* (die Gründe hierfür werden später betrachtet TODO) gekappt. Als 
Ersatz wird zu dem neuen Song eine bidirektionale Verbindung aufgebaut. Da die
Verbindung zum schlechtesten Song nur unidirektional abgebaut wird, ist die
Anzahl der Nachbarn eines Songs nicht auf einen Maximum begrenzt, da das
Hinzufügen neuer Songs *,,Einbahnstraßen"* hinterlässt.

Vielmehr handelt es sich dabei um einen Richtwert, um den sich die tatsächliche
Anzahl der Songs einpendeln wird. Momentan ist dieser Richtwert standardmäßig
auf :math:`15` gesetzt --- der durchschnittlichen Länge eines heutigen Albums
plus eins.

Wenn im folgenden vom *,,Berechnen der Distanz"* gesprochen wird, so ist damit
auch das Hinzufügen der Distanz zu den jeweiligen Song gemeint.

Im Folgenden werden die drei Schritte der ``rebuild``--Operation genauer
beleuchtet:

- **Basisiteration:** Für jeden Song wird nach willkürlich festgelegten
  Prinzipien eine kleine Menge von möglicherweise ähnlicher Songs ausgewählt. 
  Diese Menge von Songs wird untereinander mit quadratischen Aufwand verglichen.
  Diese Vorgehensweise wird mehrmals mit verschiedener Methoden wiederholt. Das
  Ziel jeder dieser Iterationen ist es für einen Song zumindestens eine kleine 
  Anzahl von ähnlichen Songs zu finden. Basierend auf diesen wird in den
  nächsten Schritten versucht die Anzahl ähnlicher Songs zu vergrößern.

  Momentan sind drei verschiedene Iterationsstrategien implementiert. Jede
  basiert auf gewissen heuristischen Annahmen die über die Eingabemenge gemacht
  wird:

    * ``sliding_window:`` Schiebt ein *,,Fenster"* über die Liste der Songs.
      Alle Songs innerhalb des Fensters werden untereinander verglichen.  Die
      Fenstergröße ist dabei konfigurierbar und ist standardmäßig auf 60
      eingestellt, da sich diese Größe nach einigen Tests als guter Kompromiss
      zwischen Qualität und Geschwindigkeit herausgestellt hat.  Bei jeder
      Iteration wird das Fenster um ein Drittel der Fenstergröße weitergeschoben.
      Dadurch entsteht eine *,,Kette"* von zusammenhängenden Songs.

      Die heuristische Annahme ist dabei, dass der Nutzer der Bibliothek seine
      Datenbank meist nach Alben sortiert eingibt. Durch diese Sortierung finden
      sich innerhalb eines Fensters oft Lieder des selben Albums --- diese  sind 
      oft sehr ähnlich.

    * ``centering_window:`` Basiert ebenfalls auf einem Fenster. Im Gegensatz
      zum obigen ``sliding_window`` besteht das Fenster allerdings aus zwei Hälften,
      wobei die eine vom Anfang an startet und die andere Hälfte von der Mitte
      aus bis zum Ende geschoben wird. Die Songs in beiden Hälften werden analog
      zu oben untereinander verglichen. Auch hier überlappen sich die einzelnen
      Hälften zu je zwei Drittel. 

      Die heuristische Annahme ist hier, dass in der bereits vorhandenen
      *,,Kette"* Querverbindungen hergestellt werden. Dies ist den nächsten
      Schritten vorteilhaft um Iterationen einzusparen.

    * ``anti_centering_window:`` Sehr ähnlich zum ``centering_window``, statt
      die zwei Hälfte aber von der Mitte aus bis zum Ende weiter zu schieben
      wird diese vom Ende zur Mitte geschoben. So werden die beiden Hälften
      solange weiter geschoben, bis sie sich in er Mitte treffen. 
      
      Auch hier sollen weitere Querverbindungen hergestellt werden.

  TODO: WIndow-sliding diagramme: cairo
  TODO: Graphen nach den einzelnen Schritten.

- **Verfeinerung:** Um den momentan sehr grob vernetzten Graphen benutzbar zu
  machen müssen einige Iterationen zur *,,Verfeinerung"* durchgeführt werden.

  Dabei wird über jeden Song im Graphen iteriert und dessen *indirekte Nachbarn*
  (also die Nachbarn der direkten Nachbarsongs) werden mit dem aktuellen Song
  verglichen. Kommen dabei Distanzen zustande, die niedriger sind als die der
  aktuellen Nachbarn, wird der indirekte Nachbar zum direkten Nachbarn. Auf
  diese Weise rücken ähnliche Songs immer weiter aufeinander zu. 
  Diese Vorgehensweise wird solange wiederholt bis nur noch eine geringe Anzahl
  von Songs *,,bewegt"* oder bis eine maximale Anzahl von Iterationen erreicht
  ist. Die Begrenzung der Iterationen ist nötig, da es Fälle geben kann in denen
  einzelne Songs immer wieder zwischen zwei gleich guten Zuständen hin- und
  herspringen können.

  Als zusätzliche Optimierung werden nicht alle indirekten Nachbarn betrachtet,
  sondern nur diese, zu denen der Weg eine gewisse *Mindestdistanz* nicht
  unterschreitet. Diese Mindestdistanz wird beim Start dabei auf :math:`2.0`
  gesetzt und während der folgenden Iterationen immer weiter abgesenkt.

  Die Gesetzmäßigkeit nach der die Mindesdistanz immer weiter abgesenkt wird ist
  dabei wie folgt beschrieben:

  .. math:: 

    \frac{4 \times mean - 2 \times sd)}{2}

- **Aufräumearbeiten:** Nach dem Verfeinerungsschritt wird der Graph von
  Einbahnstraßen durch einen ``fixing``--Schritt bereinigt und auf Konsistenz
  geprüft.

Wie bereits erwähnt gibt es eine ``rebuild_stupid``--Operation, welche für
deutlich kleinere Mengen von Songs praktikabel einsetzbar ist. Die Algorithmik
ist hierbei bedeutend einfacher: Es wird einfach jeder Song mit jedem anderen
verglichen. Als Nachbarn erhält dabei jeder Song die Nachbarn, die global
betrachtet die kleinste Distanz zu diesem besitzen. Es handelt sich als um keine
Approximation wie beim herkömmlichen ``rebuild``.

Auf die Betrachtung der Komplexität der ``rebuild``--Operation wird an dieser
Stelle verzichtet. Keine der einzelnen Schritte erreicht dabei quadratische
Komplexität.  Die einzige Ausnahme ist dabei das Vergleichen der Songs
untereinander innerhalb eines Fensters, allerdings ist dabei  die Fenstergröße
stets auf ein verträgliches Limit begrenzt. 

TODO: Menge von Vergleichen in beiden Fällen? Tabelle.
TODO: Tipps zum schreiben einer distanzfunktion für libmunin
TODO: Verweis auf abbildung im anhang mit bildern.

``fixing:`` Umbauen von Einbahnstraßen
--------------------------------------

Diese Operation dient dem Entfernen von Einbahnstraßen innerhalb des Graphen.
Einbahnstraßen können wie bereits erwähnt beim Hinzufügen neuer Distanzen
entstehen. 

Beim Entfernen wird folgendermaßen vorgegangen: Im ersten Schritt werden alle
unidirektionalen Kanten gefunden und abgespeichert. Für jede dieser Kanten wird
überprüft ob die Songs an beiden Enden den Richtwert für die Anzahl der Nachbarn
überschreitet. Sollte das nicht der Fall, so wird die Kante in eine
bidirektionale Kante umgebaut. Andernfalls wird die Kante gelöscht.

Dieses Vorgehen wurde gewählt weil es nach einigen Versuchen schwierig erschien,
den Graphen ohne Einbahnstraßen aufzubauen, ohne dass dieser zur Inselbildung
neigt. Durch den nachgelagerten ``fixing``--Schritt werden Songs die nur wenige
Nachbarn besitzen durch die vorher als zu schlecht bewerteten Kanten verbunden.

Als zusätzliche Konsistenzprüfung wird nach dem Bereinigen geprüft ob alle
Verbindungen im Graphen bidirektional sind. Sollten unidirektionale Kanten
gefunden werden, so wird eine Warnung ausgegeben.   

``add:`` Hinzufügen von Songs vor dem ``rebuild``
-------------------------------------------------

Diese Operation benötigt als Argument eine Hashtabelle mit einer Abbildung von
Attributen auf Werte. Diese Werte werden dann wie in der Projekarbeit besprochen
durch verschiedene Provider normalisiert. Mit diesen normalisierten
Informationen wird dann eine neue Song--Instanz erzeugt, welcher beim Erzeugen
ein eindeutiger Identifier zugewiesen wird. Dieser Identifier dient dann als
Index in er internen Songliste. 

Statt wie ``insert`` bereits Verbindungen zu anderen Songs herzustellen, fügt
diese Operation lediglich einen Song der internen Songliste hinzu. 

``remove:`` Löschen von Songs zur Laufzeit
------------------------------------------

Um nach einer ``rebuild``--Operation einen Song auf dem Graphen zu löschen
müssen alle Verbindungen zu diesem entfernt werden.  Um dabei eine Bildung von
Inseln (durch das Entfernen von Verbindungen) zu vermeiden, werden alle
ursprünglichen Nachbarn des zu entfernenden Songs untereinander verbunden. Dabei
wird folgendermaßen vorgegangen: Zuerst wird temporär für jeden Nachbarn den
Richtwert für die Anzahl der Nachbarn um eins erhöht. Im Anschluss wird die
Menge aller Nachbarn untereinander mit quadratischem Aufwand verglichen. Dadurch
bekommt jeder Nachbar im besten Fall eine neue Verbindung.  Abschließend werden
alle Verbindungen zum zu löschenden Song entfernt und der Richtwert wird wieder
um eins dekrementiert.

Da *libmunin* alle Songs in einer linearen List hält muss auch dort der Song
gelöscht werden. Da der Index des Songs in der Liste gleich der *UID* des Songs
ist, wird an der Stelle *UID* ein leerer Wert geschrieben. Damit dieser
möglichst bald wieder besetzt wird, wird die gelöschte *UID* in einer
*Revocation*--List gespeichert. Beim nächsten ``add`` oder ``insert`` wird diese
*UID* dann wiederverwendet.

``insert:`` Hinzufügen von Songs zur Laufzeit
----------------------------------------------

Diese Operation ist äquivalent ``add``. Als Erweiterung fügt ``insert``
allerdings den durch ``add`` erzeugten Song auch in den Graphen ein und
verbindet ihn dort. Dazu muss zuerst ein *Punkt* gefunden werden an dem der Song
passend zu seinen Attributen *eingepasst* werden kann.

Diese *Einpassung* geschieht dabei folgendermaßen:

- **Basisiteration:** Es wird mit einer gewissen *Schrittweite* über die
  Songliste iteriert. Dabei werden die Distanzen vom momentan aktuellen Song zum
  einzufügenden Song berechnet. Dadurch wird der Song bereits mit einigen
  anderen Songs verknüpft.  Die Größe der Schrittweite ist dabei abhängig von
  der Länge der Songliste.  Je länger die Liste ist, desto größer ist die
  Schrittweite.  Exakt ist sie dabei folgendermaßen definiert:

  .. math::

      Schrittweite = \lceil\log_{10}songlist\_length\rceil

- **Verfeinerung:** Songs, zu denen im vorigen Schritt eine geringe Distanz
  gefunden wurde, werden nun detaillierter betrachtet. Dazu wird die Distanz zu
  den Nachbarn dieser *guten* Songs berechnet, unter der bekannten Annahme, dass
  die indirekten Nachbar des einzufügenden Songs auch als potenzielle direkte
  Nachbarn taugen.

Als zusätzliche Beobachtung lässt sich feststellen, dass Songs die per
``insert`` eingefügt werden deutlich *weitläufiger* verbunden sind als regulär
per ``add`` hinzugefügte. Diese Eigenschaft macht sich die in der Projektarbeit 
gezeigte Demonanwedung zu Nutze: Ändert man das *Rating* eines Songs, so wird
der Song mitels ``remove`` gelöscht und mittels  ``insert`` anderswo wieder
eingefügt. Meist verbindet sich dabei der Song dann mit anderen ähnlich
bewerteten Songs. Diese bilden ein *zusätzliches Netz* über den Graphen, welches
weitläufrigere Sprünge ermöglicht.
Dadurch hat der Nutzer eine intuitive Möglichkeit den Graphen
seinen Vorstellungen nach umzubauen.

``modify:`` Verändern der Songattribute zur Laufzeit
----------------------------------------------------

Diese Operation dient als Komfortfunktion. Sie ermöglicht das Verändern der
Attribute, beziehungsweise deren zugeordneten Werte, eines einzelnen Songs. 
Würde man die Werte eines Songs manuell verändern, so müsste man alle Distanzen
zu diesem Song neu berechnen. Da dies wiederum Veränderungen im ganzen Graphen
hervorrufen könnte, wurden die Song--Instanzen unveränderbar (*,,Immutable"*)
gemacht. 

Die ``modify``--Operation umgeht dieses Problem indem es den Song erst durch ein
``remove`` entfernt und eine Kopie des ursprünglichen Songs macht, in der die
neuen Werte gesetzt werden. Dieser neue, noch unverbundene Song wird dann
mittels einer ``insert``--Operation in den Graphen eingepasst. 

Aufgrund dieser Abfolge unterschiedlicher Operation ist ``modify`` relativ
aufwendig. Es wird empfohlen diese Operation nur für einzelne Song jeweils
einzusetzen. Sollte ein bestimmtes Attribut in allen Songs geändert werden, so
ist eine ``rebuild``--Operation zu empfehlen.

Ablauf beim Hinzufügen einer Distanz
------------------------------------

Wie in TODO erwähnt, wird beim Hinzufügen einer Distanz die Schlechteste dem
Song bekannte Distanz abgefragt. Ist diese höher als die Neue wird der
Verbindung zum schlechtesten Song *gekappt* falls der Song *voll* ist.
Dieses grobe Vorgehen bringt aber bereits einige algorithmische Probleme mit
sich: Das Finden der schlechtesten Distanz erfordert jeweils linearen Aufwand.
Zwar kann die schlechteste Distanz und der dazugehörige Song zwischengespeichert
werden, doch nach einigen Tests stellte sich heraus, dass in den meisten Fällen 
ein neuer, schlechtester Song gesucht werden muss. Das ist damit zu erklären,
dass gegen Ende der ``rebuild``--Operation tendenziell immer niedrigere Distanzen 
gefunden werden.

Daher sollte man versuchen hier möglichst einen sublinearen Aufwand anzupeilen.
Ein möglicher Ansatz wird hier vorgestellt:
TODO: ...

Als Python--Pseudocode:

.. code-block:: python

    def distance_add(self, other, distance):
        if other is self:
            return False

        if self._worst_cache is not None and self._worst_cache < distance.distance:
            return False

        if distance.distance > self._max_distance:
            return False

        sdd, odd = self._dist_dict, other._dist_dict
        if other in sdd:
            if sdd[other] < distance:
                # This case should actually not happen.
                # Just here for all cases.
                return False  # Reject

            # Explain why this could damage worst song detection.
            # and why we do not care. (might change sorting)
            self._worst_cache = None
            sdd[other] = odd[self] = distance
            return True

        # Check if we still have room left
        if len(sdd) >= self._max_neighbors:
            # Find the worst song in the dictionary
            while 1:
                inversion, worst_song = self._pop_list[0]
                if worst_song in sdd:
                    worst_dist = 1.0 - inversion
                    break
                heappop(self._pop_list)

            if worst_dist < distance.distance:
                # we could prune pop_list here too,
                # but it showed that one operation only is more effective.
                self._worst_cache = worst_dist
                return False

            # delete the worst one to make place,
            # BUT: do not delete the connection from worst to self
            # we create unidir edges here on purpose.
            del sdd[worst_song]
            heappop(self._pop_list)

        # Add the new element:
        sdd[other] = odd[self] = distance

        inversion = ~distance
        heappush(self._pop_list, (inversion, other))
        heappush(other._pop_list, (inversion, self))

        # Might be something different now:
        self._worst_cache = None
        return True



