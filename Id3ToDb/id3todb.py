#!/usr/bin/env python3

import os

from mutagen.easyid3 import EasyID3
import mutagen
import psycopg2


def normalize_name(name: str):
    before = name
    name = name.replace(" ", "")
    name = name.lower()
    name = name.replace("ö", "o")
    name = name.replace("ü", "u")
    name = name.replace("ä", "a")
    name = name.replace("ß", "s")
    name = ''.join(e for e in name if e.isalnum())
    if name == '':
        return before
    return name


def normalize_name_list(name_list):
    out = []
    for n in name_list:
        out.append(normalize_name(n))
    return out


'''
length = 712
songHash = "1fe947ed67106b6ab0a0d4b0a2b50aa81b431d92bc5936a52d15d6e6fa1aaf42"
title = "Das Kleinste Glück"
titleNorm = "daskleinstegluck"
artist = "Bosse"
artistNorm = "bosse"
album = "Kamikazeherz"
albumNorm = "kamikazeherz"
'''

conn = psycopg2.connect(dbname="reactivejukebox", user="postgres", password="password", host="localhost", port="5432")
cur = conn.cursor()

# empty the database
cur.execute("TRUNCATE TABLE album CASCADE; TRUNCATE TABLE artist CASCADE; TRUNCATE TABLE song CASCADE;")

# insert artist
cur.execute("PREPARE insert_artist AS "
            "INSERT INTO artist (NameNormalized, Name) "
            "VALUES ($1,$2) "
            "ON CONFLICT (NameNormalized) DO UPDATE SET NameNormalized = EXCLUDED.NameNormalized "
            "RETURNING Id;")

# insert album
cur.execute("PREPARE insert_album AS "
            "INSERT INTO album (TitleNormalized, Title) "
            "VALUES ($1,$2) "
            "ON CONFLICT (TitleNormalized) DO UPDATE SET TitleNormalized = EXCLUDED.TitleNormalized "
            "RETURNING Id;")

# connect artist and album
cur.execute("PREPARE connect_artist_album AS "
            "INSERT INTO album_artist (ArtistId, AlbumId) "
            "VALUES ($1, $2) "
            "ON CONFLICT (ArtistId, AlbumId) DO NOTHING;")

# insert song and connect it to album
cur.execute("PREPARE insert_song AS "
            "INSERT INTO song (TitleNormalized, Title, AlbumId, Hash, Duration) "
            "VALUES ($1,$2,$3,$4,$5) "
            "ON CONFLICT (TitleNormalized) DO UPDATE SET TitleNormalized = EXCLUDED.TitleNormalized "
            "RETURNING Id;")

# connect song and artist
cur.execute("PREPARE connect_song_artist AS "
            "INSERT INTO song_artist (ArtistId, SongId) "
            "VALUES ($1, $2) "
            "ON CONFLICT (ArtistId, SongId) DO NOTHING;")

chars = "0123456789abcdef"

for i in chars:
    if not os.path.isdir("./" + i):
        continue
    for j in chars:
        if not os.path.isdir("./" + i + "/" + j):
            continue
        for file in os.listdir("./" + i + "/" + j):
            audio = EasyID3("./" + i + "/" + j + "/" + file)
            length = int(mutagen.File("./" + i + "/" + j + "/" + file).info.length)
            songHash = (i + j + file)[:-4]
            title = audio["title"][0]
            titleNorm = normalize_name(title)
            artist = audio["artist"]
            artistNorm = normalize_name_list(artist)
            album = audio["album"][0]
            albumNorm = normalize_name(album)

            cur.execute("EXECUTE insert_artist (%s, %s)", (artistNorm, artist))
            artistid = cur.fetchone()[0]
            cur.execute("EXECUTE insert_album (%s, %s)", (albumNorm, album))
            albumid = cur.fetchone()[0]
            cur.execute("EXECUTE connect_artist_album (%s, %s)", (artistid, albumid))
            cur.execute("EXECUTE insert_song (%s, %s, %s, %s, %s)", (titleNorm, title, albumid, songHash, length))
            songid = cur.fetchone()[0]
            cur.execute("EXECUTE connect_song_artist (%s, %s)", (artistid, songid))

conn.commit()
cur.close()
conn.close()
