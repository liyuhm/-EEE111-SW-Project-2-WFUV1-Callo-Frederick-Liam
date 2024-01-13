class PlaylistSongDbEntry:
    def __init__(self,
                 id=1,
                 PlayListID,
                 SongID
                 ):
        self.id = id
        self.playListID = PlayListID
        self.songID = SongID
        
    def __str__(self):
        """ 
        - string representation of the class
        """

        return f' {self.id} {self.playListID} {self.songListID} ' 
