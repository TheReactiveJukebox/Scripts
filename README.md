This is a collection of scripts that support the setup and execution process of the Reactive Jukebox project.
One of the main purposes of these scripts is to generate all the necessary database entries from a set of provided MP3 files.
Most other scripts are used internally for the team organization and for the evaluation of the user study.

## How to get data from new music files into database
This is only a small description on how to establish a fresh music database with the scripts provided in this repository.
Feel free to skip any steps, if you don't think they are necessary.

### Step 1: Hash music files
Place your music files into a directory `Music` inside of this directory.
You might have to create one yourself.
After that, run the `filehash.sh` script and wait for it to finish.
Your files inside of the `Music` directory should be hashed and in the correct structure now.

### Step 2: Get ID3 data
Place your (hashed) music files into a directory `Music` inside of this directory.
After that, run the `d3tocsv.sh` script and wait for it to finish.
You now should have a new file called `id3data.csv` inside of this directory.

### Step 3: Generate and fetch additional metadata
Place the `id3data.csv` file inside of this directory.
After that, run the `metadata.sh` script and press `y` for every step you want to execute.
Depending on what you chose, you now should have the files `lastfmdata.csv`, `bpm.csv`, `dynamics.csv` and `spotifydata.csv`.

### Step 4: Insert data into database
Required files in this directory: `spotifydata.csv`, `ExternalDataSource/genres.csv`, `bpm.csv` and `dynamics.csv`.
Run the `datatodb.sh` script and wait for it to finish. 

### Step 5: Export data from database into file
Export the tables `album`, `album_artist`, `artist`, `genre`, `song`, `song_artist` and `song_genre` from the database.
This is easily accomplished by using a graphical client like HeidiSQL.
If you don't want to use that, the following command should to the same thing: `pg_dump --file=./80music_data.sql --table=album --table=artist --table=song --table=genre --table=album_artist --table=song_artist --table=song_genre --dbname=reactivejukebox --host=localhost --port=5432 --username=postgres --inserts`.
Rename the file to `80music_data.sql` and place it in the correct directory in the database repository.
Remove any lines of the file that don't start with an `INSERT` statement and add the following in the first line: `\connect reactivejukebox`
