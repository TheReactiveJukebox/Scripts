import csv
import logging
import os
import numpy as np

import constants
import requests
import sys
from oauthtool import implicit_flow

range_from = 9364
range_to = 100000000

def _authorize():
    # Start OAuth2 implicit flow
    auth_response = implicit_flow(constants.authorizeUrl, constants.clientId)

    # Check if authorization was successful
    if "error" in auth_response and auth_response["error"] is not None:
        logging.error("Authentication failed. Error message: {0}".format(auth_response["error_description"]))
        return False

    return auth_response["access_token"]


delete_not_found = False

if delete_not_found:
    path = sys.argv[2]

#access_token = _authorize() #comment in, if new token needed.
#print(access_token) #           ""
#exit()  #                      ""
access_token = "123"

csv_outfile = open("spotifydata.csv" + "_" + str(range_from) + "to" + str(range_to), "w", encoding="utf-8", newline="")
csv_out = csv.writer(csv_outfile, delimiter=',')

infile = sys.argv[1] #lastfmdata.csv

csv_infile = open(infile, "r", encoding="utf-8") #lastfmdata.csv
csv_in = csv.reader(csv_infile, delimiter=',')

csvspotifyumlautbug_infile = open("Spotify/spotifydata.csv_umlautbug", "r", encoding="utf-8") #umlautbugfix
csvspotifyumlautbug_in = csv.reader(csvspotifyumlautbug_infile, delimiter=',') #umlautbugfix
existingspotifydata=[ x for x in csvspotifyumlautbug_in] #umlautbugfix  lines to array
existingspotifydata=np.array(existingspotifydata) #umlautbugfix

not_found_counter = 0

for rownum, row in enumerate(csv_in):
    if rownum == 0:  # header
        csv_out.writerow(('title', 'artist', 'album', 'songHash', 'length', 'published', 'trackmbid', 'artistmbid',
                          'albummbid', 'playcount', 'listeners', 'albumcover', 'genres', 'artistrating', 'trackrating',
                          'bpm', 'danceability', 'energy', 'loudness', 'speechiness', 'acousticness',
                          'instrumentalness', 'liveness', 'valence', 'spotifyurl', 'spotifyid'))
        continue  # next row
    elif rownum < range_from or rownum > range_to:
        continue


    ##  UMLAUTBUGFIX  skip songs which are already in existing spotifydata.csv and copy that line to new file
    existingdata_indexfound=-1  #umlautbugfix
    for edi,ed in enumerate(existingspotifydata[:,0:3]):  #umlautbugfix
        exisintdatalinematch= (ed==row[0:3])  #umlautbugfix
        if (np.all(exisintdatalinematch)): #current index is line with this data  #umlautbugfix
            existingdata_indexfound=edi  #umlautbugfix

    efd=existingspotifydata #shorten vairabled  #umlautbugfix
    efdi=existingdata_indexfound #shorten variabled  #umlautbugfix

    if existingdata_indexfound>0: #line exists in spotifydata   #umlautbugfix
        csv_out.writerow((row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7],
                          row[8], row[9], row[10], row[11], row[12], row[13], row[14],
                          efd[efdi][15], efd[efdi][16],efd[efdi][17],
                          efd[efdi][18], efd[efdi][19], efd[efdi][20],
                          efd[efdi][21], efd[efdi][22], efd[efdi][23],
                          efd[efdi][24], efd[efdi][25]))  #umlautbugfix
        continue #skip to next song   #umlautbugfix

    ##  UMLAUTBUGFIX ENDE

    search_request_param = {"access_token": access_token,
                            "q": row[0] + " " + row[1],
                            "type": "track",
                            "limit": 1}

    # Strangely, the Spotify API sometimes returns a 502 without any obvious reason, so in this case just try again
    while True:
        search_request = requests.get(constants.spotifyBaseUrl + "/search",
                                      params=search_request_param)
        search_data = search_request.json()

        if "tracks" in search_data:
            break

        print("An error occurred, further information below:")
        print("search_data: ")
        print(search_data)
        print("search_request: ")
        print(search_request)
        print("search_request_param: ")
        print(search_request_param)

    if len(search_data["tracks"]["items"]) == 0: #song not found at spotify
        not_found_counter += 1
        if delete_not_found:
            try:
                os.remove(path + "/" + row[3][:1] + "/" + row[3][1:2] + "/" + row[3][2:] + ".mp3")
            except:
                print("File not found: " + path + "/" + row[3][:1] + "/" + row[3][1:2] + "/" + row[3][2:] + ".mp3")
        else:
            csv_out.writerow((row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7],
                              row[8], row[9], row[10], row[11], row[12], row[13], row[14],
                              0, 0, 0, 0, 0, 0, 0, 0, 0,0,0))
    else: #song found at spotify
        track_id = search_data["tracks"]["items"][0]["id"]
        feature_request_param = {"access_token": access_token}

        while True:
            feature_request = requests.get(constants.spotifyBaseUrl + "/audio-features/" + track_id,
                                           params=feature_request_param)
            feature_data = feature_request.json()

            if "tempo" in feature_data:
                break

            print("An error occurred, further information below:")
            print("feature_request: ")
            print(feature_request)
            print("feature_data: ")
            print(feature_data)
            print("track_id: ")
            print(track_id)
            print("search_request_param: ")
            print(search_request_param)

        csv_out.writerow((row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7],
                          row[8], row[9], row[10], row[11], row[12], row[13], row[14],
                          feature_data["tempo"], feature_data["danceability"], feature_data["energy"],
                          feature_data["loudness"], feature_data["speechiness"], feature_data["acousticness"],
                          feature_data["instrumentalness"], feature_data["liveness"], feature_data["valence"],
                          search_data["tracks"]["items"][0]["preview_url"], search_data["tracks"]["items"][0]["id"]))
print(not_found_counter)
