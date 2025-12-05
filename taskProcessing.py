import csv
import os
from pathlib import Path
import random

listOfPlayLists: dict[str,list[str]] = {}

class PlaylistManager:
    playlistDir = os.path.dirname(os.path.abspath(__file__))+os.sep+"playlists"+os.sep
    #Read in playlists
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
        except FileNotFoundError:#No file playlist -> no playlists
            os.mkdir(self.playlistDir)

    def createPlaylist(self,playlistName):
        playlistPath = self.playlistDir+playlistName
        f = open(playlistPath+".csv",'a')
        listOfPlayLists[playlistName] = []
    
    def addToPlaylist(self, playlistName, songs:list[str]):
        addedSongs = []
        playlistPath = self.playlistDir+playlistName
        with open(playlistPath+".csv", "w") as playlistCSV:
            for song in songs:
                if song in listOfPlayLists[playlistName]:
                    print(f"{song} is already in playlist {playlistName}!")
                else:
                    listOfPlayLists[playlistName].append(song)
                    addedSongs.append(song)
            for song in listOfPlayLists[playlistName]:
                if song != listOfPlayLists[playlistName][len(listOfPlayLists[playlistName])-1]:
                    playlistCSV.write(song+",")
                else:
                    playlistCSV.write(song)
        print(f"{addedSongs} have been added to {playlistName}")
    
    def removeFromPlaylist(self, playlistName, songs:list[str]):
        delSongs = []
        playlistPath = self.playlistDir+playlistName
        with open(playlistPath+".csv", "w") as playlistCSV:
            for song in songs:
                if song in listOfPlayLists[playlistName]:
                    listOfPlayLists[playlistName].remove(song)
                    delSongs.append(song)
                else:
                    print(f"{song} is not present in {playlistName}!")
            for song in listOfPlayLists[playlistName]:
                if song != listOfPlayLists[playlistName][len(listOfPlayLists[playlistName])-1]:
                    playlistCSV.write(song+",")
                else:
                    playlistCSV.write(song)
        print(f"{delSongs} have been removed from {playlistName}")

    def shuffle(self, playlistName):
        random.shuffle(listOfPlayLists[playlistName])
        print(f"{playlistName} shuffled")
    
    def deletePlaylist(self, playlistName):
        playlistPath = self.playlistDir+playlistName+".csv"
        os.remove(playlistPath)
        print(f"{playlistName} deleted")
    
    def clearPlaylist(self, playlistName):
        listOfPlayLists[playlistName] = []
        print(f"{playlistName} cleared")

    def showPlaylist(self, playlistName):
        songs = []
        for song in listOfPlayLists[playlistName]:
            songs.append(song)
        print(songs)