import psycopg2
import csv

# Hopefully no song will be called like this ;)
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

file_in = open("data.csv", "r")
data = csv.reader(file_in)
next(data)      # skip first line containing headlines for each column
for row in data:        # row has the structure: [title, artist, album, songHash, length]
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

    cur.execute("EXECUTE insert_artist (%s, %s)", (artistNorm, row[1]))
    artistid = cur.fetchone()[0]
    cur.execute("EXECUTE insert_album (%s, %s)", (albumNorm, row[2]))
    albumid = cur.fetchone()[0]
    cur.execute("EXECUTE connect_artist_album (%s, %s)", (artistid, albumid))
    cur.execute("EXECUTE insert_song (%s, %s, %s, %s, %s)", (titleNorm, row[0], albumid, row[3], int(row[4])))
    songid = cur.fetchone()[0]
    cur.execute("EXECUTE connect_song_artist (%s, %s)", (artistid, songid))

conn.commit()
cur.close()
conn.close()

file_in.close()
