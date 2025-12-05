import csv
import os
from pathlib import Path

listOfPlayLists: dict[str,list[str]] = {}

class PlaylistManager:
    playlistDir = os.path.dirname(os.path.abspath(__file__))+os.sep+"playlists"+os.sep
    def __init__(self):
        try:
            for file in os.listdir(self.playlistDir):
                songs = []
                print(self.playlistDir+file)
                playlistPath = self.playlistDir+file
                with open(playlistPath) as playlistCSV:
                    readPlaylist = csv.reader(playlistCSV,delimiter=',')
                    for songList in readPlaylist:
                        songs=songList
                    listOfPlayLists[Path(file).stem] = songs
            print (listOfPlayLists)
        except FileNotFoundError:#No file playlist -> no playlists
            os.mkdir(self.playlistDir)


pm = PlaylistManager()
