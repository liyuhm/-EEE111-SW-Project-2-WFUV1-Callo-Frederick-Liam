class PlaylistDbEntry:
    def __init__(self,
                 playListID=1,
                 playListName='Playlist Name'
                 ):
        self.playListID = playListID
        self.playListName = playListName
        
    def __str__(self):
        """ 
        - string representation of the class
        """

        return f' {self.playListID} {self.playListName}  ' 
