#!/bin/bash

echo "Do you want to fetch metadata from LastFM and Musicbrainz? (y/n)"
read lastfm

if [ ${lastfm} == "y" ]
then
    echo "Fetching data, this could take a few minutes..."
    python ./LastFmMusicBrainz/lastfmcrawler.py ./id3data.csv ./LastFmMusicBrainz/genres.csv
    echo "LastFM data successfully fetchted."
elif [ ${lastfm} == "n" ]
then
    echo "Skipping LastFM and Musicbrainz crawler."
else
    echo "Wrong user input!"
    exit
fi

echo "Do you want to generate BPM data from librosa? (y/n)"
read librosabpm

if [ ${librosabpm} == "y" ]
then
    echo "Generating data, this could take a few minutes..."
    python ./Librosa/SongAnalyzer.py bpm ./Music
    echo "BPM data successfully generated."
elif [ ${librosabpm} == "n" ]
then
    echo "Skipping Librosa BPM generation."
else
    echo "Wrong user input!"
    exit
fi

echo "Do you want to generate dynamics data from librosa? (y/n)"
read librosadyn

if [ ${librosadyn} == "y" ]
then
    echo "Generating data, this could take a few minutes..."
    python ./Librosa/SongAnalyzer.py dynamics ./Music
    echo "Dynamics data successfully generated."
elif [ ${librosadyn} == "n" ]
then
    echo "Skipping Librosa dynamics generation."
else
    echo "Wrong user input!"
    exit
fi

echo "Do you want to fetch metadata from Spotify? (y/n)"
read spotify

if [ ${spotify} == "y" ]
then
    echo "Fetching data, this could take a few minutes..."
    python ./Spotify/Spotify.py lastfmdata.csv
    echo "Spotify data successfully fetched."
elif [ ${spotify} == "n" ]
then
    echo "Skipping Spotify data fetching."
else
    echo "Wrong user input!"
    exit
fi