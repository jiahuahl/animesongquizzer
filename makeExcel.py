import sys
import subprocess
import os
import random

def MakeCsv():
    file = open("database.csv", "w")
    file.write("id,title,song,anime,songtype,artist,qstart,qend,atime,difficulty,copyright\n")
    
    for songFolder in os.listdir("data"):
        AddEntry(file, songFolder)

    file.close()

def AddEntry(file, songFolder):
#    for line in file:
#        if line.startswith("indatabase"):
#            if(line[line.find(":")+1:].strip() == "true"):
#                return #already have this

    info = open("data\\"+songFolder+"\\info.txt", "r")
    
    id = songFolder
    title = ""
    song = ""
    anime = ""
    songtype = ""
    artist = ""
    qstart = ""
    qend = ""
    atime = ""
    difficulty = ""
    copyright = ""
    
    for line in info:
        if line.startswith("title"):
            title = line[line.find(":")+1:].strip()
        elif line.startswith("song"):
            song = line[line.find(":")+1:].strip()
        elif line.startswith("anime"):
            anime = line[line.find(":")+1:].strip()
        elif line.startswith("type"):
            songtype = line[line.find(":")+1:].strip()
        elif line.startswith("artist"):
            artist = line[line.find(":")+1:].strip()
        elif line.startswith("qstart"):
            qstart = line[line.find(":")+1:].strip()
        elif line.startswith("qend"):
            qend = line[line.find(":")+1:].strip()
        elif line.startswith("atime"):
            atime = line[line.find(":")+1:].strip()
        elif line.startswith("difficulty"):
            difficulty = line[line.find(":")+1:].strip()
        elif line.startswith("copyright"):
            copyright = line[line.find(":")+1:].strip()

    info.close()
    entryList = [id, title, song, anime, songtype, artist, qstart, qend, atime, difficulty, copyright]
    processedEntries = []
    for entry in entryList:
        entry = "\"" + entry + "\""
        processedEntries.append(entry)
    entryString = ",".join(processedEntries) + "\n"
    file.write(entryString)

def main(argv):
    MakeCsv()

if __name__ == "__main__":
    main(sys.argv[1:])
