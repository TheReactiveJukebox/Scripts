import os

from mutagen.easyid3 import EasyID3
import mutagen
import csv

# Hopefully no song will be called like this ;)
SKIP = "1c73b71e7e1364f2eda6007749a93fe9dc90b844b27a121de985e78b1aa3aa82"

out = open("data.csv", "w", newline="")
csv_out = csv.writer(out)

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
            artist = audio["artist"][0]
            album = audio["album"][0]

            print((title, artist, album, songHash, length))
            csv_out.writerow((title, artist, album, songHash, length))

out.close()
