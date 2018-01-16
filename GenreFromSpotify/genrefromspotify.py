import logging
import psycopg2
import requests
from Spotify import constants
from Spotify.oauthtool import implicit_flow


def _authorize():
    # Start OAuth2 implicit flow
    auth_response = implicit_flow(constants.authorizeUrl, constants.clientId)

    # Check if authorization was successful
    if "error" in auth_response and auth_response["error"] is not None:
        logging.error("Authentication failed. Error message: {0}".format(auth_response["error_description"]))
        return False

    return auth_response["access_token"]


success = 0
failure = 0
songid_genre = {}

# access_token = _authorize()
access_token = "BQA_7kAxMLKYHRW73K4JC_L0CP5GsgvSmqCdwKFEnwd49pXje4erZAcDRv25KFNTxdFAD3ESc8QmXEa-cofoFCzi7cs6KJw0s9Oxl-FTcQwNg3VEdq1Ogt3_jVEYf3fOSvppZ5jHEw"

authorization_request_param = {"access_token": access_token}

conn = psycopg2.connect(dbname="reactivejukebox", user="postgres", password="password", host="localhost", port="5432")

cur = conn.cursor()
cur.execute("SELECT name FROM genre")

genres = []
var = cur.fetchone()
while var:
    genres.append(var[0])
    var = cur.fetchone()

cur.close()

cur = conn.cursor()
cur.execute(
    "SELECT song.id,song.spotifyid "
    "FROM song "
    "FULL OUTER JOIN song_genre ON song.id=song_genre.songid "
    "WHERE song_genre.genreid IS NULL AND song.spotifyid != '0' "
    "ORDER BY song.id;")

var = cur.fetchone()
count = 0
list20 = []
current = ""
while var and count < 20:
    if count > 0:
        current = current + ","
    current = current + var[1]
    count += 1
    if count == 20:
        list20.append(current)
        current = ""
        count = 0
    var = cur.fetchone()

for l in list20:
    track_request_param = {"access_token": access_token,
                           "ids": l}
    track_request = requests.get(constants.spotifyBaseUrl + "/tracks",
                                 params=track_request_param)
    track_data = track_request.json()

    artist_list = ""
    for t in track_data['tracks']:
        artist_list = artist_list + t['artists'][0]['id'] + ","
    artist_list = artist_list[:-1]

    artist_request_param = {"access_token": access_token,
                            "ids": artist_list}
    artist_request = requests.get(constants.spotifyBaseUrl + "/artists",
                                  params=artist_request_param)
    artist_data = artist_request.json()

    for idx, a in enumerate(artist_data['artists']):
        g = [x.strip().lower() for x in a['genres']]
        g = [gen for gen in g if gen in genres]
        if len(g) != 0:
            songid_genre[track_data['tracks'][idx]['id']] = g
            success += 1
        else:
            failure += 1

print("Dictionary: ")
print(songid_genre)
print("Success: ")
print(success)
print("Failure: ")
print(failure)

cur.close()
conn.close()

out = open("85more_genres.sql", "w")
out.write("\connect reactivejukebox\n\n")
out.write("PREPARE fill_song_genre AS\nINSERT INTO song_genre (songid, genreid)\nSELECT song.id, genre.id\nFROM song, genre\nWHERE song.spotifyid = $1 AND genre.name = $2;\n\n")

for track_spotify_id in songid_genre:
    for genre_name in songid_genre[track_spotify_id]:
        out.write("EXECUTE fill_song_genre ('" + track_spotify_id +"', '" + genre_name + "');\n")

out.close()
