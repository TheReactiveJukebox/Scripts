import csv
import logging
import os

import constants
import requests
import sys
from oauthtool import implicit_flow


def _authorize():
    # Start OAuth2 implicit flow
    auth_response = implicit_flow(constants.authorizeUrl, constants.clientId)

    # Check if authorization was successful
    if "error" in auth_response and auth_response["error"] is not None:
        logging.error("Authentication failed. Error message: {0}".format(auth_response["error_description"]))
        return False

    return auth_response["access_token"]


delete_not_found = True

if delete_not_found:
    path = sys.argv[2]

# access_token = _authorize()
access_token = "123"

csv_outfile = open("spotifydata.csv", "w", encoding="utf-8", newline="")
csv_out = csv.writer(csv_outfile, delimiter=',')

infile = sys.argv[1]

csv_infile = open(infile, "r", encoding="utf-8")
csv_in = csv.reader(csv_infile, delimiter=',')

# bpm_dict = {}
#
# # read bpm from librosa
# with open("bpm_all.csv", "r", encoding="utf-8") as csv_bpmfile:
#     csv_bpm = csv.reader(csv_bpmfile, delimiter=',')
#     for rownum, row in enumerate(csv_bpm):
#         bpm_dict[row[0]] = row[1]

not_found_counter = 0

for rownum, row in enumerate(csv_in):
    if rownum == 0:  # header
        csv_out.writerow(('title', 'artist', 'album', 'songHash', 'length', 'published', 'trackmbid', 'artistmbid',
                          'albummbid', 'playcount', 'listeners', 'albumcover', 'genres', 'artistrating', 'trackrating',
                          'bpm', 'danceability', 'energy', 'loudness', 'speechiness', 'acousticness',
                          'instrumentalness', 'liveness', 'valence', 'spotifyurl', 'spotifyid'))
        continue  # next row

    search_request_param = {"access_token": access_token,
                            "q": row[0] + " " + row[1],
                            "type": "track",
                            "limit": 1}
    search_request = requests.get(constants.spotifyBaseUrl + "/search",
                                  params=search_request_param)
    search_data = search_request.json()

    if len(search_data["tracks"]["items"]) == 0:
        not_found_counter += 1
        if delete_not_found:
            os.remove(path + "/" + row[3][:1] + "/" + row[3][1:2] + "/" + row[3][2:])
        else:
            csv_out.writerow((row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7],
                              row[8], row[9], row[10], row[11], row[12], row[13], row[14],
                              0, 0, 0, 0, 0, 0, 0, 0, 0,0,0))
    else:
        track_id = search_data["tracks"]["items"][0]["id"]
        feature_request_param = {"access_token": access_token}
        feature_request = requests.get(constants.spotifyBaseUrl + "/audio-features/" + track_id,
                                       params=feature_request_param)
        feature_data = feature_request.json()

        # if abs(float(feature_data["tempo"]) - float(bpm_dict[row[3]])) > 20:
        #     print("[1] CSV: " + bpm_dict[row[3]] + "BPM " + row[1] + " - " + row[0])
        #     print("[2] Spt: " + str(feature_data["tempo"]) + "BPM " + search_data["tracks"]["items"][0]["artists"][0]["name"]
        #           + " - " + search_data["tracks"]["items"][0]["name"])

        csv_out.writerow((row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7],
                          row[8], row[9], row[10], row[11], row[12], row[13], row[14],
                          feature_data["tempo"], feature_data["danceability"], feature_data["energy"],
                          feature_data["loudness"], feature_data["speechiness"], feature_data["acousticness"],
                          feature_data["instrumentalness"], feature_data["liveness"], feature_data["valence"],
                          search_data["tracks"]["items"][0]["preview_url"], search_data["tracks"]["items"][0]["id"]))


print(not_found_counter)
