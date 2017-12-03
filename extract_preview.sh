#!/bin/bash

# list_include_item "10 11 12" "2"
function list_include_item {
  local list="$1"
  local item="$2"
  if [[ $list =~ (^|[[:space:]])"$item"($|[[:space:]]) ]] ; then
    # yes, list include item
    result=0
  else
    result=1
  fi
  return $result
}

outdir="previewMusik"
mkdir "$outdir"
seekdir="previewMusik"

duration=30 #output song duration

EXISTINGFILES=$(ls $seekdir/)
FILES="Music/*/*/*.mp3"
for f in $FILES
do
	filename="${f##*/}" #extract only filename
	parentdir="$(dirname "$f")" #musik/a/2/asdf.mp3  -> musik/a/2
	hash2="${parentdir##*/}" #musik/a/2  -> 2
	parentparentdir="$(dirname "$parentdir")" #musik/a/2 -> musik/a
	hash1="${parentparentdir##*/}" #musik/a  -> a
	fullhashfilename="$hash1$hash2$filename" #a/2/asdf.mp3 -> a2asdf.mp3

	if `list_include_item "$EXISTINGFILES" "$fullhashfilename"` #if file already exists
	then
		echo "Skipped $f"
		continue #skip this file
	fi

	echo "Processing $f Hash=$fullhashfilename"
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
	#echo "Use segment= $stminute:$stsecond - $etminute:$etsecond"
	mp3cut -o "$outdir/$fullhashfilename" -t $stminute:$stsecond-$etminute:$etsecond $f
done
