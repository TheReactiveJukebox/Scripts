#!/usr/bin/env python3
#sorts the genres array in any csv with the genres column
#can work on lastfmdata and spotifydata
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

def normalizeTag(tagname):
    tagname = tagname.replace('-', ' ')  # rock-pop -> rock pop
    tagname = tagname.replace('\'', '')  # 90's -> 90s
    tagname = tagname.replace('+', ' ')  # dance+and+electronica -> dance and electronica
    tagname = tagname.replace('/', ' ')  # singer/songwriter -> singer songwriter
    tagname = tagname.replace('.', ' ')  # post.rock -> post rock
    tagname = tagname.replace('_', ' ')  # alternative_metal -> alternative metal
    return tagname

not_inflate_tags=['rock & roll']

def inflate_tags(tags):
    tags_new = []
    for t in tags:  # 'alternative rock'
        if (t in not_inflate_tags):
            continue #skip not_inflate_tags tags
        if type(t) is not str:  # some tags can be of type 'byte' (for example Oasis - Wonderwall)
            t = t.decode('UTF-8')  # decode byte to string
        tt = t.split(' ')  # ['alternative','rock']
        if ('classic' in tt and len(tt)>1):
            tt.remove('classic') #remove 'classic', if it was part of a genre like 'classic rock'
        tt += [t]  # ['alternative', 'rock', 'alternative rock']
        tt = [x.rstrip() for x in tt]
        tags_new += tt

    return tags_new


def correct_tags(tags):  # correct common spelling mistakes
    tags_correct = []
    search_for = ['electro','electonic','electronic dance', 'r&b', 'electro swing', 'synth pop', 'ragga', 'synthie pop', 'genre: deep house',
                  'rhythm and blues', 'hellektro', 'pbrnb', '1960s', '1970s', '1980s', '1990s', '00s', 'hiphop', 'triphop', 'edm', 'psy trance','eurotrance','euro pop','euro dance','rock n roll','rock & roll','electro pop','psy trance','pop trance','punk pop']
    replace_with = ['electronic','electronic', 'electro dance' ,'rnb', 'electroswing', 'synthpop', 'reggae', 'synthpop', 'deep house',
                    'rhythm & blues', 'aggrotech', 'alternative rnb', '60s', '70s', '80s', '90s', '2000s', 'hip hop', 'trip hop', 'electronic dance music', 'psytrance','euro trance','europop','eurodance','rock and roll','rock and roll','electropop','psytrance','trance pop','pop punk']
    for t in tags:
        for sfindex, sf in enumerate(search_for):
            t = t.replace(search_for[sfindex], replace_with[sfindex])
        tags_correct += [t]
    return tags_correct


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

                        songgenres = c.replace('[','').replace(']','').replace('\'','').split(',')  #convert list-string to list
                        songgenres = [x.lstrip() for x in songgenres] #remove whitespace on the left of each genre

                        #Filter and normalize tags (if they are not already)
                        tags = songgenres #handle songgenres as unfiltered tags
                        tags = inflate_tags(tags)  # inflate tags (also fix utf8 tags), example: 'alternative rock' -> 'alternative rock','alternative','rock'
                        tags = [normalizeTag(t) for t in tags]  # normalize tags. for example replace '-' by ' '
                        tags = correct_tags(tags)  # correct typos

                        track_genres = [x for x in tags if x in genres]  # search for tags with a genre. Filters out non-genre tags


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
