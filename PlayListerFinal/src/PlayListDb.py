from SongDbEntry import SongDbEntry
from os.path import exists
import csv

class PlayListDb:  

    def __init__(self, name='PlayList.csv'):
        # CSV filename         
        self.ExportFileName = name
        # initialize container of database entries 
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
        """ 
        1,OMG,NewJeaqns,KPoP,january 7 2024,www. cccc
        2,Bad,Michael Jackson,Pop,January 6 2024,zzzz
        3,qwe,asd,Rock,February 12 2023,dasdsad
        4,asdasf,gfddhdf,Rnb,March 3 2023,asdsad
        5,rty,abc,Rnb,March 3 2023,asdsad
        """
        return self.songlist
    

    def insert_song(self, songID, songTitle, artist, genre, date, spot_link):
        """
        - inserts an entry in the database
        - no return value
        """
        newEntry = SongDbEntry(songID, songTitle, artist, genre, date, spot_link)
        self.songlist.append(newEntry)

    def delete_song(self, id):
        """
        - deletes the corresponding entry in the database as specified by 'id'
        - no return value
        """

        for entry in self.songlist:
            if entry.songID == id:
                self.songlist.remove(entry)
                break
        
    def update_song(self, new_songID, new_songTitle, new_artist, new_genre, new_date, new_spot_link):
        """
        - updates the corresponding entry in the database as specified by 'id'
        - no return value
        """
        for entry in self.songlist:
            if entry.songID == new_songID:
                entry.songTitle = new_songTitle
                entry.artist = new_artist
                entry.genre = new_genre
                entry.date = new_date
                entry.spot_link = new_spot_link
                break

    def export_csv(self, new_filename = ""):
        """
        - exports database entries as a CSV file
        - CSV : Comma Separated Values
        - no return value
        - example
        12,Eileen Dover,SW-Engineer,Male,On-Site
        13,Ann Chovey,HW-Engineer,Female,On-Site
        14,Chris P. Bacon,SW-Engineer,Male,On-Leave
        15,Russell Sprout,SW-Engineer,Male,Remote
        16,Oscar Lott,Project-Manager,Male,On-Site        
        """
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
        """
        - returns True if an entry exists for the specified 'id'
        - else returns False
        """
        for song in self.songlist:
            if song.songID == id:
                return True    
        return False
    
    def __str__(self):
        """ 
        - string representation of the class
        """
        dataStr = ''
        for entry in self.songlist:
            dataStr += f'{entry.songID} {entry.PlaylistID} {entry.songTitle} {entry.artist} {entry.genre} {entry.Date_Added} {entry.spot_link} \n' 
        return f'{dataStr}'
    




#a = PlayListDb ('misc/liam2.csv')


#print (a)
#a.update_song('1', 5, 'Ditto', 'NewJeans', 'Pop', 'January 2 2024', 'zzz')
#a.insert_song('5', 'Ditto', 'NewJeans', 'Pop', 'January 2 2024', 'zzz')
#a.export_csv('misc/liam2.csv')
#a.delete_song('5', 'nwjns', 'gegege', 'Pop', 'January 2 2024', 'aaa')
#a.export_csv()