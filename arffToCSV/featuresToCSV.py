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

featurenames=[   #["feature name",feature_id, feature_dimensions, preprocessing_mode]
["Zero-crossing rate",0,1,'mean'], # Timbre features
["Zero-crossing rate",0,1,'var'],
["Root mean square",4,1,'mean'],
["Low energy",6,1,'mean'],
["Tristimulus 2048",20051,2,'mean'],
["RMS peak number in 3 seconds",11,1,'mean'],
["Spectral irregularity 2048",20029,1,'mean'],
#["Spectral bandwidth 2048",20030,1,'mean'], #not available
#["Spectral crest factor 2048",20033,4,'mean'],
#["Spectral flatness measure 2048",20034,4,'mean'],
#["Distances in phase domain 2048",20041,1,'mean'],
["CMRARE cepstral modulation features with polynomial order 3",45,8,'mean'], #CMRARE
["CMRARE cepstral modulation features with polynomial order 5",46,12,'mean'],
["CMRARE cepstral modulation features with polynomial order 10",47,22,'mean'],
["Inharmonicity 2048",20053,1,'mean'], # Harmony and melody features
["Major/minor alignment 2048",20055,1,'mean'],
["Strengths of major keys 2048",20056,12,'mean'],
["Strengths of minor keys 2048",20057,12,'mean'],
["Harmonic change detection function 2048",20059,1,'mean'],
["Spectral brightness 2048",20037,1,'mean'],
["Characteristics of fluctuation patterns",410,7,'mean'], #Tempo features
["Rhythmic clarity",418,1,'mean'],
["Estimated onset number per minute",420,1,'mean']
]
featurenames=np.array(featurenames)  #featurenames[:,0] returns all names


with open(csvoutpath, 'w') as outfile:

    outfile.write('songHash' )
    for currentfeature in featurenames: #for every feature
        feature_name=currentfeature[0]
        feature_dimension=int(currentfeature[2])
        feature_preprocessingmode=currentfeature[3]

        if (feature_dimension<=1): #feature has only one dimension
            outfile.write(',' + feature_name)  #write header
        else: #multi dimenional feature
            for fi in np.arange(1,feature_dimension+1): #for every dimension
                outfile.write(',' + feature_name+' #'+str(fi))  #write header with dimension number

        #for preproessing modes other than mean add note to featurename in header
        if (feature_preprocessingmode=='var'):
            outfile.write(' !var')

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
            feature_dimension=int(currentfeature[2])
            feature_preprocessingmode=currentfeature[3]

            arff_file=hashdir+'/'+songhash+'_'+feature_id+'.arff'
            with open(arff_file, 'r') as featurefile:
                featurefile_lines=[x.replace('\n','') for x in featurefile.readlines()] #line from arff file to list
                data_indices = [i for i, s in enumerate(featurefile_lines) if '@DATA' in s]

                for fi in np.arange(1,feature_dimension+1): #for every dimension

                    featurevalues=[]
                    datacount=1 #start at 1
                    while data_indices[0]+datacount < len(featurefile_lines):
                        value=featurefile_lines[data_indices[0]+datacount].split(',')[fi-1] #extract data from arff
                        if isNumber(value): #some values can be NaN
                            featurevalues.append(float(value))
                        datacount+=1

                    if (feature_preprocessingmode=='mean'):
                        feature_preprocessed=np.mean(featurevalues)
                    elif (feature_preprocessingmode=='var'):
                        feature_preprocessed=np.var(featurevalues)

                    '''
                    ...
                    @DATA       <- at data_indices[0]
                    15.234234,1   <- data_indices[0]+1
                    3.22313,2     <- data_indices[0]+2
                    ...
                    '''
                    outfile.write(',' + str(feature_preprocessed))

        outfile.write('\n') #one song finished


print('Finished')
print('')
