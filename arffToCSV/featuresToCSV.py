#!/usr/bin/env python3

import csv
import os
import sys
import numpy as np

#python3 featuresToCSV.py ./Extraction features.csv

if len(sys.argv)<3:
    print('Error: Missing parameters!')
    print('Usage: emotiontocsv.py directoryToARFFs output.csv')
    exit()

directory=sys.argv[1] #'./Test100/'
csvoutpath=sys.argv[2] #'features.csv'

def isNumber(number):
    if number=='NaN':
        return False
    try:
        float(number)
        return True
    except ValueError:
        return False

def translate(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)

hashdirs=[x[0] for x in os.walk(directory)] #list of all directories in directory
hashdirs=hashdirs[1:]

featurenames=[
["Zero-crossing rate",0], # Timbre features
["Root mean square",4],
["Low energy",6],
["Tristimulus 2048",20051],
["RMS peak number in 3 seconds",11],
["Spectral irregularity 2048",20029],
#["Spectral bandwidth 2048",20030], #not available
#["Spectral crest factor 2048",20033],
#["Spectral flatness measure 2048",20034],
#["Distances in phase domain 2048",20041],
["CMRARE cepstral modulation features with polynomial order 3",45], #CMRARE
["CMRARE cepstral modulation features with polynomial order 5",46],
["CMRARE cepstral modulation features with polynomial order 10",47],
["Inharmonicity 2048",20053], # Harmony and melody features
["Major/minor alignment 2048",20055],
["Strengths of major keys 2048",20056],
["Strengths of minor keys 2048",20057],
["Harmonic change detection function 2048",20059],
["Spectral brightness 2048",20037],
["Characteristics of fluctuation patterns",410], #Tempo features
["Rhythmic clarity",418],
["Estimated onset number per minute",420]
]
featurenames=np.array(featurenames)  #featurenames[:,0] returns all names


with open(csvoutpath, 'w') as outfile:

    outfile.write('songHash' )
    for currentfeature in featurenames: #for every feature
        feature_name=currentfeature[0]
        outfile.write(',' + feature_name)
    outfile.write('\n')

    for i_hashdir,hashdir in enumerate(hashdirs): #go through all songs
        print(str(i_hashdir)+'/'+str(len(hashdirs))+':'+str(hashdir))
        songhash = hashdir[hashdir.rfind("/")+1:]
        outfile.write(songhash)  #write first column for this song
        if len(songhash)<10: #skip non hashes
            continue
        for currentfeature in featurenames: #for every feature
            feature_name=currentfeature[0]
            feature_id=currentfeature[1]

            arff_file=hashdir+'/'+songhash+'_'+feature_id+'.arff'
            with open(arff_file, 'r') as featurefile:
                featurefile_lines=[x.replace('\n','') for x in featurefile.readlines()] #line from arff file to list
                data_indices = [i for i, s in enumerate(featurefile_lines) if '@DATA' in s]
                featurevalues=[]
                datacount=1 #start at 1
                while data_indices[0]+datacount < len(featurefile_lines):
                    value=featurefile_lines[data_indices[0]+datacount].split(',')[0] #extract data from arff
                    if isNumber(value): #some values can be NaN
                        featurevalues.append(float(value))
                    datacount+=1

                feature_mean=np.mean(featurevalues)

                '''
                ...
                @DATA       <- at data_indices[0]
                15.234234,1   <- data_indices[0]+1
                3.22313,2     <- data_indices[0]+2
                ...
                '''
                outfile.write(',' + str(feature_mean))

        outfile.write('\n') #one song finished


print('Finished')
print('')
