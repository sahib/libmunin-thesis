********
Einstieg
********

Begriffserklärungen
====================

.. glossary::

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

      Assoziationsregeln...

      .. math::

          Rating(A, B) = (1.0 - Kulczynski(A, B)) \cdot ImbalanceRatio(A, B)

      *wobei:* |hfill| *Aussagekraft:*
             
          - :math:`Kulczynski(A, B) =  \frac{p(A \vert B) + p(B \vert A)}{2}` |hfill| Güte der Regel
          - :math:`ImbalanceRatio(A, B) = \frac{\vert support(A) - support(B) \vert}{support(A) + support(B) - support(A \cup B)}` |hfill| Gleichmäßigkeit der Regel
          - :math:`support(X) = H_n(X)` |hfill|  Absolute Häufigkeit von X in allen Transaktionen

      Mehr dazu in der Bachelorarbeit.    

      *Vergleiche zudem:* :cite:`datamining-concepts-and-techniques` Datamining
      Concepts and Techniques.

    Distanzfunktion.

    
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
- *Vermeidung von überspezifischen Distanzfunktionen:* 
  Distanzfunktionen sollten nicht versuchen auch sehr schlechte Ähnlichkeiten
  noch zu *belohnen*. -> "Stretching"

- Defintion der :term:`Distanzfunktion` einhalten.

*Hinweise zum Schreiben von Providern:*

- Provider laufen nur einmal, Distanzfunktionen oft -> komprimieren.
- Unwichtiges weglassen

Im Folgenden wird der Aufbau des Graphen näher betrachtet. Danach werden einige
ausgewählte Provider mit den dazugehörigen Distanzfunktionen erläutert.
Anschließend wird noch die Fähigkeit von *libmunin* vom Nutzer automatisch
mittels Assoziationsregeln zu lernen.  Abschließend wird noch auf die Struktur
der gegebenen Empfehlungen eingegangen.
