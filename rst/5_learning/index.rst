#################
Implizites Lernen
#################

Assoziationsregeln...

.. math::

    Rating(A, B) = (1.0 - Kulczynski(A, B)) \cdot ImbalanceRatio(A, B)

*wobei:* |hfill| *Aussagekraft:*
             
    * :math:`Kulczynski(A, B) =  \frac{p(A \vert B) + p(B \vert A)}{2}` |hfill| Güte der Regel
    * :math:`ImbalanceRatio(A, B) = \frac{\vert support(A) - support(B) \vert}{support(A) + support(B) - support(A \cup B)}` |hfill| Gleichmäßigkeit der Regel
    * :math:`support(X) = H_n(X)` |hfill|  Absolute Häufigkeit von X in allen Transaktionen

Mehr dazu in der Bachelorarbeit.    

*Vergleiche zudem:* :cite:`datamining-concepts-and-techniques` Datamining
Concepts and Techniques.


Generierung von Regeln
======================


Frequent Itemsets
------------------


Ableitung von Regeln aus Frequent Itemsets
------------------------------------------

Apriori kurz anreißen -> langsam.


RELIM
-----


Anwenden von Regeln
====================
