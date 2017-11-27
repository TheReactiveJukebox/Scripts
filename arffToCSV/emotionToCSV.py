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

arousalmin=0
arousalmax=100
arousalmin_translated=0
arousalmax_translated=1

valencemin=0
valencemax=100
valencemin_translated=0
valencemax_translated=1


def printStatistics(datalist):
    print('max='+str(max(datalist)))
    print('min='+str(min(datalist)))
    print('mean='+str(max(datalist)))
    print('q 0.25='+str(np.percentile(datalist,25)))
    print('q 0.5='+str(np.percentile(datalist,50)))
    print('q 0.75='+str(np.percentile(datalist,75)))

def translate(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)

hashdirs=[x[0] for x in os.walk(directory)] #list of all directories in directory

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
            valence=translate(arffvalence, valencemin, valencemax, valencemin_translated, valencemax_translated)
            outfile.write(songhash + ',' + str(arousal) + ',' + str(valence) + '\n')


print('')
print('Statistics Arousal:')
printStatistics(allarousal)
print('')
print('Statistics Valence:')
printStatistics(allvalence)
