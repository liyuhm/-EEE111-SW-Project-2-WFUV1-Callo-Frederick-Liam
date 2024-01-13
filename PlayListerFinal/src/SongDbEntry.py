from datetime import date

class SongDbEntry:
    def __init__(self,
                 songID,
                 songTitle,
                 artist, 
                 genre, 
                 date,
                 spot_link
                 ):
        
        self.songID = songID
        self.PlaylistID = ""
        self.songTitle = songTitle
        self.artist = artist
        self.genre = genre
        self.spot_link = spot_link

        if date == "":
            today = date.today()
            self.Date_Added = today.strftime('%B %d, %Y')
        else: 
            self.Date_Added = date


    def __str__(self):
        """ 
        - string representation of the class
        """

        return f' {self.songID} {self.songTitle} {self.artist} {self.genre} {self.Date_Added}' 
