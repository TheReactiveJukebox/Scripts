#!/usr/bin/env python3

# sudo apt-get install python-dev
# pip install librosa
# pip install scikits.samplerate
# sudo apt-get install libav-tools

# manually remove f13dbd1ccb62e9262979f2763488d6be8882507c5fee47a45c64981005ec2289.mp3 from songs (broken)

from __future__ import print_function

import sys
import librosa
import numpy as np
import os
import csv
import time

import Dynamics



# mode="bpm"
# mode = "dynamics"
mode = sys.argv[1].split(',')  #example: "bpm" or "dynamics" or "bpm,dynamics" for both

# songbasepath = "/media/fisch/HDD/Musik PG/"
songbasepath = sys.argv[2]

splitcomputation=''
if len(sys.argv)>=4:
    if len(sys.argv[3])>=3: #argument given
        splitcomputation=sys.argv[3].split('-') #1-4  ->  split in 4, compute part 1. start script with 1-4, 2-4, 3-4 and 4-4 for all files
        splitcomputation[0]=int(splitcomputation[0])
        splitcomputation[1]=int(splitcomputation[1])
        assert splitcomputation[0]>0,'first number has to be >0'
        assert splitcomputation[1]>0,'second number has to be >0'
        assert splitcomputation[0]<=splitcomputation[1],'first number has to be lower or equal the second number'

def beat_track(y, sr):
    # Use a default hop size of 512 samples @ 22KHz ~= 23ms
    hop_length = 512  # This is the window length used by default in stft
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr, hop_length=hop_length, start_bpm=120.0, tightness=100, trim=True)
    # see documentation https://librosa.github.io/librosa/generated/librosa.beat.beat_track.html

    return tempo


if __name__ == '__main__':
    starttime = time.time()

    hashdirs = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']

    partnumber=''
    if splitcomputation!='': #for attaching a csv part number if mulitprocessing enabled
        partnumber='_'+str(splitcomputation[0])

    if 'bpm' in mode:
        out_bpm = open("bpm" + ".csv"+partnumber, "w")
        csv_out_bpm = csv.writer(out_bpm, delimiter=',')
        csv_out_bpm.writerow(('songHash', 'bpm'))

    if 'dynamics' in mode:
        out_dynamics = open("dynamics" + ".csv"+partnumber, "w")
        csv_out_dynamics = csv.writer(out_dynamics, delimiter=',')
        csv_out_dynamics.writerow(('songHash', 'dynamics'))

    files = []  # list of all songnames,  /3/d/d1e05fde310a963b31ade7adc49fce50a9c78bdbd6be7ab677f7636d626fe7.mp3 -> 3dd1e05fde310a963b31ade7adc49fce50a9c78bdbd6be7ab677f7636d626fe7.mp3
    for d1 in hashdirs:
        for d2 in hashdirs:
            _songpath = songbasepath + "/" + d1 + "/" + d2 + "/"  # current songpath
            # print("Path:"+_songpath)
            _files = os.listdir(_songpath)
            # print("Files:"+str(_files))
            files += [str(d1) + str(d2) + x for x in _files]  # append first two hash chars to each filename

    #files=files[0:8] #use only a part of all files

    if splitcomputation!='':
        print('splitting files part '+str(splitcomputation[0])+' of '+str(splitcomputation[1]))
        print('number of files:'+str(len(files)))
        _filesperpart=len(files)*1.0/splitcomputation[1]
        files=files[int((splitcomputation[0]-1)*_filesperpart):int(splitcomputation[0]*_filesperpart)]
        print('using files '+str(int((splitcomputation[0]-1)*_filesperpart))+':'+str(int(splitcomputation[0]*_filesperpart)))
        

    for ifile, filename in enumerate(files):
        filename_absolute = songbasepath + "/" + filename[0] + "/" + filename[1] + "/" + filename[2:]
        songHash = filename[0:-4]  # remove .mp3 to get song hash

        print(str(ifile+1) + "/" + str(len(files)) + ":" + filename)

        # load file
        # y, sr = librosa.load(input_file, sr=22050)
        y, sr = librosa.load(filename_absolute, sr=44100)

        if 'bpm' in mode:
            #### BPM ####
            bpm = beat_track(y, sr)  # analyze bpm
            # print("  BPM=" + str(bpm))
            csv_out_bpm.writerow((songHash, bpm))  # write row to csv
            out_bpm.flush()

        if 'dynamics' in mode:
            #### Dynamics ####
            dyn = Dynamics.dynamics(y, sr)  # analyze dynamics
            # print("  Dyn=" + str(dyn))
            csv_out_dynamics.writerow((songHash, dyn))  # write row to csv
            out_dynamics.flush()

        timeRemaining = ((time.time() - starttime) / (ifile + 1) * len(files) - (time.time() - starttime))
        print("  Remaining Time:" + str(round(timeRemaining / 60)) + "m" + str(round(timeRemaining % 60)) + "s")


    if 'bpm' in mode:
        out_bpm.close()

    if 'dynamics' in mode:
        out_dynamics.close()

    print('done!')
