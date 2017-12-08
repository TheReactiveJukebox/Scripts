#!/usr/bin/env python3
#sorts the genres array in any csv with the genres column
#usage: python3 sortgenres.py lastfmdata.csv genres.csv genres_meta.csv lastfmdata_sorted.csv

import csv
import os
import sys
import numpy as np

inputfile=sys.argv[1] #lastfmdata.csv
genresfile=sys.argv[2] #genres.csv
metagenresfile=sys.argv[3] #genres_meta.csv
outpath=sys.argv[4] #outputcsv.csv
genres=[]
metagenres=[]

with open(genresfile, 'r') as genresdata: #all genres
    csvgenres=csv.reader(genresdata)
    with open(metagenresfile, 'r') as metagenresdata: # all metagenres (subset of genres)
        csvmetagenres=csv.reader(metagenresdata)
        for mg in csvmetagenres:
            metagenres.append(mg) #all metagenres to list

    for genre in csvgenres: #for every listed genre
        if genre not in metagenres: #only subgenres
            genre=genre[0]
            genres.append(genre)

    for genre in metagenres: #for every listed metagenre
        genre=genre[0]
        genres.append(genre) #append metagenres to the end (lowest priority)

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
                    c=c.replace('"','""') #replace " with double "", csv convention
                    if ci==genrecolumn: #at genres column

                        songgenres=c.replace('[','').replace(']','').replace('\'','').split(',')  #convert list-string to list
                        songgenres=[x.lstrip() for x in songgenres] #remove whitespace on the left of each genre

                        #sort genres by genres-list
                        songgenres_sorted=[]
                        for cg in genres: #go through all sorted genres

                            if cg in songgenres:
                                songgenres_sorted.append(cg) #add genre to output

                        c=str(songgenres_sorted) #convert back to string for csv


                    if ci>0:
                        outdata.write(',')

                    if c.find(',')>=0:
                        c='"'+c+'"' #add " to make it one entry in csv
                    outdata.write(c)
                outdata.write('\n')
