import csv
serverlogfile="studie.csv"
googleforms="Jukebox Studie.csv"
outputfile="test.csv"
data=[]
isHeader=True


def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def mapText(entry,array): #map entry-text to index of this text in array
    for i,e in enumerate(array):
        if e==entry:
            return i
    print("!!!! ERROR in mapText: "+str(entry)+" not found in array "+str(array))
    exit()

def mapBinary(string,array): #map string to array as binary with last element for not found strings. string="asdf", array=["bbb","ccc","asdf"] -> ["",0,0,1]
    returnarray=[0 for x in array]
    splitstring=string.split(";")
    for ie,e in enumerate(splitstring): #every user entry (checked box)
        for ix,x in enumerate(array): #possible given answers
            if x==e: #current element is an answer
                returnarray[ix]=1 #set element index to true
                splitstring[ie]=""
    freetext=[x for x in splitstring if len(x)>0]
    if len(freetext)>0:
        returnarray.append(freetext[0])
    else:
        returnarray.append("")
    return returnarray

with open(googleforms, 'r') as f: #every user has exactly one line in the google forms file
    reader = csv.reader(f, delimiter=',', quotechar='\"')
    for row in reader: #for every user-id
        if isHeader:
            isHeader=False
            continue #skip header

        #print(row)

        datadict={}
        datadict["ID"]=int(row[1])
        datadict["Time"]=row[0]
        datadict["Zufriedenheit Songs"]=mapText(row[2],["","sehr unzufrieden","unzufrieden","eher unzufrieden","eher zufrieden","zufrieden","sehr zufrieden"]) #1-6
        datadict["Songrelevanz"]=mapText(row[3],["","sehr schlecht","schlecht","eher schlecht","eher gut","gut","sehr gut"])
        _unpassend=mapBinary(row[4],["Die Songs waren zu ähnlich","Die Songs waren zu unterschiedlich","Die Songs waren zu bekannt","Die Songs waren zu unbekannt"])
        datadict["Songs unpassend (zu aehnlich)"]=_unpassend[0]
        datadict["Songs unpassend (zu unterschiedlich)"]=_unpassend[1]
        datadict["Songs unpassend (zu bekannt)"]=_unpassend[2]
        datadict["Songs unpassend (zu unbekannt)"]=_unpassend[3]
        datadict["Songs unpassend (Freitext)"]=_unpassend[4]

        datadict["Weitere Anmerkungen zu Empfehlungen?"]=row[5]
        datadict["Feedbackmoeglichkeiten sinnvoll"]=mapText(row[6],["","6 - sehr sinnlos","5","4","3","2","1 - sehr sinnvoll"])
        datadict["Merkmal (Interpret)"]=mapText(row[7],["","sehr unwichtig","unwichtig","eher unwichtig","eher wichtig","wichtig","sehr wichtig"])
        datadict["Merkmal (Erscheinungsjahr)"]=mapText(row[8],["","sehr unwichtig","unwichtig","eher unwichtig","eher wichtig","wichtig","sehr wichtig"])
        datadict["Merkmal (Album)"]=mapText(row[9],["","sehr unwichtig","unwichtig","eher unwichtig","eher wichtig","wichtig","sehr wichtig"])
        datadict["Merkmal (Genre)"]=mapText(row[10],["","sehr unwichtig","unwichtig","eher unwichtig","eher wichtig","wichtig","sehr wichtig"])
        datadict["Merkmal (Stimmung)"]=mapText(row[11],["","sehr unwichtig","unwichtig","eher unwichtig","eher wichtig","wichtig","sehr wichtig"])
        datadict["Merkmal (Tempo)"]=mapText(row[12],["","sehr unwichtig","unwichtig","eher unwichtig","eher wichtig","wichtig","sehr wichtig"])
        datadict["Merkmal (Popularität)"]=mapText(row[13],["","sehr unwichtig","unwichtig","eher unwichtig","eher wichtig","wichtig","sehr wichtig"])
        datadict["Merkmal (Freitext)"]=row[14]
        datadict["Tempoaenderung Art"]=mapText(row[15],["","Alle Songs sollten ähnliches Tempo haben","Das Tempo der Songs sollte variieren","Die Radiostation sollte langsam beginnen und sich dann steigern","Die Radiostation solle schnell beginnen und dann langsamer werden","Das Tempo ist für die Radiostation nicht wichtig"])
        datadict["Intiuitivaet Radiostationserstellung"]=mapText(row[16],["","desaströs (keine Optionen wurden gefunden)", "sehr unintuitiv (die meisten Optionen waren schwierig zu finden)","unintuitiv (einige Optionen waren schwierig zu finden)","intuituv (alle Optionen innerhalb weniger Sekunden gefunden)","sehr intuitiv (alle Optionen sofort gefunden)","perfekt (genau so wie gewünscht)"])
        datadict["Intuitivitaet Feedback"]=mapText(row[17],["","desaströs (keine Optionen wurden gefunden)", "sehr unintuitiv (die meisten Optionen waren schwierig zu finden)","unintuitiv (einige Optionen waren schwierig zu finden)","intuituv (alle Optionen innerhalb weniger Sekunden gefunden)","sehr intuitiv (alle Optionen sofort gefunden)","perfekt (genau so wie gewünscht)"])
        datadict["Nutzen Feedback"]=mapText(row[18],["","6 - auf keinen Fall","5","4","3","2","1 - absolut"])
        datadict["Freitext Anmerkungen Feedback / UI"]=row[19]
        datadict["Alter"]=int(row[20][0:2])
        datadict["Spielt Instrument"]=mapText(row[21],["","6 - Ich spiele kein Instrument","5","4","3","2","1 - Profi-Musiker"])
        datadict["Konzertbesuche"]=mapText(row[22],["","seltener","1-2 mal","3-5 mal","5-10 mal","mehr als 10 mal"])
        _musikdienst=mapBinary(row[23],["Radio","Spotify","Amazon Music","iTunes","Deezer","Soundcloud","Google Play Music","Napster"])
        datadict["Musik-Dienste (Radio)"]=_musikdienst[0]
        datadict["Musik-Dienste (Spotify)"]=_musikdienst[1]
        datadict["Musik-Dienste (Amazon Music)"]=_musikdienst[2]
        datadict["Musik-Dienste (iTunes)"]=_musikdienst[3]
        datadict["Musik-Dienste (Deezer)"]=_musikdienst[4]
        datadict["Musik-Dienste (Soundcloud)"]=_musikdienst[5]
        datadict["Musik-Dienste (Google Play Music)"]=_musikdienst[6]
        datadict["Musik-Dienste (Napster)"]=_musikdienst[7]
        datadict["Musik-Dienste (Freitext)"]=_musikdienst[8]
        datadict["Musikkonsum / tag"]=mapText(row[24],["","< 10","10 bis 30","30 bis 60","60 bis 120","> 120"])
        datadict["Verwendung vorgefertige PL"]=mapText(row[25],["","ausschließlich selbst erstellte","meist selbst erstellte","meist vorgefertigte","ausschließlich vorgefertigte"])
        datadict["Weitere Anmerkungen"]=row[26]

        datadict["#Erstellte od. Aktualisierte Radiostationen"]=0
        datadict["#Aktualisierte Radiostationen"]=0
        datadict["#Genre"]=0
        datadict["#Tempo"]=0
        datadict["#Mood"]=0
        datadict["#Year"]=0
        datadict["#Startsong"]=0
        datadict["#FB+ Genre"]=0
        datadict["#FB+ Artist"]=0
        datadict["#FB+ Song"]=0
        datadict["#FB+ Album"]=0
        datadict["#FB+ Mood"]=0
        datadict["#FB+ Tempo"]=0
        datadict["#FB- Genre"]=0
        datadict["#FB- Artist"]=0
        datadict["#FB- Song"]=0
        datadict["#FB- Album"]=0
        datadict["#FB- Mood"]=0
        datadict["#FB- Tempo"]=0
        datadict["#Skips"]=0
        datadict["#Multiskips"]=0
        datadict["#Deletes"]=0
        datadict["#Finished Songs"]=0

        userNotFoundInServerlog=True #gets set to false if found

        with open(serverlogfile, 'r') as f: # Serverlogfile
            logreader = csv.reader(f, delimiter=';')
            logheader=None
            for logrow in logreader: #for every user-id
                if not RepresentsInt(logrow[1]): #if USER column has no number in current row -> row is a header
                    if logheader is None:
                        logheader=logrow
                    continue
                _timestamp=logrow[logheader.index('TIMESTAMP')]
                _uID=int(logrow[logheader.index('USER')])
                _event=logrow[logheader.index('EVENT')]

                if _uID!=datadict["ID"]: #current log line belongs not current user-id
                    continue

                userNotFoundInServerlog=False #user has been found

                if _event=="RADIO_START":
                    datadict["#Erstellte od. Aktualisierte Radiostationen"]+=1
                if _event=="RADIO_UPDATE": #TODO: heisst das event wirklich RADIO_UPDATE?

                    datadict["#Erstellte od. Aktualisierte Radiostationen"]+=1
                    datadict["#Aktualisierte Radiostationen"]+=1

                if _event=="RADIO_START" or _event=="RADIO_UPDATE":
                    if len(row[logheader.index('GENRE')])>0:
                        datadict["#Genre"]+=1
                    if len(row[logheader.index('SPEED_MIN')])>0:
                        datadict["#Tempo"]+=1
                    if len(row[logheader.index('AROUSAL')])>0:
                        datadict["#Mood"]+=1
                    if len(row[logheader.index('YEAR_START')])>0:
                        datadict["#Year"]+=1
                    if len(row[logheader.index('SONG')])>0:
                        datadict["#Startsong"]+=1

                if _event=="GENRE_FEEDBACK":
                    if row[logheader.index('RATING_SONG')]=="1": #positive feedback
                        datadict["#FB+ Genre"]+=1
                    else:
                        datadict["#FB- Genre"]+=1

                if _event=="ALBUM_FEEDBACK":
                    if row[logheader.index('RATING_SONG')]=="1": #positive feedback
                        datadict["#FB+ Album"]+=1
                    else:
                        datadict["#FB- Album"]+=1

                if _event=="SONG_FEEDBACK":
                    if row[logheader.index('RATING_SONG')]=="1": #positive feedback
                        datadict["#FB+ Song"]+=1
                    else:
                        datadict["#FB- Song"]+=1

                if _event=="ARTIST_FEEDBACK":
                    if row[logheader.index('RATING_SONG')]=="1": #positive feedback
                        datadict["#FB+ Artist"]+=1
                    else:
                        datadict["#FB- Artist"]+=1

                if _event=="TEMPO_FEEDBACK": #TODO: heist es so?
                    if row[logheader.index('RATING_SONG')]=="1": #positive feedback
                        datadict["#FB+ Tempo"]+=1
                    else:
                        datadict["#FB- Tempo"]+=1

                if _event=="MOOD_FEEDBACK": #TODO:heisst es so?
                    if row[logheader.index('RATING_SONG')]=="1": #positive feedback
                        datadict["#FB+ Mood"]+=1
                    else:
                        datadict["#FB- Mood"]+=1

                if _event=="ACTION_FEEDBACK":
                    if row[logheader.index('USER_ACTION')]=="SKIP": #positive feedback
                        datadict["#Skips"]+=1
                    if row[logheader.index('USER_ACTION')]=="MULTI_SKIP": #positive feedback
                        datadict["#Multiskips"]+=1
                    if row[logheader.index('USER_ACTION')]=="\DELETE": #positive feedback
                        datadict["#Deletes"]+=1
                if _event=="HISTORY_POST":
                    datadict["#Finished Songs"]+=1

        if not userNotFoundInServerlog: #user was also in server log
            data.append(datadict) #append one user data to list


#random order
#keys=[key for key in data[0].keys()]

#or used defined order
keys=["ID","Time","Zufriedenheit Songs","Songrelevanz","Songs unpassend (zu aehnlich)","Songs unpassend (zu unterschiedlich)","Songs unpassend (zu bekannt)","Songs unpassend (zu unbekannt)","Songs unpassend (Freitext)","Weitere Anmerkungen zu Empfehlungen?","Feedbackmoeglichkeiten sinnvoll","Merkmal (Interpret)","Merkmal (Erscheinungsjahr)","Merkmal (Album)","Merkmal (Genre)","Merkmal (Stimmung)","Merkmal (Tempo)","Merkmal (Popularität)","Merkmal (Freitext)","Tempoaenderung Art","Intiuitivaet Radiostationserstellung","Intuitivitaet Feedback","Nutzen Feedback","Freitext Anmerkungen Feedback / UI","Alter","Spielt Instrument","Konzertbesuche","Musik-Dienste (Radio)","Musik-Dienste (Spotify)","Musik-Dienste (Amazon Music)","Musik-Dienste (iTunes)","Musik-Dienste (Deezer)","Musik-Dienste (Soundcloud)","Musik-Dienste (Google Play Music)","Musik-Dienste (Napster)","Musik-Dienste (Freitext)","Musikkonsum / tag","Verwendung vorgefertige PL","Weitere Anmerkungen","#Erstellte od. Aktualisierte Radiostationen","#Aktualisierte Radiostationen","#Genre","#Tempo","#Mood","#Year","#FB+ Genre","#FB+ Artist","#FB+ Song","#FB+ Album","#FB+ Mood","#FB+ Tempo","#FB- Genre","#FB- Artist","#FB- Song","#FB- Album","#FB- Mood","#FB- Tempo","#Skips","#Multiskips","#Deletes","#Finished Songs"]


#write data to file
with open(outputfile, 'w') as f:
    writer = csv.writer(f,delimiter=';', quotechar='"')
    writer.writerow(keys) #write header

    for userdict in data: #for every user
        writer.writerow([userdict[x] for x in keys])
