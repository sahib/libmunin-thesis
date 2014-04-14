***********
Überleitung
***********

Das allgemeine Problem
======================

:dropcaps:`Musik` ist nur schwer vergleichbar. Fragt man mehrere Menschen wie
*ähnlich* ein Musikstück zu einem anderem ist, so erhält man genauso viele
Antworten wie man Fragen gestellt hat. Die Einschätzung von Musik ist eine sehr
subjektive Angelegenheit, die auch häufig zwischen Menschen Diskussionen
auslöst.  Stuft man die *Rolling Stones* als *Rock* ein? Oder doch eher als
*Pop?* Was zählt überhaupt noch als *Rock*? Gibt es eine Definition dafür?

Wenn man jetzt noch versucht einem Computer dem Begriff der *Musikähnlichkeit*
beizubringen wird es kompliziert. Dieser kann nur objektiv nach bestimmten
*Metriken* entscheiden. Diese Metriken zu definieren, muss dann wiederum die
Aufgabe eines Menschen sein --- also sind auch diese wiederum subjektiv, da sie
die *Vorlieben* des Autors widerspiegeln. Auch können diese Metriken nie für
alle Fälle funktionieren. Ein gutes Stück *,,Kaffeesatzleserei"* lässt sich
leider nie ganz vermeiden.

Das konkrete Problem
====================

So gesehen, ist *libmunin* in der *,,Standardeinstellung"* ein
Musikempfehlungssystem, das genau auf einen Nutzer und dessen Vorlieben
zugeschnitten ist: Seinem Entwickler. Bibliotheksanwender können jedoch die
Bibliothek an ihre Präferenzen anpassen oder ihren Endnutzern eine Möglichkeit
geben, selbst Einstellungen vorzunehmen. So könnte man im praktischen Einsatz
die Gewichtung einzelner Attribute während der Laufzeit zu ändern.

Damit die Bibliotheksanwender diese Anpassungen vornehmen können, sollten sie
verstehen was intern vor sich geht. Genau darum soll es in dieser Arbeit gehen.
Es wird insbesondere auf die wichtigsten Provider und deren Funktionalität
eingegangen, wie diese sich auf die Distanzfunktionen auswirken und wie aus den
einzelnen Distanzen der komplette Graph aufgebaut wird. Zudem wird auf die
Lernfähigkeiten von *libmunin* eingegangen und die generierten Empfehlungen
werden näher betrachtet. Zu jedem vorgestellten Thema werden auch Überlegungen
angestellt, welche Verbesserungen in zukünftigen Versionen gemacht werden
können.
