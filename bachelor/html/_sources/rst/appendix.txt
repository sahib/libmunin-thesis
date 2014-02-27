.. only:: latex

   .. raw:: latex

       \appendix

Abkürzungsverzeichnis
======================

.. figtable::
    :spec: >{\raggedleft\arraybackslash}p{0.25\linewidth} | p{0.65\linewidth}

    =======================  ==================================
    Abkürzung                Bedeutung
    =======================  ==================================
    **API**                  *Application Programming Interface*
    **GUI**                  *Graphical User Interface*
    **LoC**                  *Lines of Code*
    =======================  ==================================

.. only:: latex

   .. raw:: latex

       \newpage

Glossar
=======

.. glossary:: 

    Song

        Im Kontext von *libmunin* ist ein Song eine Menge von Attributen.
        Jedem Attribut ist, wie in einer Hashmap, ein Wert zugeordnet. 

        Beispielsweise haben alle Songs ein Attribut ``artist``, aber jeder
        einzelner Song kennt dafür einen bestimmten Wert.

        Desweiteren wird für jeden Song die Distanz zu einer Menge ähnlicher
        Songs gespeichert, sowie einen Integer der als Identifier dient.

    Distanz

        Eine Distanz beschreibt die Ähnlichkeit zweier Songs oder Attribute. 
        Eine Distanz von 0 bedeutet dabei eine maximale Ähnlichkeit (oder
        minimale *Entfernung* zueinander), eine Distanz von 1.0 maximale
        Unähnlichkeit (oder maximale *Entfernung*).

        Die Distanz wird durch eine :term:`Distanzfunktion` berechnet.

    Distanzfunktion

        Eine Distanzfunktion ist im Kontext von *libmunin* eine Funktion, die 
        zwei Songs als Eingabe nimmt und die :term:`Distanz` zwischen
        diesen berechnet.

        Dabei wird jedes :term:`Attribut` betrachte welchesi n beiden Songs
        vorkommt betrachtet. Für diese wird von der :term:`Maske` eine
        spezialisierte :term:`Distanzfunktion` festgelegt, die weiß wie diese
        zwei bestimmten Werte sinnvoll verglichen werden können. Die so
        errechneten Werte werden, gemäß der Gewichtung in der :term:`Maske`, zu
        einem Wert verschmolzen.

        Fehlen Attribute in einen der beiedn Songs wird für diese jeweils eine
        Distanz von 1.0 angenommen und ebenfalls in die gewichtete Oberdistanz
        eingerechnet.

        Die folgenden Bedingungen müssen sowohl für die allgemeine
        Distanzfunktion, als auch für die speziellen Distanzfunktionen gelten:
 
        *Uniformität:*
        
        .. math::

            0 \leq D(i, j) \leq 1 \, \forall \, i,j \in D

        *Symmetrie:*

        .. math::

            D(i, j) = D(j, i) \, \forall \, i,j \in D

        *Identität:*

        .. math::

            D(i, i) = 0.0 \, \forall \, i \in D

        *Dreiecksungleichung:*

        .. math::

            D(i, j) \leq D(i, x) + (x, j)

    Session

        Eine *Session* ist eine Nutzung von *libmunin* über einem bestimmten
        Zeitraum. Zum Erstellen einer Session werden die Daten importiert,
        analysiert und ein :term:`Graph` wird daraus aufgebaut.
    
        Zudem kann eine *Session* persistent für späteren Gebrauch gespeichert
        werden. 

        Für Nutzer der Bibliothek ist die :term:`Session` auch Eintrittspunkt
        für jegliche von *libmunin* bereitgestellte Funktionalität.

    Maske

        Die :term:`Session` benötigt eine Beschreibung der Daten die importiert
        werden. So muss ich darauf geeinigt werden was beispielsweise unter dem
        Schlüssel ``genre`` abgespeichert wird.
    
        In der *Maske* werden daher die einzelnen Attribute festgelegt, die ein
        einzelner Song haben kann und wie diese anzusprechen sind. Zudem wird
        pro Attribut ein :term:`Provider` und eine :term:`Distanzfunktion`
        festgelegt die bei der Verarbeitung dieses Wertes genutzt wird. Zudem
        wird die Gewichtung des Attributes festgelegt - manche Attribute sind
        für die Ähnlichkeit zweier Songs entscheidender als andere.

    Attribut

        Ein Attribut ist ein *Schlüssel* in der :term:`Maske`. Er repräsentiert
        eine Vereinbarung mit dem Nutzer unter welchem Namen das Attribut in
        Zukunft angesprochen wird. Zu jedem gesetzten Attribut gehört ein Wert,
        andernfalls ein spezieller leerer Wert. Ein Song besteht aus einer 
        Menge dieser Paare.

    Provider

        Ein *Provider* normalisiert einen Wert anhand verschiedener
        Charakteristiken. Sie dienen als vorgelagerte Verarbeitung von den Daten
        die in das System geladen werden. Jeder *Provider* ist dabei einem 
        :term:`Attribut` zugeordnet.

        Ihr Ziel ist für die :term:`Distanzfunktion` einfache und effizient 
        vergleichbare Werte zu liefern - da die :term:`Distanzfunktion` sehr
        viel öfters aufgerufen wird als der *Provider*.

    Assoziationsregel
        
        Eine Assoziationsregel verbindet zwei Mengen *A* und *B* von Songs
        miteinander. Wird eine der beiden Mengen miteinander gehört, ist es
        wahrscheinlich dass auch die andere Menge daraufhin angehört wird.

        Sie werden aus dem Verhalten des Nutzers abgeleitet.

        Die Güte der Regel wird durch ein *Rating* beschrieben:

        .. math::

            Rating(A, B) = (1.0 - Kulczynski(A, B)) \cdot ImbalanceRatio(A, B)

        wobei:

        .. math::

            Kulczynski(A, B) =  \frac{p(A \vert B) + p(B \vert A)}{2}

        .. math::

            ImbalanceRatio(A, B) = \frac{\vert support(A) - support(B) \vert}{support(A) + support(B) - support(A \cup B)}


        .. admonition:: Vergleiche dazu:

            :cite:`datamining-concepts-and-techniques`
            Datamining Concepts and Techniques.


    Recommendation

        Eine Recommendation (dt. Empfehlung) ist ein :term:`Song` der vom System
        auf Geheiß des Benutzers hin vorgeschlagen wird. 

        Die Empfehlunge sollte eine geringe Distanz zum :term:`Seedsong` haben.

    Seedsong

        Ein Song der als Basis für Empfehlungen ausgewählt wurde. 

    Graph 

        Im Kontext von *libmunin* ist der Graph eine Abbildung aller Songs (als
        Knoten) und deren Distanz (als Kanten) untereinander. Im idealen Graphen
        kennt jeder :term:`Song` *N* zu ihm selbst ähnlichsten Songs als
        Nachbarn.

        Da die Erstellung eines idealen Graphen sehr aufwendig ist, wird auf
        eine schneller zu berechnende Approximation zurückgegriffen.

.. _gengre-graph-vis:

Visualisierungen des Genregraph
===============================

Der gesamte Genrebaum ist schwer im Ganzen übersichtlich darzustellen. Deshalb
folgen drei unterschiedliche Versionen, mit unterschiedlichen Detailstufen:

* :num:`fig-genre-graph-min`: Nur die wichtigsten Genres werden gezeigt.
* :num:`fig-genre-graph-mid`: Grob alle populären Genres werden gezeigt.
* :num:`fig-genre-graph-big`: Alle Genres werden gezeigt.

**Bedeutung der Farben:** Der Farbton der Knoten varriert je nach Tiefe. Knoten
der ersten Ebene sind rot. Je tiefer desto mehr wandelt sich der Farbton
Richtung grün. Die Sättigung der Knoten zeigt die Anzahl der Kinder des Knoten
an. Sehr gesättigte Knoten haben viele Kinder. Der Wurzelknoten *Music* ist von
dieser Regel ausgenommen. Der farbliche Hintergrund kennzeichnet einzelne
Genre-"Länder" die automatisch erkannt werden - diese haben keine tiefere
Bedeutung.


**Plotting Vorgang:** Das Plotting selbst wird durch GraphViz (TODO: link)
erledigt. Als Eingabe nimmt GraphViz eine textuelle Beschreibung des Graphen die
von einem Python-Script erstellt wird. 

.. figtable::
   :spec: l l l
   :label: Referenz der Detailstufen

    +----------------------------+------------------+------------------------+
    | **Abbildung**              |  **Detailstufe** |  **Anzahl** der Knoten |
    +============================+==================+========================+
    | :num:`fig-genre-graph-min` | *0.5*            |  2197                  |
    +----------------------------+------------------+------------------------+
    | :num:`fig-genre-graph-mid` | *0.1*            |  483                   |
    +----------------------------+------------------+------------------------+
    | :num:`fig-genre-graph-big` | *0.0*            |  39                    |
    +----------------------------+------------------+------------------------+

.. code-block:: bash

    $ cd libmunin_git_clone/
    $ python munin/provider/genre.py --cli --plot 0.0  # Detailstufe. Hier: Voll.
    $ sfdp /tmp/genre.graph | \                        # Layoutting
      gvmap -e | \                                     # Landkarte einzeichnen
      neato -n2 -Ecolor="#55555555" -Tpdf \            # Rendern
      > graph.pdf                                      # In <graph.png> schreiben
    $ pdf-viewer graph.pdf                             # Resultat anschauen

.. only:: latex
   
   **Zoombare Version:** In gedruckter Form sind die Plots nur schwer abzudrucken. 
   Unter TODO:link können die Plots in zoombarer SVG-Version angesehen werden.


.. _fig-genre-graph-min:

.. figure:: figs/genre_graph_min.*
   :alt: xxx
   :width: 100%
   :align: center

   Minimale Version.

.. _fig-genre-graph-mid:

.. figure:: figs/genre_graph_mid.*
   :alt: xxx
   :width: 100%
   :align: center

   Mittlere Version.


.. _fig-genre-graph-big:

.. figure:: figs/genre_graph_big.*
   :alt: xxx
   :width: 100%
   :align: center

   Riesige Version.


.. only:: latex

   .. raw:: latex

       \newpage

.. _end-of-doc:
