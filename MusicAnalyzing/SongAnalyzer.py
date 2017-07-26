#!/usr/bin/env python3

#sudo apt-get install python-dev
#pip install librosa
#pip install scikits.samplerate

#remove f13dbd1ccb62e9262979f2763488d6be8882507c5fee47a45c64981005ec2289.mp3 from songs (broken)

from __future__ import print_function

import sys
import librosa
import numpy as np
import os
import csv
import time

import Dynamics

#mode="bpm"
mode="dynamics"


def beat_track(y,sr):
    # Use a default hop size of 512 samples @ 22KHz ~= 23ms
    hop_length = 512 # This is the window length used by default in stft
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr, hop_length=hop_length, start_bpm=120.0, tightness=100, trim=True)
    #see documentation https://librosa.github.io/librosa/generated/librosa.beat.beat_track.html

    return tempo

if __name__ == '__main__':
    starttime=time.time()

    songbasepath="/media/fisch/HDD/Uni/PG/Musik PG"
    hashdirs=['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']


    out = open(mode+".csv", "w" )
    csv_out = csv.writer(out, delimiter=',')
    csv_out.writerow(('songHash',mode))

    files=[] #list of all songnames,  /3/d/d1e05fde310a963b31ade7adc49fce50a9c78bdbd6be7ab677f7636d626fe7.mp3 -> 3dd1e05fde310a963b31ade7adc49fce50a9c78bdbd6be7ab677f7636d626fe7.mp3
    for d1 in hashdirs:
        for d2 in hashdirs:
            _songpath=songbasepath+"/"+d1+"/"+d2+"/" #current songpath
            #print("Path:"+_songpath)
            _files=os.listdir(_songpath)
            #print("Files:"+str(_files))
            files+=[str(d1)+str(d2)+x for x in _files] #append first two hash chars to each filename

    #print(files)


    #files=files[0:1] #use only a part of all files


    for ifile,filename in enumerate(files):
        filename_absolute=songbasepath+"/"+filename[0]+"/"+filename[1]+"/"+filename[2:]
        songHash=filename[0:-4] #remove .mp3 to get song hash

        print(str(ifile)+"/"+str(len(files))+":"+filename)

        #load file
        #y, sr = librosa.load(input_file, sr=22050)
        y, sr = librosa.load(filename_absolute,sr=44100)


        if mode=="bpm":
        #### BPM ####
            bpm=beat_track(y,sr) #analyze bpm
            print("  BPM="+str(bpm))
            csv_out.writerow((songHash, bpm)) #write row to csv

        elif mode=="dynamics":
        #### Dynamics ####
            dyn=Dynamics.dynamics(y,sr) #analyze dynamics
            print("  Dyn="+str(dyn))
            csv_out.writerow((songHash, dyn)) #write row to csv




        timeRemaining=((time.time()-starttime)/(ifile+1) * len(files) - (time.time()-starttime) )
        print("  Remaining Time:"+str(round(timeRemaining/60))+"m"+str(round(timeRemaining%60))+"s")

    print('done!')
