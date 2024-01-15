from SongDbEntry import SongDbEntry
from os.path import exists
import csv

class PlayListDb:  

    def __init__(self, name='PlayList.csv'):         
        self.ExportFileName = name 
        self.songlist = [] 
        ExistingEntries = self.fetch_fromCSV()
        for m in ExistingEntries:
            print(m)
            b = SongDbEntry(m[0],m[1],m[2],m[3],m[4],m[5])
            self.songlist.append(b)

    def fetch_fromCSV(self):
        rows = []

        file_exists = exists(self.ExportFileName)
        if (file_exists):
            with open(self.ExportFileName, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    rows.append(row)

        return rows
    

    def fetch_songs(self):
        return self.songlist
    

    def insert_song(self, songID, songTitle, artist, genre, date, spot_link):
        newEntry = SongDbEntry(songID, songTitle, artist, genre, date, spot_link)
        self.songlist.append(newEntry)

    def delete_song(self, id):
        for entry in self.songlist:
            if entry.songID == id:
                self.songlist.remove(entry)
                break
        
    def update_song(self, new_songID, new_songTitle, new_artist, new_genre, new_date, new_spot_link):
        for entry in self.songlist:
            if entry.songID == new_songID:
                entry.songTitle = new_songTitle
                entry.artist = new_artist
                entry.genre = new_genre
                entry.date = new_date
                entry.spot_link = new_spot_link
                break

    def export_csv(self, new_filename = ""):
        if new_filename == "":
            new_filename = self.ExportFileName

        with open(new_filename, 'w', encoding= 'cp1252') as f:
            writer = csv.writer(f)
            for entry in self.songlist:
                data = []
                data.append(entry.songID)
                data.append(entry.PlaylistID)
                data.append(entry.songTitle)
                data.append(entry.artist)
                data.append(entry.genre)
                data.append(entry.Date_Added)
                data.append(entry.spot_link)
    

                writer.writerow(data)


    def songID_exists(self, id):
        for song in self.songlist:
            if song.songID == id:
                return True    
        return False
    
    def __str__(self):
        dataStr = ''
        for entry in self.songlist:
            dataStr += f'{entry.songID} {entry.PlaylistID} {entry.songTitle} {entry.artist} {entry.genre} {entry.Date_Added} {entry.spot_link} \n' 
        return f'{dataStr}'
