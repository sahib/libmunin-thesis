*****************
Begriffsklärungen
*****************

Im Folgenden werden häufig gewisse Begriffe gebraucht, die nicht allgemein
verständlich, oder die im Kontext von *libmunin* anders besetzt sind.
Diese sollen hier definiert werden, bevor fortgefahren wird.

Allgemeine Fachbegriffe
-----------------------

.. glossary:: 

    Hashtabelle

      Eine Hashtabelle ist eine Datenstruktur, die eine Abbildung von
      eindeutigen Schlüsselwerten auf beliebige Werte möglich macht. Die
      interessante Eigenschaft ist dabei der konstante Zeitaufwand beim
      Nachschlagen eines Wertes durch den Schlüssel und dem effizienten 
      Hinzufügen neuer Schlüssel/Wert--Paare.

    Breitensuche

      Verfahren um in definierter Weise einen Graphen zu traversieren. Dabei
      wird ausgehend von einem Knoten zuerst jeder Nachbarknoten besucht. Erst
      dann wird analog mit den Nachbarknoten verfahren. Bereits besuchte Knoten
      werden markiert und nicht weiter verfolgt.

    Tags

      In Audiofiles können bei den meisten Formaten Metadaten abgelegt
      werden. Dies wird oft genutzt um häufig gebrauchte Daten wie den *Artist*,
      *Album* und *Title*, aber auch komplexere Daten wie das *Coverart*,
      abzuspeichern. Tags können von geeigneten Tools wie Musicplayern
      ausgelesen werden.

    Iterator

      Ein Iterator ist ein *Versprechen* einen Wert genau dann zu berechnen wenn
      er gebraucht wird. Meistens werden Iteratoren dazu genutzt, um
      Datenstrukturen zu traversieren. Jeder Aufruf des Iterator liefert dabei
      den nächsten Wert oder signalisiert, dass keine neuen Werte mehr vorhanden
      sind.
    
    Proxymethode

      Eine *Methode*, die ihre Parameter lediglich an eine andere Methode oder
      Funktion weiterreicht. Sie werden meist aus Gründen der API--Gestaltung
      eingesetzt.

    Languagebindings

      Eine Zusatzprogrammschicht, die es möglich macht, eine in einer bestimmten
      Programmiersprache (beispielsweise in :math:`\mathrm{C}`) geschriebene
      Bibliothek in einer anderen Programmiersprache (beispielsweise Python) zu
      nutzen. 

Kontextspezifische Fachbegriffe
-------------------------------

.. glossary:: 

    Song

      Im Kontext von *libmunin* ist ein Song eine Menge von Attributen.  Jedem
      :term:`Attribut` ist, wie in einer Hashtabelle, genau ein Wert zugeordnet. 

      Beispielsweise haben alle Songs ein Attribut ``artist``, aber jeder
      einzelner Song kennt dafür einen bestimmten Wert.

      Desweiteren wird für jeden Song die Distanz zu einer Menge ähnlicher
      Songs gespeichert, sowie einen Integer der als Identifier dient.

    Seedsong

      Ein :term:`Song` der als Basis für Empfehlungen ausgewählt wurde. 

    Session

      Eine *Session* ist eine Nutzung von *libmunin* über einem bestimmten
      Zeitraum. Zum Erstellen einer Session werden die Daten importiert,
      analysiert und ein Graph wird daraus aufgebaut.
    
      Wer die Bibliothek benutzt, wird die *Session* zudem als Eintrittspunkt
      für die API benutzen.

    Maske

      Die :term:`Session` benötigt eine Beschreibung der Daten die importiert
      werden. So muss sich beispielsweise darauf geeinigt werden, *was* in einem
      :term:`Song` unter dem Schlüssel ``genre`` abgespeichert wird.
    
      In der *Maske* werden daher die einzelnen Attribute festgelegt die ein
      einzelner Song haben kann und wie diese anzusprechen sind. Zudem wird
      pro Attribut ein :term:`Provider` und eine :term:`Distanzfunktion`
      festgelegt, die bei der Verarbeitung dieses Wertes genutzt wird. Zudem
      wird die Gewichtung des Attributes festgelegt. Manche Attribute sind
      für die Ähnlichkeit zweier Songs entscheidender als andere.

    Distanz

      Eine Distanz beschreibt die Ähnlichkeit zweier Songs.
      Eine Distanz von 0 bedeutet dabei eine maximale Ähnlichkeit (oder
      minimale *Entfernung* zueinander), eine Distanz von 1 maximale
      Unähnlichkeit (oder maximale *Entfernung*).

      Die Distanz wird durch eine :term:`Distanzfunktion` berechnet.

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

    Attribut

      Ein Attribut ist ein *Schlüssel* in der :term:`Maske`. Er repräsentiert
      eine Vereinbarung mit dem Nutzer unter welchem Namen das Attribut in
      Zukunft angesprochen wird. Zu jedem gesetzten Attribut gehört ein Wert,
      andernfalls ein spezieller leerer Wert. Ein Song besteht aus einer 
      Menge dieser Paare.

    Provider

      Ein *Provider* normalisiert einen Wert anhand verschiedener
      Charakteristiken. Sie dienen zur vorgelagerten Verarbeitung von den Daten
      die in *libmunin* geladen werden. Jeder *Provider* ist dabei durch die
      :term:`Maske` einem Attribut zugeordnet.

      Ihr Ziel ist für die :term:`Distanzfunktion` einfache und effizient 
      vergleichbare Werte zu liefern - da die Distanzfunktion sehr
      viel öfters aufgerufen wird als der *Provider*.

    Assoziationsregeln
        
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
