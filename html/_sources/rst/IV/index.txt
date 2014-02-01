***************
Implementierung
***************

Übersicht
=========

::

    munin/
    |---- __init__.py                     # Version Info
    |---- __main__.py                     # Contains an example program
    |---- database.py                     # Implements all TODO
    |---- dbus_client.py
    |---- dbus_service.py
    |---- distance/
    |   |---- __init__.py
    |   |---- bpm.py
    |   |---- date.py
    |   |---- genre.py
    |   |---- keywords.py
    |   |---- levenshtein.py
    |   |---- moodbar.py
    |   |---- rating.py
    |   |---- wordlist.py
    |---- easy.py
    |---- graph.py
    |---- helper.py
    |---- history.py
    |---- plot.py
    |---- provider/
    |   |---- __init__.py
    |   |---- bpm.py
    |   |---- composite.py
    |   |---- date.py
    |   |---- generate_genre_list.py
    |   |---- genre.list
    |   |---- genre.py
    |   |---- keywords.py
    |   |---- moodbar.py
    |   |---- normalize.py
    |   |---- stem.py
    |   |---- wordlist.py
    |---- rake.py
    |---- scripts/
    |   |---- moodbar_visualizer.py
    |   |---- moodbar_walk.py
    |---- session.py
    |---- song.py
    |---- stopwords/                     # Stopword supoort
    |   |---- data                       # Stopworddatabase 
    |   |   |---- de                     # Each file contains a newline separated
    |   |   |---- en                     # list of stopwords. 
    |   |   |---- es                     # File name is the ISO 638-1 language code.
    |   |   |---- …
    |   |---- __init__.py
    |---- testing.py

    5 directories, 57 files
    

Historie
========

Putting it together
===================

.. code-block:: python
    :linenos:
    :emphasize-lines: 1,3,11,12,14,21

    from munin.easy import EasySession

    MY_DATABASE = [
        # Artist:            Album:               Title:             Genre:
        ('Akrea'          , 'Lebenslinie'      , 'Trugbild'       , 'death metal'),
        ('Vogelfrey'      , 'Wiegenfest'       , 'Heldentod'      , 'folk metal'),
        ('Letzte Instanz' , 'Götter auf Abruf' , 'Salve te'       , 'folk rock'),
        ('Debauchery'     , 'Continue to Kill' , 'Apostle of War' , 'brutal death')
    ]

    session = EasySession()
    with session.transaction():
        for idx, (artist, album, title, genre) in enumerate(MY_DATABASE):
             session.mapping[session.add({
                 'artist': artist,
                 'album': album,
                 'title': title,
                 'genre': genre
             })] = idx

    for munin_song in session.recommend_from_seed(session[0], 2):
        print(MY_DATABASE[munin_song.uid])


The output of this little wonder should be:

.. code-block:: python

    ('Vogelfrey'  , 'Wiegenfest'       , 'Heldentod'      , 'folk metal'),
    ('Debauchery' , 'Continue to Kill' , 'Apostle of War' , 'brutal death')

