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
                playlistPath = self.playlistDir+file
                with open(playlistPath) as playlistCSV:
                    readPlaylist = csv.reader(playlistCSV,delimiter=',')
                    for songList in readPlaylist:
                        songs=songList
                    listOfPlayLists[Path(file).stem] = songs
        except FileNotFoundError:#No file playlist -> no playlists
            os.mkdir(self.playlistDir)

    #create a playlist
    def createPlaylist(self,playlistName):
        if playlistName not in listOfPlayLists.keys():
            playlistPath = self.playlistDir+playlistName
            f = open(playlistPath+".csv",'a')
            listOfPlayLists[playlistName] = []
            return f"Playlist {playlistName} has been created"
        else:
            return f"{playlistName} already exists"
    
    #add a song to the playlist
    def addToPlaylist(self, playlistName, songs:list[str]):
        alrExistSongs =[]
        if len(songs)>0:
            addedSongs = []
            playlistPath = self.playlistDir+playlistName
            with open(playlistPath+".csv", "w") as playlistCSV:
                for song in songs:
                    if song in listOfPlayLists[playlistName]:
                        alrExistSongs.append(song)
                    else:
                        listOfPlayLists[playlistName].append(song)
                        addedSongs.append(song)
                for song in listOfPlayLists[playlistName]:
                    if song != listOfPlayLists[playlistName][len(listOfPlayLists[playlistName])-1]:
                        playlistCSV.write(song+",")
                    else:
                        playlistCSV.write(song)
            ret = "I've added "
            if len(addedSongs)>0:
                ret += ", ".join(addedSongs)
            else:
                ret += "no songs"
            ret += f" to {playlistName}"
            if len(alrExistSongs)>0:
                ret += f". These songs were already in {playlistName}: {", ".join(alrExistSongs)}"
            return ret
        else:
            return "Please tell me which songs you'd like to add"
    
    #delete a song from the playlist
    def removeFromPlaylist(self, playlistName, songs:list[str]):
        delSongs = []
        neSongs = []
        if len(songs)>0:
            playlistPath = self.playlistDir+playlistName
            with open(playlistPath+".csv", "w") as playlistCSV:
                for song in songs:
                    if song in listOfPlayLists[playlistName]:
                        listOfPlayLists[playlistName].remove(song)
                        delSongs.append(song)
                    else:
                        neSongs.append(song)
                for song in listOfPlayLists[playlistName]:
                    if song != listOfPlayLists[playlistName][len(listOfPlayLists[playlistName])-1]:
                        playlistCSV.write(song+",")
                    else:
                        playlistCSV.write(song)
            ret = "I've removed "
            if len(delSongs)>0:
                ret += ", ".join(delSongs)
            else:
                ret += "no songs"
            ret += f" from {playlistName}"
            if len(neSongs)>0:
                ret += f". These songs weren't present in {playlistName}: {", ".join(neSongs)}"
            return ret
        else:
            return "Please tell me which songs you'd like to delete"

    #shuffle playlist
    def shuffle(self, playlistName):
        if playlistName in listOfPlayLists.keys():
            random.shuffle(listOfPlayLists[playlistName])
            return f"{playlistName} has been shuffled"
        else:
            return f"There's no playlist called {playlistName}, do you want me to make it?"
    
    #delete playlist entirely
    def deletePlaylist(self, playlistName):
        playlistPath = self.playlistDir+playlistName+".csv"
        os.remove(playlistPath)
        listOfPlayLists.pop(playlistName)
        return f"{playlistName} has been deleted"
    
    #remove all songs from playlist
    def clearPlaylist(self, playlistName):
        if playlistName in listOfPlayLists.keys():
            listOfPlayLists[playlistName] = []
            return f"{playlistName} has been cleared"
        else:
            return f"There's no playlist called {playlistName}, do you want me to make it?"

    #return the songs in the playlist
    def showPlaylist(self, playlistName):
        if playlistName in listOfPlayLists.keys():
            songs = []
            for song in listOfPlayLists[playlistName]:
                songs.append(song)
            return f"{playlistName} has these songs: {", ".join(songs)}"
        else:
                return f"There's no playlist called {playlistName}, do you want me to make it?"