# Vorgehensweise für das Einfügen von Musik-Metadaten in die Datenbank und Erstellen einer .sql Datei zum Initialisieren der Datenbank

1. Korrektes Anlegen der Dateistruktur mit dem dafür vorgesehenen Skript MP3-File-Hashing
2. Platzieren des id3todb.py Skripts im entsprechenden Ordner
3. Datenbank lokal starten
4. Skript ausführen
5. Aus der Datenbank die Tabellen `album`, `artist`, `song`, `album_artist`, `song_artist` exportieren. Dies geht am einfachsten mit einem grafischen Client, wie z.B. HeidiSQL, ein ähnliches Ergebnis liefert aber auch der Befehl: `pg_dump --file=./80music_data.sql --table=album --table=artist --table=song --table=album_artist --table=song_artist --dbname=reactivejukebox --host=localhost --port=5432 --username=postgres --inserts`
6. Die erstellte Datei `80music_data.sql` so anpassen, dass diese nur noch INSERTs enthält und am Kopf der Datei folgendes ergänzen: `\connect reactivejukebox`
7. Verschieben der Datei in den entsprechenden Ordner im Database Repository