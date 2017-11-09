#!/bin/bash
outdir="previewMusik"
mkdir "$outdir"

duration=30 #output song duration

FILES="Musik/*/*/*.mp3"
for f in $FILES
do
	filename="${f##*/}" #extract only filename
	parentdir="$(dirname "$f")" #musik/a/2/asdf.mp3  -> musik/a/2
	hash2="${parentdir##*/}" #musik/a/2  -> 2
	parentparentdir="$(dirname "$parentdir")" #musik/a/2 -> musik/a
	hash1="${parentparentdir##*/}" #musik/a  -> a
	fullhashfilename="$hash1$hash2$filename" #a/2/asdf.mp3 -> a2asdf.mp3

	echo "Processing $f"
	echo "Hash=$fullhashfilename"
	l=$(mp3info -p "%S" $f)
	#echo "Length=$l s"
	starttime=$(( l/2 - duration/2))
	#echo "Starttime= $starttime"
	if [ "$l" -lt "$duration" ]
	then
	 echo "$f is too short: length=$l seconds. Using whole song"
	 starttime=0
	 #example 1/9/b8f2800f3e7eb7006b73b0a55079f5b8b804e6af7caf98ffacb7de0ce1bb19.mp3   27seconds
	 #read temp
  fi

	stminute=$((starttime/60))
	stsecond=$((starttime%60))
	stsecond=$(printf "%02d" $stsecond) #add leading zero

	etminute=$(( (starttime+duration)/60))
	etsecond=$(( (starttime+duration)%60))
	etsecond=$(printf "%02d" $etsecond) #add leading zero
	echo "Use segment= $stminute:$stsecond - $etminute:$etsecond"
	mp3cut -o "$outdir/$fullhashfilename" -t $stminute:$stsecond-$etminute:$etsecond $f
done