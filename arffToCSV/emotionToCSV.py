#!/usr/bin/env python3

import csv
import os
import sys
import numpy as np

#python3 emotiontocsv.py ./Extraction emotions.csv

if len(sys.argv)<3:
    print('Error: Missing parameters!')
    print('Usage: emotiontocsv.py directoryToARFFs output.csv')
    exit()

directory=sys.argv[1] #'./Test100/'
csvoutpath=sys.argv[2] #'emotions.csv'

allarousal=[]
allvalence=[]

arousalmin=10
arousalmax=20
arousalmin_translated=-1
arousalmax_translated=1

valencemin=4.5
valencemax=9
valencemin_translated=-1
valencemax_translated=1


def printStatistics(datalist):
    print('max='+str(max(datalist)))
    print('min='+str(min(datalist)))
    print('mean='+str(np.mean(datalist)))
    percentiles=[0.01,0.05,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.95,0.99]
    for q in percentiles:
        print('q '+str(q)+'='+str(np.percentile(datalist, (q*100) )))

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

def translate(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)

hashdirs=[x[0] for x in os.walk(directory)] #list of all directories in directory
hashdirs=hashdirs[1:] #remove first entry, the directory itself

with open(csvoutpath, 'w') as outfile:
    outfile.write('songHash' + ',' + 'arousal' + ',' + 'valence' + '\n')
    for hashdir in hashdirs:
        songhash = hashdir[hashdir.rfind("/")+1:]
        if len(songhash)<10: #skip non hashes
            continue
        arff_emotion_file=hashdir+'/'+songhash+'_700.arff' #miremotion has id 700
        with open(arff_emotion_file, 'r') as emotionfile:
            emotionfile_lines=[x.replace('\n','') for x in emotionfile.readlines()] #line from arff file to list
            data_indices = [i for i, s in enumerate(emotionfile_lines) if '@DATA' in s]
            arffarousal=float(emotionfile_lines[data_indices[0]+1].split(',')[0]) #extract arousal from arff
            arffvalence=float(emotionfile_lines[data_indices[0]+2].split(',')[0]) #extract valence from arff
            '''
            ...
            @DATA       <- at data_indices[0]
            15.234234,1   <- arousal    data_indices[0]+1
            3.22313,2     <- valence    data_indices[0]+2
            ...
            '''
            allarousal.append(arffarousal)
            allvalence.append(arffvalence)
            arousal=translate(arffarousal, arousalmin, arousalmax, arousalmin_translated, arousalmax_translated)
            arousal=clamp(arousal,arousalmin_translated,arousalmax_translated)
            valence=translate(arffvalence, valencemin, valencemax, valencemin_translated, valencemax_translated)
            valence=clamp(valence,valencemin_translated,valencemax_translated)
            outfile.write(songhash + ',' + str(arousal) + ',' + str(valence) + '\n')


print('')
print('Statistics Arousal:')
printStatistics(allarousal)
print('')
print('Statistics Valence:')
printStatistics(allvalence)
