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
Rechenaufwand gegen die Qualität der Approximation eingetauscht werden kann. 
So kann der Nutzer entscheiden wie lange er *libmunin* rechnen lassen will.

Der Ausgangszustand der ``rebuild``--Operationen ist eine Liste von Songs die
vom Nutzer bereitgestellt wird. Jeder Song darin soll nun so im Graphen
platziert werden, dass er (im besten Fall) die ähnlichsten Songs als Nachbarn
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

    * ``centering_window:`` Basiert ebenfalls auf einem Fenster. Anders als beim
      ``sliding_window`` besteht das Fenster allerdings aus zwei Hälften, wobei
      die eine vom Anfang an startet und die andere Hälfte von der Mitte aus bis
      zum Ende geschoben wird. Die Songs in beiden Hälften werden analog zu oben 
      untereinander verglichen. Auch hier überlappen sich die einzelnen Hälften
      zu je zwei Drittel. 

      Die heuristische Annahme ist hier, dass in der bereits vorhandenen
      *,,Kette"* Querverbindungen hergestellt werden. Dies ist den nächsten
      Schritten vorteilhaft um Iterationen einzusparen.

    * ``anti_centering_window:`` Sehr ähnlich zum ``centering_window``, statt
      die zwei Hälfte aber von der Mitte aus bis zum Ende weiter zu schieben
      wird diese vom Ende zur Mitte geschoben. So werden die beiden Hälften
      solange weiter geschoben, bis sie sich in er Mitte treffen. 
      
      Auch hier sollen weitere Querverbindungen hergestellt werden.

  TODO: WIndow-sliding diagramme
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


TODO: Verweis auf abbildung im anhang mit bildern.

``fixing:`` Umbauen von Einbahnstraßen
--------------------------------------

Diese Operation dient dem Entfernen von Einbahnstraßen innerhalb des Graphen.
Einbahnstraßen können wie bereits erwähnt beim Hinzufügen neuer Distanzen
entstehen. 

Beim Entfernen wird folgendermaßen vorgegangen: Im ersten Schritt werden alle
unidirektionalen Kanten gefunden und abgespeichert. Für jede dieser Kanten wird
überprüft ob die Songs an beiden Enden die maximale Anzahl der Nachbarn
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



``remove:`` Löschen von Songs zur Laufzeit
------------------------------------------

``insert:`` Hinzufügen von Songs zur Laufzeit
----------------------------------------------

Die modify operation ist eine komfort funktion aus remove und insert.
