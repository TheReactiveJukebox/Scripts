#!/bin/bash

b=4 #number of threads
for (( a=1;a<=b; a++))
do
    #echo $a-$b
    #python3 ./Librosa/SongAnalyzer.py bpm /media/fisch/HDD/Musik\ PG $a-$b
    screen -S songanalyzer -d -m /usr/bin/python3 ./Librosa/SongAnalyzer.py bpm,dynamics ./Music PG $a-$b
done

echo "started $b processes in screens. To see debug messages, attach w/ -> screen -r songanalyzer <- to any of them."

while screen -list | grep -q ".*songanalyzer"; do
    sleep 2
done
echo "all processes finished"

python3 ./Librosa/mergecsv.py bpm.csv $b #merges all bpm.csv_... to bpm.csv
rm bpm.csv_* #remove all temp files

python3 ./Librosa/mergecsv.py dynamics.csv $b #merges all dynamics.csv_... to dynamics.csv
rm dynamics.csv_* #remove all temp files
