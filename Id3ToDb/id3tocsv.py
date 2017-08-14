import os

from mutagen.easyid3 import EasyID3
import mutagen
import csv
import sys

path = sys.argv[1]

# Hopefully no song will be called like this ;)
SKIP = "1c73b71e7e1364f2eda6007749a93fe9dc90b844b27a121de985e78b1aa3aa82"

out = open("id3data.csv", "w", newline="")
csv_out = csv.writer(out)
csv_out.writerow(("title", "artist", "album", "songHash", "length"))

chars = "0123456789abcdef"

for i in chars:
    if not os.path.isdir(path + "/" + i):
        continue
    for j in chars:
        if not os.path.isdir(path + "/" + i + "/" + j):
            continue
        for file in os.listdir(path + "/" + i + "/" + j):
            audio = EasyID3(path + "/" + i + "/" + j + "/" + file)
            length = int(mutagen.File(path + "/" + i + "/" + j + "/" + file).info.length)
            songHash = (i + j + file)[:-4]
            title = audio["title"][0]
            artist = audio["artist"][0]
            album = audio["album"][0]

            csv_out.writerow((title, artist, album, songHash, length))

out.close()
