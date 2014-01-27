******
Design
******

Übersicht
=========

.. figure:: figs/integration.*
    :alt: Integrationsübersicht
    :width: 100%
    :align: center

    Wie integriert sich libmunin in seine Umgebung?

.. figure:: figs/provider_process.*
    :alt: Attributverarbeitung
    :width: 75%
    :align: center

    Ablauf bei der Verarbeitung eines einzelnen Attributes.

Architektur
===========

.. figure:: figs/arch.*
    :alt: Architekturübersicht.
    :width: 100%
    :align: center

    Grobe Übersicht über die architektur.

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
