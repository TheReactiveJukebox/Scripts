#!/usr/bin/env python3
#sorts the genres array in any csv with the genres column
#usage: python3 sortgenres.py lastfmdata.csv genres.csv lastfmdata_sorted.csv

import csv
import os
import sys
import numpy as np

inputfile=sys.argv[1] #lastfmdata.csv
genresfile=sys.argv[2] #genres.csv
outpath=sys.argv[3] #outputcsv.csv
genres=[]

with open(genresfile, 'r') as genresdata:
    csvgenres=csv.reader(genresdata)
    for genre in csvgenres:
        genre=genre[0]
        genres.append(genre)

print(str(len(genres))+' genres found')


csvheader=''
genrecolumn=0
with open(inputfile, 'r') as inputdata:
    with open(outpath, 'w') as outdata:
        csvinputdata=csv.reader(inputdata)
        for row in csvinputdata: #for every song
            if csvheader=='': #read header
                csvheader=row
                genrecolumn=csvheader.index('genres')
                for ci,c in enumerate(row):
                    if ci>0:
                        outdata.write(',')
                    outdata.write(c)
                outdata.write('\n')

            else:


                for ci,c in enumerate(row):
                    if ci==genrecolumn: #at genres column

                        songgenres=c.replace('[','').replace(']','').replace('\'','').split(',')  #convert list-string to list
                        songgenres=[x.lstrip() for x in songgenres] #remove whitespace on the left of each genre

                        #sort genres by genres-list
                        songgenres_sorted=[]
                        for sg in genres: #go through all sorted genres

                            if sg in songgenres:
                                songgenres_sorted.append(sg) #add genre to output

                        c=str(songgenres_sorted) #convert back to string for csv


                    if ci>0:
                        outdata.write(',')

                    if c.find(',')>=0:
                        c='"'+c+'"' #add " to make it one entry in csv
                    outdata.write(c)
                outdata.write('\n')

    #outdata.write('\t('+str(nd_id)+', '+str(nd_genre)+', '+str(nd_metaid)+'),\n')
