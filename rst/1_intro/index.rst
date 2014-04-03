***********
Überleitung
***********

Das allgemeine Problem
======================

Musik ist nur schwer vergleichbar. Fragt man mehrere Menschen *wie ähnlich* ein
Musikstück zu einem anderem ist, so erhält man genauso viele Antworten wie man
Fragen gestellt hat. Die Einschätzung von Musik ist eine sehr subjektive
Angelegenheit die selbst für Menschen schwierig ist. Stuft man die *Rolling
Stones* als *Rock* ein? Oder doch eher als *Pop?* Was zählt eigentlich noch als
*Rock*?

Wenn man jetzt noch versucht einem Computer dem Begriff der *Musikähnlichkeit*
beizubringen wird es kompliziert. Dieser kann nur objektiv nach bestimmten
*Metriken* entscheiden. Diese Metriken zu definieren muss dann wiederum die
Aufgabe eines Menschen sein --- also sind auch diese wiederum subjektiv, da sie
die *Vorlieben* des Autors widerspiegeln. Auch können diese Metriken nie für
alle Fälle funktionieren. 

Das konkrete Problem
====================

So gesehen, ist *libmunin* in der *,,Standardeinstellung"* ein
Musikempfehlungssystem, das genau auf einen Nutzer und dessen Vorlieben
zugeschnitten ist. Entwickler können jedoch die Bibliothek an ihre Präferenzen
anpassen oder ihren Nutzern eine Möglichkeit geben selbst Einstellungen
vorzunehmen. So wäre es im praktischen Einsatz möglich die Gewichtung einzelner
Attribute während der Laufzeit zu ändern.

Damit die Bibliotheksanwender diese Anpassungen vornehmen können, sollten sie
verstehen was intern vor sich geht.  Darum soll es in dieser Arbeit gehen.
Insbesondere wird auf die wichtigsten Provider und deren Funktionalität
eingegangen, wie diese sich auf die Distanzfunktionen auswirken und wie aus den
einzelnen Distanzen der komplette Graph aufgebaut wird. Zudem wird auf die
Lernfähigkeiten von *libmunin* eingegangen und die von *libmunin* generierten
Empfehlungen werden näher betrachtet.
