import sqlite3
from datetime import date
from tkinter import filedialog
import csv

class PlaylistDbSqlite:
    def __init__(self, dbName='PlayList.db'):
        super().__init__()
        self.dbName = dbName
        self.csvFile = self.dbName.replace('.db', '.csv')
        self.create_table()

    def connect_cursor(self):
        self.conn = sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()        

    def commit_close(self):
        self.conn.commit()
        self.conn.close()        

    def create_table(self):
        self.connect_cursor()
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS SongTable (
                    songID TEXT PRIMARY KEY,
                    songTitle TEXT,
                    artist TEXT,
                    genre TEXT,
                    spot_link TEXT,
                    dateAdded TEXT)''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS PlaylistTable (
                playListID INTEGER PRIMARY KEY AUTOINCREMENT,
                playListName TEXT,
                dateAdded TEXT)''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS SongPlaylistTable (
                songID TEXT,
                playListID TEXT)''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS GenreTable (
                genreID INTEGER PRIMARY KEY AUTOINCREMENT,
                genreName TEXT)''')

        self.commit_close()

    def fetch_songs(self):
        self.connect_cursor()
        self.cursor.execute('SELECT * FROM SongTable')
        songs = self.cursor.fetchall()
        self.conn.close()
        return songs

    def fetch_playLists(self):
        self.connect_cursor()
        self.cursor.execute('SELECT s.* FROM PlayListTable p left outer join SongTable s on p.playListID = s.songID')
        songs = self.cursor.fetchall()
        self.conn.close()
        return songs

    def fetch_genres(self):
        self.connect_cursor()
        self.cursor.execute('SELECT genreName FROM GenreTable')
        genres = self.cursor.fetchall()
        self.conn.close()
        return genres

    def insert_song(self, songID, songTitle, artist, genre, spot_link, dateAdded):
        self.connect_cursor()
        self.cursor.execute('INSERT INTO SongTable ( songID, songTitle, artist, genre, dateAdded, spot_link) VALUES ( ?, ?, ?, ?, ?, ?)',
                    ( songID, songTitle, artist, genre, dateAdded, spot_link))
        self.commit_close()

    def insert_playlist(self, playListName, dateAdded = date.today()):
        self.connect_cursor()
        self.cursor.execute('INSERT INTO playListTable ( playListName, dateAdded) VALUES ( ?, ?)',
                    (playListName, dateAdded))
        self.commit_close()

    def insert_songPlayList(self, songTitle, playListName):
        self.connect_cursor()

        self.cursor.execute('SELECT songID FROM SongTable WHERE songTitle = ?', (songTitle,))
        result =self.cursor.fetchone()
        songID = result[0]
        self.cursor.execute('SELECT playListID FROM playListTable WHERE playListName = ?', (playListName,))
        result =self.cursor.fetchone()
        playListID = result[0]
        self.conn.close()

        self.connect_cursor()
        self.cursor.execute('INSERT INTO songPlayListTable (songID, playListID) VALUES (?, ?)',
                    (songID, playListID))
        self.commit_close()

    def delete_song(self, songID):
        self.connect_cursor()
        self.cursor.execute('DELETE FROM SongTable WHERE songID = ?', (songID,))
        self.commit_close()

    def update_song(self, new_songTitle, new_artist, new_genre, new_dateAdded, new_spot_link, songID):
        self.connect_cursor()
        self.cursor.execute('UPDATE SongTable SET songTitle = ?, artist = ?, genre = ?, dateAdded = ?, spot_link = ? WHERE songID = ?',
                    (new_songTitle, new_artist, new_genre, new_dateAdded, new_spot_link, songID))
        self.commit_close()

    def update_playlist(self, new_songTitle, new_artist, new_genre, new_dateAdded, new_spot_link, songID):
        self.connect_cursor()
        self.cursor.execute('UPDATE SongTable SET songTitle = ?, artist = ?, genre = ?, dateAdded = ?, spot_link = ? WHERE songID = ?',
                    (new_songTitle, new_artist, new_genre, new_dateAdded, new_spot_link, songID))

        #self.cursor.execute('UPDATE playListTable SET playListName = ? WHERE playListID = ?',
        #            (new_playListName, playListID))
        self.commit_close()

    def songID_exists(self, songID):
        self.connect_cursor()
        self.cursor.execute('SELECT COUNT(*) FROM SongTable WHERE songID = ?', (songID,))
        result =self.cursor.fetchone()
        self.conn.close()
        return result[0] > 0

    def songTitle_exists(self, song):
        self.connect_cursor()
        self.cursor.execute('SELECT COUNT(*) FROM SongTable WHERE songTitle = ?', (song,))
        result =self.cursor.fetchone()
        self.conn.close()
        return result[0] > 0

    def playList_exists(self, playlist):
        self.connect_cursor()
        self.cursor.execute('SELECT COUNT(*) FROM PlayListTable WHERE playListName = ?', (playlist,))
        result =self.cursor.fetchone()
        self.conn.close()
        return result[0] > 0

    def export_csv(self):
        with open(self.csvFile, "w") as filehandle:
            dbEntries = self.fetch_songs()
            for entry in dbEntries:
                print(entry)
                filehandle.write(f"{entry[0]},{entry[1]},{entry[2]},{entry[3]},{entry[4]},{entry[5]}\n")

    def import_csv(self):
        file_path = filedialog.askopenfilename(title="Select CSV File", filetypes=[("CSV files", "*.csv")])

        with open(file_path, 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                for row in csv_reader:
                    print(f"CSV Row: {row}")
                    (songID, songTitle, artist, genre, spot_link, dateAdded) = row
                    self.insert_song(songID, songTitle, artist, genre, spot_link, dateAdded)

def test_SongDb():
    iSongDb = PlaylistDbSqlite(dbName='PlayListDb.db')

    for i in range(30):
        iSongDb.insert_songs(f'{i}', f'playlistID{i}', f'Title{i}', f'Artist{i}', f'Genre {i}', '2024/02/25', 'https://open.spotify.com/track/3gRhGExNITCqVo0mCyqp3m?si=eecb9d27c8f44712')
        assert iSongDb.id_exists(f'{i}')

    all_entries = iSongDb.fetch_songs()
    assert len(all_entries) == 30

    for i in range(10, 20):
        iSongDb.update_songs(f'playlistID{i}', f'Title{i}', f'Artist{i}', f'Genre {i}', '2022/11/25', 'https://open.spotify.com/track/6zdryckXPbIeQE5npNqvNp?si=0782a0c55dac40e1', i)
        assert iSongDb.id_exists(i)

    all_entries = iSongDb.fetch_songs()
    assert len(all_entries) == 30

    for entry in range(10):
        iSongDb.delete_songs(entry)
        assert not iSongDb.id_exists(entry) 

    all_entries = iSongDb.fetch_songs()
    assert len(all_entries) == 20