*****************
Begriffsklärungen
*****************

Im Folgenden werden häufig gewisse Begriffe gebraucht, die nicht allgemein
verständlich sind oder im Kontext von *libmunin* anders gebraucht werden. 
Diese wollen wir hier definieren, bevor wir fortfahren. 

Allgemeine Fachbegriffe
-----------------------

.. glossary:: 

    Hashtabelle

      Eine Hashtabelle ist eine Datenstruktur, die eine Abbildung von
      eindeutigen Schlüsselwerten auf beliebige Werten möglich macht. Die
      interessante Eigenschaft ist dabei der konstante Zeitaufwand beim
      Nachschlagen eines Wertes durch den Schlüssel und dem Hinzufügen neuer
      Schlüssel/Wert--Paare.

    Breitensuche

      Verfahren um in definierter Weise einen Graphen zu traversieren. Dabei
      wird ausgehend von einem Knoten zuerst jeder Nachbarknoten besucht. Erst
      dann wird analog mit den Nachbarknoten verfahren.  

    Tag

      In Audiofiles, können bei den meisten Formatten, Metadaten abgelegt
      werden. Dies wird oft genutzt um häufig gebrauchte Daten wie den *Artist*,
      *Album* und *Titel*, aber auch komplexere Daten wie das *Coverart*,
      abzuspeichern. Tags können von geeigneten Tools wie Musicplayern
      ausgelesen werden.

    Iterator

      Ein Iterator ist ein *Versprechen* einen Wert genau dann zu berechnen wenn
      er gebraucht wird. Meistens werden Iteratoren dazu genutzt um 
      Datenstrukturen zu traversieren --- jeder Aufruf des Iterator liefert
      dabei den nächsten Wert.
    
    Proxymethode

      Eine *Methode* die ihre Parameter lediglich an eine andere Methode oder
      Funktion weiterreicht. Sie werden meist aus Gründen der API-Gestaltung
      eingesetzt.

    Languagebindings

      Eine *Wrapper--Schicht*, die es möglich macht, eine in einer bestimmten
      Programmiersprache (beispielsweise in C) geschriebene Bibliothek in einer
      anderen Programmiersprache (beispielsweise Python) zu nutzen. 

Kontextspezifische Fachbegriffe
-------------------------------

.. glossary:: 

    Song

      Im Kontext von *libmunin* ist ein Song eine Menge von Attributen.
      Jedem Attribut ist, wie in einer Hashmap, ein Wert zugeordnet. 

      Beispielsweise haben alle Songs ein Attribut ``artist``, aber jeder
      einzelner Song kennt dafür einen bestimmten Wert.

      Desweiteren wird für jeden Song die Distanz zu einer Menge ähnlicher
      Songs gespeichert, sowie einen Integer der als Identifier dient.

    Seedsong

      Ein :term:`Song` der als Basis für Empfehlungen ausgewählt wurde. 

    Session

      Eine *Session* ist eine Nutzung von libmunin über einem bestimmten
      Zeitraum. Zum Erstellen einer Session werden die Daten importiert,
      analysiert und ein Graph wird daraus aufgebaut.
    
      Zudem kann eine *Session* persistent für späteren Gebrauch gespeichert
      werden. 

      Wer die Bibliothek benutzt wird die *Session* zudem als Eintrittspunkt
      für die API benutzen.

    Maske

      Die :term:`Session` benötigt eine Beschreibung der Daten die importiert
      werden. So muss ich darauf geeinigt werden was beispielsweise unter dem
      Schlüssel ``genre`` abgespeichert wird.
    
      In der *Maske* werden daher die einzelnen Attribute festgelegt die ein
      einzelner Song haben kann und wie diese anzusprechen sind. Zudem wird
      pro Attribut ein :term:`Provider` und eine :term:`Distanzfunktion`
      festgelegt die bei der Verarbeitung dieses Wertes genutzt wird. Zudem
      wird die Gewichtung des Attributes festgelegtes - manche Attribute sind
      für die Ähnlichkeit zweier Songs entscheidender als andere.

    Distanz

      Eine Distanz beschreibt die Ähnlichkeit zweier Songs oder Attribute. 
      Eine Distanz von 0 bedeutet dabei eine maximale Ähnlichkeit (oder
      minimale *Entfernung* zueinander), eine Distanz von 1.0 maximale
      Unähnlichkeit (oder maximale *Entfernung*).

      Die Distanz wird durch eine :term:`Distanzfunktion` berechnet.

    Distanzfunktion

      Eine Distanzfunktion ist im Kontext von *libmunin* eine Funktion, die 
      zwei Songs als Eingabe nimmt und die Distanz zwischen
      diesen berechnet.

      Dabei wird jedes Attribut betrachte welches in beiden Songs
      vorkommt betrachtet. Für diese wird von der Maske eine
      spezialisierte Distanzfunktion festgelegt, die weiß wie diese
      zwei bestimmten Werte sinnvoll verglichen werden können. Die so
      errechneten Werte werden, gemäß der Gewichtung in der Maske, zu
      einem Wert verschmolzen.

      Fehlen Attribute in einen der beiden Songs wird für diese jeweils eine
      Distanz von 1.0 angenommen und ebenfalls in die gewichtete Oberdistanz
      eingerechnet.

      Die folgenden Bedingungen müssen sowohl für die allgemeine
      Distanzfunktion, als auch für die speziellen Distanzfunktionen gelten:
 
      * *Uniformität:* :math:`0 \leq D(i, j) \leq 1\forall i,j \in D`
      * *Symmetrie:* :math:`D(i, j) = D(j, i) \forall i,j \in D`
      * *Identität:* :math:`D(i, i) = 0.0 \forall i \in D`
      * *Dreiecksungleichung:* :math:`D(i, j) \leq D(i, x) + (x, j) \forall i,j,x \in D`

    Attribut

      Ein Attribut ist ein *Schlüssel* in der Maske. Er repräsentiert
      eine Vereinbarung mit dem Nutzer unter welchem Namen das Attribut in
      Zukunft angesprochen wird. Zu jedem gesetzten Attribut gehört ein Wert,
      andernfalls ein spezieller leerer Wert. Ein Song besteht aus einer 
      Menge dieser Paare.

    Provider

      Ein *Provider* normalisiert einen Wert anhand verschiedener
      Charakteristiken. Sie dienen als vorgelagerte Verarbeitung von den Daten
      die in das System geladen werden. Jeder *Provider* ist dabei einem 
      Attribut zugeordnet.

      Ihr Ziel ist für die Distanzfunktion einfache und effizient 
      vergleichbare Werte zu liefern - da die Distanzfunktion sehr
      viel öfters aufgerufen wird als der *Provider*.

    Assoziationsregeln
        
      Eine Assoziationsregel verbindet zwei Mengen *A* und *B* von Songs
      miteinander. Wird eine der beiden Mengen miteinander gehört, ist es
      wahrscheinlich dass auch die andere Menge daraufhin angehört wird.

      Sie werden aus dem Verhalten des Nutzers abgeleitet.

      Die Güte der Regel wird durch ein *Rating* beschrieben:

      .. math::

          Rating(A, B) = (1.0 - Kulczynski(A, B)) \cdot ImbalanceRatio(A, B)

      wobei:

          * :math:`Kulczynski(A, B) =  \frac{p(A \vert B) + p(B \vert A)}{2}`
          * :math:`ImbalanceRatio(A, B) = \frac{\vert support(A) - support(B) \vert}{support(A) + support(B) - support(A \cup B)}`
          * :math:`support(X) = H_n(X)`

      *Vergleiche dazu:* :cite:`datamining-concepts-and-techniques` Datamining
      Concepts and Techniques.
