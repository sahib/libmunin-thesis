*********
Hauptteil
*********

Implementierung
===============

Sehr kompliziert:

.. code-block:: python

    def hello(world):
        print(world)

    if __name__ == '__main__':
        hello('Na' * 10 + ' Batman!')


Architektur
===========

.. architektur diagramm

Maske
-----

- Beschreibung der Musikdatenbank die von außen reinkommt.
- Besteht aus einem Mapping, bei dem die keys den Namen eines Attributes
  festlegt das ein einzelner Song haben wird, das zugehörige Value legt
  den dafür zuständigen Provider, die zuständige Distanzfunktion und 
  wie stark dieses Attribut des Songs gewichtet werden soll.

.. code-block:: python

   {
    'genre': (provider, distance_func, weight)
   }

Session
-------

- API Entry für alle Funktionen
- Speichert songs ab
- Speichert die Maske

Song
----

- Speichert nur values, keine

Distance
--------

- Speichert alle Teildistanzen, statt einzelne weighted Distanz.
- Macht 'explanations' leicht.


Kurze Implementierungshistorie
==============================

Probleme:

    - Graphenaufbau (combinations = teuer) 
    - Festlegung von distance_add funktionsweise

Graphenoperationen
==================

genaue beschreibungen in bachelorarbeit.

add
---

insert
------

remove
------

modify
------

rebuild
-------

fix
---

Ausstellen von Recommendations
==============================

Sieben von Recomemndations
==========================

Lernen durch die History
========================

Keywordextraction
=================
