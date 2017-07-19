from datetime import date, datetime

import psycopg2
import csv

# Hopefully no song will be called like this ;)
import re

SKIP = "1c73b71e7e1364f2eda6007749a93fe9dc90b844b27a121de985e78b1aa3aa82"


def normalize_name(name: str):
    name = name.replace(" ", "")
    name = name.lower()
    name = name.replace("ö", "o")
    name = name.replace("ü", "u")
    name = name.replace("ä", "a")
    name = name.replace("ß", "s")
    name = ''.join(e for e in name if ord(e) < 128)  # Non-ASCII-Characters should not be included in normalized name
    name = ''.join(e for e in name if e.isalnum())  # Remove all special characters
    if name == '':  # If no normalized name remains, e.g. with '...', don't include the entry in the database
        return SKIP
    return name


def normalize_name_list(name_list):
    out = []
    for n in name_list:
        out.append(normalize_name(n))
    return out


conn = psycopg2.connect(dbname="reactivejukebox", user="postgres", password="password", host="localhost", port="5432")
cur = conn.cursor()

# empty the database
cur.execute("TRUNCATE TABLE album CASCADE; TRUNCATE TABLE artist CASCADE; TRUNCATE TABLE song CASCADE; TRUNCATE TABLE genre CASCADE;")

# insert artist
cur.execute("PREPARE insert_artist AS "
            "INSERT INTO artist (NameNormalized, Name, MusicBrainzId, Rating) "
            "VALUES ($1, $2, $3, $4) "
            "ON CONFLICT (NameNormalized) DO UPDATE SET NameNormalized = EXCLUDED.NameNormalized "
            "RETURNING Id;")

# insert album
cur.execute("PREPARE insert_album AS "
            "INSERT INTO album (TitleNormalized, Title, Cover, MusicBrainzId) "
            "VALUES ($1, $2, $3, $4) "
            "ON CONFLICT (TitleNormalized) DO UPDATE SET TitleNormalized = EXCLUDED.TitleNormalized "
            "RETURNING Id;")

# connect artist and album
cur.execute("PREPARE connect_artist_album AS "
            "INSERT INTO album_artist (ArtistId, AlbumId) "
            "VALUES ($1, $2) "
            "ON CONFLICT (ArtistId, AlbumId) DO NOTHING;")

# insert song and connect it to album
cur.execute("PREPARE insert_song AS "
            "INSERT INTO song (TitleNormalized, Title, AlbumId, Hash, Duration, Published, MusicBrainzId, Playcount, Listeners) "
            "VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9) "
            "ON CONFLICT (TitleNormalized) DO UPDATE SET TitleNormalized = EXCLUDED.TitleNormalized "
            "RETURNING Id;")

# connect song and artist
cur.execute("PREPARE connect_song_artist AS "
            "INSERT INTO song_artist (ArtistId, SongId) "
            "VALUES ($1, $2) "
            "ON CONFLICT (ArtistId, SongId) DO NOTHING;")

# insert genre
cur.execute("PREPARE insert_genre AS "
            "INSERT INTO genre (Id, Name) "
            "VALUES ($1, $2) "
            "RETURNING Id;")

# connect song and genre
cur.execute("PREPARE connect_song_genre AS "
            "INSERT INTO song_genre (SongId, GenreId) "
            "VALUES ($1, $2) "
            "ON CONFLICT (SongId, GenreId) DO NOTHING;")

genres = {}
genre_in = open("genres.csv", "r")
genre_data = csv.reader(genre_in)
i = 1
for row in genre_data:
    genres[row[0]] = i
    cur.execute("EXECUTE insert_genre (%s, %s)", (i, row[0]))
    i += 1
genre_in.close()

file_in = open("data.csv", "r", encoding="utf-8")
data = csv.reader(file_in)
next(data)  # skip first line containing headlines for each column
for row in data:
    # row has the structure:
    # [0title, 1artist, 2album, 3songHash, 4length, 5published, 6trackmbid,
    #  7artistmbid, 8albummbid, 9playcount, 10listeners, 11albumcover, 12genres, 13rating]
    titleNorm = normalize_name(row[0])
    if titleNorm == SKIP:
        print(("Title skipped:", row[0], titleNorm))
        continue
    artistNorm = normalize_name(row[1])
    if SKIP in artistNorm:
        print(("Artist skipped:", row[1], artistNorm))
        continue
    albumNorm = normalize_name(row[2])
    if albumNorm == SKIP:
        print(("Album skipped:", row[2], albumNorm))
        continue

    rating = 0 if row[13] is "" else float(row[13])
    cur.execute("EXECUTE insert_artist (%s, %s, %s, %s)", (artistNorm, row[1], row[7], rating))
    artistid = cur.fetchone()[0]
    cur.execute("EXECUTE insert_album (%s, %s, %s, %s)", (albumNorm, row[2], row[11], row[8]))
    albumid = cur.fetchone()[0]
    cur.execute("EXECUTE connect_artist_album (%s, %s)", (artistid, albumid))
    if re.compile("\d*-\d*-\d*").match(row[5]):
        release_date = datetime.strptime(row[5], "%Y-%m-%d")
    elif re.compile("\d*-\d*").match(row[5]):
        release_date = datetime.strptime(row[5], "%Y-%m")
    elif row[5] is not "":
        release_date = datetime.strptime(row[5], "%Y")
    else:
        release_date = None
    cur.execute("EXECUTE insert_song (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (titleNorm, row[0], albumid, row[3], int(row[4]), release_date, row[6], int(row[9]), int(row[10])))
    songid = cur.fetchone()[0]
    cur.execute("EXECUTE connect_song_artist (%s, %s)", (artistid, songid))
    genList = row[12].replace("'", "")
    genList = genList.replace("[", "")
    genList = genList.replace("]", "")
    genList = genList.split(",")
    for gen in genList:
        if gen in genres:
            cur.execute("EXECUTE connect_song_genre (%s, %s)", (songid, genres[gen]))

conn.commit()
cur.close()
conn.close()

file_in.close()
